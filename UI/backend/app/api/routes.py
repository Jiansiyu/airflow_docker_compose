from fastapi import APIRouter, UploadFile, Form, HTTPException
from app.config import settings
from requests.auth import HTTPBasicAuth
from datetime import datetime, timezone
import requests
from pathlib import Path
import shutil

router = APIRouter()

UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


def trigger_dag_run(dag_id: str, category: str, filename: str):
    """
    Trigger a DAG run in Airflow, passing in file and category as conf.
    """
    token = get_jwt_token()
    trigger_url = f"{settings.AIRFLOW_URL.rstrip('/')}/api/v2/dags/{dag_id}/dagRuns"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    now_z = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    payload = {
        "logical_date": now_z,
        # "dag_run_id": "cli_triggered_job",  # should be unique, but not required
        "conf": {
            "dag_id": dag_id,

        },
    }
    response = requests.post(trigger_url, headers=headers, json=payload)
    print(response.json())
    if response.status_code in [200, 201]:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


@router.post("/upload")
async def upload_file(file: UploadFile, category: str = Form(...), workflow: str = Form(...)):
    """
    Upload a file to the server and trigger a DAG run.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided.")
    if not workflow:
        raise HTTPException(status_code=400, detail="No workflow (DAG) specified.")

    # Save the file locally
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Trigger the DAG run in Airflow
    try:
        run_info = trigger_dag_run(workflow, category, file_path.name)
        return {
            "filename": file.filename,
            "category": category,
            "workflow": workflow,
            "message": "File uploaded and DAG triggered successfully.",
            "dag_run": run_info,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File uploaded, but failed to trigger DAG: {str(e)}")


# list all the ceres expression categories
@router.get("/eval/ceres/categories")
async def list_categories():
    """
    List all Ceres expression categories.
    """
    # This is a placeholder implementation. Replace with actual logic to fetch categories.
    categories = ["category1", "category2", "category3"]
    return {"categories": categories}


@router.get("/airflow/{dag_id}/dag_runs")
def get_dag_runs(dag_id: str):
    return {"dag_id": dag_id, "runs": []}


def get_jwt_token():
    auth_url = f"{settings.AIRFLOW_URL}/auth/token"
    credentials = {
        "username": settings.AIRFLOW_WWW_USER_USERNAME,
        "password": settings.AIRFLOW_WWW_USER_PASSWORD
    }
    response = requests.post(auth_url, json=credentials)
    if response.status_code in [200, 201]:
        return response.json().get("access_token")
    else:
        raise HTTPException(status_code=500, detail="Failed to obtain JWT token from Airflow.")


def list_airflow_dags() -> list[str]:
    token = get_jwt_token()
    resp = requests.get(
        f"{settings.AIRFLOW_URL.rstrip('/')}/api/v2/dags",
        headers={"Authorization": f"Bearer {token}"}
    )
    resp.raise_for_status()
    payload = resp.json()
    return [d["dag_id"] for d in payload.get("dags", [])]


# list all DAGs
@router.get("/airflow/dags/list")
def list_dags():
    try:
        dags = list_airflow_dags()
        return {"dags": dags}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# list runs for a specific DAG
@router.get("/airflow/{dag_id}/runs")
def list_dag_runs(dag_id: str):
    token = get_jwt_token()
    runs_url = f"{settings.AIRFLOW_URL.rstrip('/')}/api/v2/dags/{dag_id}/dagRuns"
    headers = {
        "Authorization" : f"Bearer {token}",
        "Content-Type": "application/json",
    }
    response = requests.get(runs_url, headers=headers)
    if response.status_code in [200, 201]:
        return response.json()
    else:
        # bubble up Airflow’s error text
        raise HTTPException(status_code=response.status_code, detail=response.text)


@router.post("/airflow/{dag_id}/trigger")
async def trigger_dag_api(dag_id: str):
    token = get_jwt_token()
    trigger_url = f"{settings.AIRFLOW_URL.rstrip('/')}/api/v2/dags/{dag_id}/dagRuns"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    now_z = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    payload = {
        "logical_date": now_z,
        "conf": {"dag_id": dag_id}
    }
    response = requests.post(trigger_url, headers=headers, json=payload)

    if response.status_code == 200:
        return {
            "message": "DAG triggered successfully.",
            "logical_date": now_z,
            "response": response.json(),
        }
    else:
        # bubble up Airflow’s error text
        raise HTTPException(status_code=response.status_code, detail=response.text)
