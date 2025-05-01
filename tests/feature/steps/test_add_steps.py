import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src')))
import pytest
from pytest_bdd import scenarios, given, when, then
from tasks import generate_unique_id, filter_tasks_by_category

# Link to your feature file
scenarios('../add_task.feature')


@pytest.fixture
def task_list():
    return []

@given("the task list is empty")
def empty_task_list(task_list):
    task_list.clear()

@when('I add a task with title "Buy groceries"')
def add_groceries_task(task_list):
    task_list.append({
        "id": generate_unique_id(task_list),
        "title": "Buy groceries",
        "description": "",
        "priority": "Medium",
        "category": "Personal",
        "due_date": "2025-05-01",
        "completed": False
    })

@then("the task list should contain 1 task")
def check_task_count(task_list):
    assert len(task_list) == 1

@when('I add a task with priority "High"')
def add_high_priority_task(task_list):
    task_list.append({
        "id": generate_unique_id(task_list),
        "title": "Urgent Task",
        "description": "",
        "priority": "High",
        "category": "Work",
        "due_date": "2025-05-01",
        "completed": False
    })

@then('the task should have priority "High"')
def assert_high_priority(task_list):
    assert any(task["priority"] == "High" for task in task_list)

@when('I add a task with category "Personal"')
def add_personal_task(task_list):
    task_list.append({
        "id": generate_unique_id(task_list),
        "title": "Personal Task",
        "description": "",
        "priority": "Low",
        "category": "Personal",
        "due_date": "2025-05-01",
        "completed": False
    })

@then('the task should be categorized as "Personal"')
def assert_personal_category(task_list):
    assert any(task["category"] == "Personal" for task in task_list)

@given('there is a task titled "Workout"')
def workout_task(task_list):
    task_list.append({
        "id": 5,
        "title": "Workout",
        "description": "",
        "priority": "Medium",
        "category": "Health",
        "due_date": "2025-05-01",
        "completed": False
    })

@when("I mark the task as completed")
def complete_workout(task_list):
    for task in task_list:
        if task["title"] == "Workout":
            task["completed"] = True

@then("the task should be marked completed")
def check_completion(task_list):
    task = next((t for t in task_list if t["title"] == "Workout"), None)
    assert task and task["completed"]

@given("there are tasks in multiple categories")
def multiple_category_tasks(task_list):
    task_list.extend([
        {"id": 1, "title": "Math HW", "category": "School", "completed": False},
        {"id": 2, "title": "Gym", "category": "Health", "completed": False}
    ])

@when('I filter tasks by category "School"')
def filter_by_school(task_list):
    task_list[:] = filter_tasks_by_category(task_list, "School")

@then('I should see only tasks in the "School" category')
def assert_only_school(task_list):
    assert all(task["category"] == "School" for task in task_list)
