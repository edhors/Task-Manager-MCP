from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import yaml

# Load user configuration
def load_users():
    with open('user_config.yaml', 'r') as f:
        return yaml.safe_load(f)['users']

# Connect to the database
engine = create_engine('sqlite:///tasks.db')
Session = sessionmaker(bind=engine)
session = Session()

# Load users
users = load_users()

# Print available users
print("\nAvailable Users:")
print("-" * 40)
for user in users:
    print(f"User ID: {user['user_id']} - Name: {user['name']}")

# Get task details
print("\nEnter task details:")
user_id = int(input("User ID: "))
title = input("Title: ")
details = input("Details: ")
expiry_input = input("Expiry date (YYYY-MM-DD HH:MM) [optional, press Enter to skip]: ")

# Validate user_id
if not any(user['user_id'] == user_id for user in users):
    print(f"Error: User ID {user_id} not found in configuration")
    exit(1)

# Parse expiry date if provided
expiry = None
if expiry_input.strip():
    try:
        expiry = datetime.strptime(expiry_input, "%Y-%m-%d %H:%M")
    except ValueError:
        print("Error: Invalid date format. Please use YYYY-MM-DD HH:MM")
        exit(1)

# Create and add task
try:
    from task_server import Task  # Import Task model from task_server.py
    task = Task(
        user_id=user_id,
        title=title,
        details=details,
        expiry=expiry
    )
    session.add(task)
    session.commit()
    print(f"\nTask created successfully with ID: {task.id}")
except Exception as e:
    print(f"Error creating task: {str(e)}")
    session.rollback()
finally:
    session.close() 