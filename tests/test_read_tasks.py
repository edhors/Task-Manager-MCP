from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Connect to the database
engine = create_engine('sqlite:///tasks.db')
Session = sessionmaker(bind=engine)
session = Session()

# Get metadata
metadata = MetaData()
metadata.reflect(bind=engine)

# Get the tasks table
tasks_table = metadata.tables['tasks']

# Query all tasks
tasks = session.query(tasks_table).all()

# Print header
print("\nTasks Database Contents:")
print("-" * 100)
print(f"{'ID':<5} {'User ID':<8} {'Status':<10} {'Title':<30} {'Expiry':<20} {'Created At':<20} {'Updated At':<20}")
print("-" * 100)

# Print each task
for task in tasks:
    print(f"{task.id:<5} {task.user_id:<8} {task.status:<10} {task.title[:30]:<30} "
          f"{task.expiry.strftime('%Y-%m-%d %H:%M') if task.expiry else 'None':<20} "
          f"{task.created_at.strftime('%Y-%m-%d %H:%M'):<20} "
          f"{task.updated_at.strftime('%Y-%m-%d %H:%M'):<20}")

session.close() 