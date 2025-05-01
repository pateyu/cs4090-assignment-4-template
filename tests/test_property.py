import sys
import os
try:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
    from tasks import (
        generate_unique_id,
        filter_tasks_by_priority,
        filter_tasks_by_category,
        search_tasks,
        filter_tasks_by_completion
    )
except ModuleNotFoundError:
    from src.tasks import (
        generate_unique_id,
        filter_tasks_by_priority,
        filter_tasks_by_category,
        search_tasks,
        filter_tasks_by_completion
    )

from hypothesis import given, strategies as st
from tasks import (
    generate_unique_id,
    filter_tasks_by_priority,
    filter_tasks_by_category,
    search_tasks,
    filter_tasks_by_completion
)

@given(st.lists(
    st.fixed_dictionaries({"id": st.integers(min_value=1)})
))
def test_generate_unique_id_is_unique(task_list):
    ids = [task["id"] for task in task_list]
    new_id = generate_unique_id(task_list)
    assert new_id not in ids

@given(st.text(), st.text())
def test_search_tasks_finds_title_or_description(title, desc):
    tasks = [{"title": title, "description": desc}]
    assert len(search_tasks(tasks, title)) >= 1 or len(search_tasks(tasks, desc)) >= 1

@given(
    st.lists(
        st.fixed_dictionaries({
            "priority": st.sampled_from(["High", "Medium", "Low"])
        })
    ),
    st.sampled_from(["High", "Medium", "Low"])
)
def test_filter_tasks_by_priority_valid(tasks, level):
    result = filter_tasks_by_priority(tasks, level)
    assert all(task["priority"] == level for task in result)

@given(
    st.lists(
        st.fixed_dictionaries({
            "category": st.text()
        })
    ),
    st.text()
)
def test_filter_tasks_by_category_valid(tasks, category):
    result = filter_tasks_by_category(tasks, category)
    assert all(task["category"] == category for task in result)

@given(
    st.lists(
        st.fixed_dictionaries({
            "completed": st.booleans()
        })
    )
)
def test_filter_tasks_by_completion_valid(tasks):
    completed = filter_tasks_by_completion(tasks, True)
    not_completed = filter_tasks_by_completion(tasks, False)
    assert all(task["completed"] for task in completed)
    assert all(not task["completed"] for task in not_completed)
