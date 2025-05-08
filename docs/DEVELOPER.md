# Developer Guide

This guide contains information for developers working on the Task Manager MCP.

## Development Environment Setup

### Prerequisites

- Python 3.8+
- Docker (for container development)
- VS Code with Remote Development extension (recommended)
- UV package manager

### Environment Setup Options

#### Option 1: Using Dev Container (Recommended)
The project includes a dev container configuration that automatically sets up your development environment:

1. Install Docker and VS Code with Remote Development extension
2. Open the project in VS Code
3. Click "Reopen in Container" when prompted
4. The container will automatically:
   - Install UV
   - Create a virtual environment
   - Install all dependencies from pyproject.toml

#### Option 2: Manual Setup
If you prefer not to use containers, you can set up manually:

```bash
# Install UV package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create and activate virtual environment
uv venv
source .venv/bin/activate

# Install dependencies from pyproject.toml
uv pip install -e .
```

## Project Structure

```
tms/
├── .devcontainer/       # Dev container configuration
├── docs/               # Documentation
├── src/                # Source code
├── tests/              # Test files
├── pyproject.toml      # Project configuration and dependencies
└── user_config.yaml    # Application configuration
```

## Dependencies

Dependencies are managed through `pyproject.toml`. The project uses UV package manager for better performance and dependency resolution.

### Key Dependencies
- fastmcp - Latest stable version
- sqlalchemy - Latest stable version
- pyyaml - Latest stable version

### Checking Installed Packages
To verify your environment:
```bash
source .venv/bin/activate  # Activate virtual environment
pip list  # List all installed packages
```

## Configuration

Application configuration is handled through `user_config.yaml`. Copy the example configuration and modify as needed:
```bash
cp user_config.yaml.example user_config.yaml
```

## Code Style Guide

We use Ruff for code formatting and linting. The configuration is in `pyproject.toml`:

- Line length: 120 characters
- Python target version: 3.8+
- Formatting style: Based on Black
- Quote style: Double quotes

### Type Hints

Use type hints in all new code:

```python
def add_task(title: str, user_id: int, details: Optional[str] = None) -> Task:
    ...
```

## Database Management

We use SQLAlchemy for database operations:

- Models are defined in `models.py`
- Use SQLAlchemy's declarative base
- Always use transactions for data modifications
- Include database migrations for schema changes

Example:
```python
from sqlalchemy.orm import Session

def create_task(db: Session, task: TaskCreate) -> Task:
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
```

## Testing

### Running Tests

```bash
pytest tests/
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files with `test_` prefix
- Use pytest fixtures for common setup
- Aim for high test coverage

Example:
```python
def test_create_task():
    task = create_task(
        title="Test Task",
        user_id=1,
        details="Test details"
    )
    assert task.title == "Test Task"
    assert task.user_id == 1
```

## API Documentation

The API is documented using FastAPI's automatic documentation:

- Access at `/docs` when running the server
- Include docstrings for all API endpoints
- Document all parameters and return types

Example:
```python
@app.post("/tasks/", response_model=Task)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new task.

    Args:
        task: Task creation model
        db: Database session

    Returns:
        Created task
    """
    return crud.create_task(db=db, task=task)
```

## Deployment

### Container Deployment

1. Build the container:
   ```bash
   docker build -t tms .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 tms
   ```

### Environment Variables

Required environment variables:
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Application secret key
- `DEBUG`: Enable/disable debug mode

## Contributing

1. Create a new branch for your feature
2. Write tests for new functionality
3. Ensure all tests pass
4. Submit a pull request

### Commit Messages

Follow conventional commits:
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Test updates

## Troubleshooting

Common issues and solutions:

1. **Database Connection Issues**
   - Check DATABASE_URL environment variable
   - Verify database server is running
   - Check network connectivity

2. **Development Container Issues**
   - Rebuild container: `Dev Containers: Rebuild Container`
   - Check Docker daemon is running
   - Verify devcontainer.json configuration 