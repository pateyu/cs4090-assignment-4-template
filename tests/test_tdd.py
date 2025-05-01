import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from datetime import datetime
from tasks import mark_all_tasks_complete, clear_completed_tasks, filter_urgent_tasks

def test_mark_all_tasks_complete():
    tasks = [
        {"id": 1, "title": "A", "completed": False},
        {"id": 2, "title": "B", "completed": False}
    ]
    result = mark_all_tasks_complete(tasks)
    assert all(task["completed"] for task in result)

def test_clear_completed_tasks():
    tasks = [
        {"id": 1, "completed": True},
        {"id": 2, "completed": False}
    ]
    result = clear_completed_tasks(tasks)
    assert len(result) == 1
    assert not result[0]["completed"]

def test_filter_urgent_tasks():
    today = datetime.now().strftime("%Y-%m-%d")
    tasks = [
        {"title": "Urgent", "priority": "High", "due_date": today, "completed": False},
        {"title": "Not Urgent", "priority": "Medium", "due_date": today, "completed": False}
    ]
    result = filter_urgent_tasks(tasks)
    assert len(result) == 1
    assert result[0]["title"] == "Urgent"
