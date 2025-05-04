# Developer Guide

This guide contains information for developers working on the Task Manager MCP.

## Development Environment Setup

### Prerequisites

- Python 3.8+
- Docker (for container development)
- VS Code with Remote Development extension (recommended)
- UV package manager

### Local Setup

1. **Clone and Setup:**
   ```bash
   git clone <repository-url>
   cd tms
   curl -LsSf https://astral.sh/uv/install.sh | sh
   uv venv
   source .venv/bin/activate
   uv pip install -e .
   ```

2. **IDE Configuration:**
   - Use VS Code with the following extensions:
     - Python
     - Ruff (for linting/formatting)
     - Docker
     - Remote Development

## Project Structure

```
tms/
├── .devcontainer/       # Dev container configuration
├── docs/               # Documentation
├── src/                # Source code
├── tests/              # Test files
└── pyproject.toml      # Project configuration
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