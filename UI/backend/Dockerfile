# Use a slim Python image as the base
FROM python:3.12-slim

# Set environment variables to avoid Python buffering and enable pip cache dir
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

# Set the working directory
WORKDIR /app

# Copy the requirements and install
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY app/ ./app/
COPY alembic.ini .
COPY alembic/ ./alembic/
COPY scripts/ ./scripts/
COPY uploads/ ./uploads/
COPY pyproject.toml .

# Copy the .env file (if needed at runtime only, can also mount as a volume)

# Expose FastAPI port
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# Use a slim Python image as the base
FROM python:3.12-slim

# Set environment variables to avoid Python buffering and enable pip cache dir
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

# Set the working directory
WORKDIR /app



# Copy the application code
COPY app/ ./app/
COPY alembic.ini .
COPY alembic/ ./alembic/
COPY scripts/ ./scripts/
COPY uploads/ ./uploads/
COPY pyproject.toml .

# Copy the requirements and install

RUN pip install .

# Expose FastAPI port
EXPOSE 8000

# Command to run the FastAPI application
COPY scripts/start.sh .
CMD ["./start.sh"]
