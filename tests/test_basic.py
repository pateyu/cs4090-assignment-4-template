import pytest
import sys
import os
import json
from datetime import datetime, timedelta

# Add parent directory to Python path to import tasks.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from tasks import (
    generate_unique_id,
    filter_tasks_by_priority,
    filter_tasks_by_category,
    filter_tasks_by_completion,
    search_tasks,
    get_overdue_tasks,
    save_tasks,
    load_tasks
)

def test_generate_unique_id():
    tasks = [{"id": 1}, {"id": 2}]
    assert generate_unique_id(tasks) == 3
    assert generate_unique_id([]) == 1

def test_filter_tasks_by_priority():
    tasks = [{"priority": "High"}, {"priority": "Low"}]
    filtered = filter_tasks_by_priority(tasks, "High")
    assert len(filtered) == 1
    assert filtered[0]["priority"] == "High"

def test_filter_tasks_by_category():
    tasks = [{"category": "Work"}, {"category": "Personal"}]
    filtered = filter_tasks_by_category(tasks, "Work")
    assert len(filtered) == 1
    assert filtered[0]["category"] == "Work"

def test_filter_tasks_by_completion():
    tasks = [{"completed": True}, {"completed": False}]
    assert len(filter_tasks_by_completion(tasks, True)) == 1
    assert len(filter_tasks_by_completion(tasks, False)) == 1

def test_search_tasks():
    tasks = [
        {"title": "Buy milk", "description": "from store"},
        {"title": "Study", "description": "math homework"}
    ]
    result = search_tasks(tasks, "milk")
    assert len(result) == 1
    assert result[0]["title"] == "Buy milk"

def test_get_overdue_tasks():
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    tasks = [
        {"title": "Late task", "due_date": yesterday, "completed": False},
        {"title": "Upcoming task", "due_date": tomorrow, "completed": False},
        {"title": "Done task", "due_date": yesterday, "completed": True}
    ]
    overdue = get_overdue_tasks(tasks)
    assert len(overdue) == 1
    assert overdue[0]["title"] == "Late task"

def test_save_and_load_tasks(tmp_path):
    tasks = [{"id": 1, "title": "Test Task", "priority": "High", "category": "Work", "completed": False, "due_date": "2025-05-01"}]
    test_file = tmp_path / "tasks.json"
    save_tasks(tasks, file_path=test_file)
    loaded = load_tasks(file_path=test_file)
    assert loaded == tasks

def test_load_tasks_invalid_json(tmp_path):
    test_file = tmp_path / "corrupt.json"
    test_file.write_text("Not JSON!")
    result = load_tasks(file_path=test_file)
    assert result == []
