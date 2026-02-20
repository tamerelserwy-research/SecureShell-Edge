# syntax=docker/dockerfile:1
FROM python:3.10-slim-bookworm

# Set environment variables for reproducibility
ENV PYTHONHASHSEED=42 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements-freeze.txt .
RUN pip install --no-cache-dir -r requirements-freeze.txt

# Copy source code
COPY secure_llm.py validator.py sandbox.py run_evaluation.py ./

# Optional: Download dataset at build time (uncomment if you want the dataset baked in)
# RUN wget -q --show-progress https://zenodo.org/records/18636114/files/SecLLM_PowerShell_Dataset.json

# Create directory for models (user must place model files here when running)
RUN mkdir -p /app/models

# Set entrypoint (can be overridden)
ENTRYPOINT ["python", "run_evaluation.py"]
CMD []
