# syntax=docker/dockerfile:1
FROM python:3.10-slim

# Install system dependencies including Rust toolchain
RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# Install UV using pip (more reliable than the installer script)
RUN pip install uv

# Set work directory
WORKDIR /app

# Copy lock file and project files
COPY uv.lock pyproject.toml ./
COPY src/ ./src/

# Install dependencies using UV with lock file
RUN uv sync --frozen

# Copy the rest of the project
COPY . .

# Create user_config.yaml if it doesn't exist
RUN echo 'users:\n  - user_id: 1\n    name: "Default User"' > user_config.yaml

# Expose FastMCP server port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the FastMCP task server using UV
CMD ["uv", "run", "python", "src/task_server.py"] 