import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import tasks
from tasks import filter_tasks_by_priority, save_tasks

#  Parameterized test
@pytest.mark.parametrize("priority, expected_count", [
    ("High", 2),
    ("Medium", 1),
    ("Low", 1),
    ("None", 0)
])
def test_filter_tasks_by_priority_param(priority, expected_count):
    task_list = [
        {"title": "Task 1", "priority": "High"},
        {"title": "Task 2", "priority": "Low"},
        {"title": "Task 3", "priority": "Medium"},
        {"title": "Task 4", "priority": "High"},
    ]
    filtered = filter_tasks_by_priority(task_list, priority)
    assert len(filtered) == expected_count

#  Mocking test using monkeypatch
def test_save_tasks_mock(monkeypatch):
    calls = {}

    def fake_save(tasks_input, file_path):
        calls["called"] = True
        calls["file_path"] = str(file_path)
        calls["tasks"] = tasks_input

    # Patch the actual function
    monkeypatch.setattr("tasks.save_tasks", fake_save)

    test_tasks = [{"id": 1, "title": "Mock Task", "priority": "High", "category": "Work", "completed": False, "due_date": "2025-05-01"}]
    tasks.save_tasks(test_tasks, file_path="dummy_path.json")

    assert calls["called"] is True
    assert calls["file_path"] == "dummy_path.json"
    assert calls["tasks"] == test_tasks
