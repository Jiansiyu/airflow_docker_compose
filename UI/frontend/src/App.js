import { useState, useEffect } from 'react';
import axios from 'axios';
import FileUploadForm from './components/FileUploadForm';
import PastRunsTable from './components/PastRunsTable';

export default function App() {
  const [file, setFile] = useState(null);
  const [category, setCategory] = useState('');
  const [categories, setCategories] = useState([]);
  const [workflow, setWorkflow] = useState('');
  const [workflows, setWorkflows] = useState([]);
  const [runs, setRuns] = useState([]);
  const BASE_URL = process.env.REACT_APP_BACKEND_BASE_URL;

  const fetchCategories = async () => {
    const res = await axios.get(`${BASE_URL}/eval/ceres/categories`);
    setCategories(res.data.categories);
  };

  const fetchWorkflows = async () => {
    const res = await axios.get(`${BASE_URL}/airflow/dags/list`);
    setWorkflows(res.data.dags);
  };

  useEffect(() => {
    fetchCategories();
    fetchWorkflows();
    const mockRuns = [
      {
        id: 1,
        workflow: 'example_dag',
        status: 'success',
        stored_filename: 'example_run.rrd',
        file_path: 'https://app.rerun.io/version/0.20.3/examples/arkit_scenes.rrd',
      },
      {
        id: 2,
        workflow: 'data_pipeline',
        status: 'running',
        stored_filename: 'data_pipeline_run.rrd',
        file_path: 'https://app.rerun.io/version/0.20.3/examples/arkit_scenes.rrd',
      },
      {
        id: 3,
        workflow: 'analytics_job',
        status: 'failed',
        stored_filename: 'analytics_job_run.rrd',
        file_path: 'https://app.rerun.io/version/0.20.3/examples/arkit_scenes.rrd',
      },
    ];
    setRuns(mockRuns);

  }, []);

  const uploadAndStart = async () => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('category', category);
    formData.append('workflow', workflow);

    try {
      const res = await axios.post(`${BASE_URL}/upload`, formData);
      console.log(res.data);
      alert("Upload and DAG trigger successful!");
    } catch (err) {
      console.error(err);
      alert("Upload or DAG trigger failed.");
    }
  };

  return (
      <div className="min-h-screen bg-gray-50 p-8">
        <h1 className="text-2xl font-bold mb-4">Airflow Job Dashboard</h1>

        <FileUploadForm
            onUpload={{ file, setFile, category, setCategory, workflow, setWorkflow, uploadAndStart }}
            categories={categories}
            workflows={workflows}
        />
        <PastRunsTable runs={runs} />
      </div>
  );
}
