from fastmcp.server import FastMCP
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from fastapi.responses import JSONResponse, HTMLResponse
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import yaml
import os

# Database setup
Base = declarative_base()
engine = create_engine('sqlite:///tasks.db')
Session = sessionmaker(bind=engine)

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String(1024), nullable=False)
    details = Column(String(1024), nullable=False)
    expiry = Column(DateTime, nullable=True)
    status = Column(String(20), default='active')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create tables
Base.metadata.create_all(engine)

# Load user configuration
def load_users():
    with open('user_config.yaml', 'r') as f:
        return yaml.safe_load(f)['users']

# Initialize FastMCP server
server = FastMCP()

@server.custom_route("/healthz", methods=["GET"])
async def health_check(request):
    return JSONResponse({"status": "ok"})


@server.custom_route("/", methods=["GET"])
async def home_dir(request):
    # return a simple html page with a link to the sse endpoint
    return HTMLResponse(content="<h1>Hello , I'm working well</h1>")

@server.tool()
def create(user_id: int, title: str, details: str, expiry: str = None) -> int:
    """Create a new task for the specified user."""
    users = load_users()
    if not any(user['user_id'] == user_id for user in users):
        raise ValueError(f"User ID {user_id} not found in configuration")
    
    session = Session()
    try:
        task = Task(
            user_id=user_id,
            title=title,
            details=details,
            expiry=datetime.fromisoformat(expiry) if expiry else None
        )
        session.add(task)
        session.commit()
        return task.id
    finally:
        session.close()

@server.tool()
def update(task_id: int, title: str = None, details: str = None, expiry: str = None) -> int:
    """Update an existing task."""
    session = Session()
    try:
        task = session.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise ValueError(f"Task ID {task_id} not found")
        if task.status != 'active':
            raise ValueError("Cannot update a cancelled task")
            
        if title is not None:
            task.title = title
        if details is not None:
            task.details = details
        if expiry is not None:
            task.expiry = datetime.fromisoformat(expiry)
            
        session.commit()
        return task.id
    finally:
        session.close()

@server.tool()
def cancel(task_id: int) -> bool:
    """Cancel a task."""
    session = Session()
    try:
        task = session.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise ValueError(f"Task ID {task_id} not found")
        if task.status != 'active':
            return False
            
        task.status = 'cancelled'
        session.commit()
        return True
    finally:
        session.close()

@server.tool()
def list(user_id: int = None):
    """List all active tasks, optionally filtered by user_id."""
    session = Session()
    try:
        query = session.query(Task).filter(Task.status == 'active')
        if user_id is not None:
            query = query.filter(Task.user_id == user_id)
        tasks = query.all()
        return [{
            'task_id': t.id,
            'user_id': t.user_id,
            'title': t.title,
            'details': t.details,
            'expiry': t.expiry.isoformat() if t.expiry else None,
            'status': t.status
        } for t in tasks]
    finally:
        session.close()

@server.tool()
def details(task_id: int):
    """Get details of a specific task."""
    session = Session()
    try:
        task = session.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise ValueError(f"Task ID {task_id} not found")
            
        return {
            'task_id': task.id,
            'user_id': task.user_id,
            'title': task.title,
            'details': task.details,
            'expiry': task.expiry.isoformat() if task.expiry else None,
            'status': task.status,
            'created_at': task.created_at.isoformat(),
            'updated_at': task.updated_at.isoformat()
        }
    finally:
        session.close()

@server.tool()
def search(search_key: str):
    """Search tasks by title or details."""
    session = Session()
    try:
        tasks = session.query(Task).filter(
            Task.status == 'active',
            (Task.title.contains(search_key) | Task.details.contains(search_key))
        ).all()
        
        return [{
            'task_id': t.id,
            'user_id': t.user_id,
            'title': t.title,
            'details': t.details,
            'expiry': t.expiry.isoformat() if t.expiry else None,
            'status': t.status
        } for t in tasks]
    finally:
        session.close()

if __name__ == "__main__":
    import sys
    # Get port from command line or use default
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    
    print(f"Starting Task Management MCP Server on port {port}...")
    server.run(transport='sse', port=8000, host='0.0.0.0') 
