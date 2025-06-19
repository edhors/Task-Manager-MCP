# syntax=docker/dockerfile:1
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY src/ ./src/

# Install dependencies using pip
RUN pip install -e .

# Copy the rest of the project (if needed)
COPY . .

# Expose FastAPI default port
EXPOSE 8000

# Set environment variables (optional, can be overridden)
ENV PYTHONUNBUFFERED=1

# Default command (update the module path as needed)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"] 