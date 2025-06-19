# syntax=docker/dockerfile:1
FROM python:3.8-slim

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install UV package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Set work directory
WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY src/ ./src/
COPY user_config.yaml.example ./user_config.yaml.example

# Install dependencies
RUN uv venv && \
    .venv/bin/uv pip install -e .

# Copy the rest of the project (if needed)
COPY . .

# Expose FastAPI default port
EXPOSE 8000

# Set environment variables (optional, can be overridden)
ENV PYTHONUNBUFFERED=1

# Default command (update the module path as needed)
CMD [".venv/bin/uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"] 