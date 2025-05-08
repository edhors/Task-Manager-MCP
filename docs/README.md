# Task Manager MCP

A modern task management system built with Python, featuring FastMCP and SQLAlchemy for data persistence.

## Features

- Create, read, update, and delete tasks
- Assign tasks to specific users
- Set task expiry dates
- Search and filter tasks
- Command-line interface for task management

## Prerequisites

- Python 3.8 or higher
- UV package manager

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd tms
   ```

2. **Setup Development Environment:**
   There are two ways to set up the environment:

   **Using Dev Container (Recommended):**
   1. Install Docker and VS Code with Remote Development extension
   2. Open the project in VS Code
   3. Click "Reopen in Container" when prompted
   4. The container will automatically set up everything

   **Manual Setup:**
   ```bash
   # Install UV package manager
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Create and activate virtual environment
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

   # Install dependencies from pyproject.toml
   uv pip install -e .
   ```

3. **Configure the application:**
   - Copy `user_config.yaml.example` to `user_config.yaml`
   - Update the configuration as needed

## Docker Development

The project includes a dev container configuration for consistent development environments:

1. Install Docker and VS Code with Remote Development extension
2. Open the project in VS Code
3. Click "Reopen in Container" when prompted
4. The container will automatically set up the development environment with UV