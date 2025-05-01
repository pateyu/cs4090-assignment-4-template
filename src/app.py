import streamlit as st
import pandas as pd
from datetime import datetime
import subprocess
from tasks import (
    load_tasks,
    save_tasks,
    filter_tasks_by_priority,
    filter_tasks_by_category,
    generate_unique_id
)

def main():
    st.title("To-Do Application")

    tasks = load_tasks()

    st.sidebar.header("Add New Task")
    with st.sidebar.form("new_task_form"):
        task_title = st.text_input("Task Title")
        task_description = st.text_area("Description")
        task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        task_category = st.selectbox("Category", ["Work", "Personal", "School", "Other"])
        task_due_date = st.date_input("Due Date")
        submit_button = st.form_submit_button("Add Task")

        if submit_button and task_title.strip():
            new_task = {
                "id": generate_unique_id(tasks),
                "title": task_title,
                "description": task_description,
                "priority": task_priority,
                "category": task_category,
                "due_date": task_due_date.strftime("%Y-%m-%d"),
                "completed": False,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            tasks.append(new_task)
            save_tasks(tasks)
            st.sidebar.success("Task added successfully!")
        elif submit_button:
            st.sidebar.error("Task title cannot be empty or just spaces.")

    st.header("Your Tasks")
    col1, col2 = st.columns(2)
    with col1:
        filter_category = st.selectbox(
            "Filter by Category",
            ["All"] + list(set([task.get("category", "Other") for task in tasks]))
        )
    with col2:
        filter_priority = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])

    show_completed = st.checkbox("Show Completed Tasks")

    filtered_tasks = tasks.copy()
    if filter_category != "All":
        filtered_tasks = filter_tasks_by_category(filtered_tasks, filter_category)
    if filter_priority != "All":
        filtered_tasks = filter_tasks_by_priority(filtered_tasks, filter_priority)
    if not show_completed:
        filtered_tasks = [task for task in filtered_tasks if not task.get("completed")]

    for task in filtered_tasks:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"~~**{task['title']}**~~" if task.get("completed") else f"**{task['title']}**")
            st.write(task.get("description", ""))
            st.caption(
                f"Due: {task.get('due_date')} | Priority: {task.get('priority')} | Category: {task.get('category', 'Other')}"
            )
        with col2:
            if st.button("Complete" if not task.get("completed") else "Undo", key=f"complete_{task['id']}"):
                for t in tasks:
                    if t["id"] == task["id"]:
                        t["completed"] = not t["completed"]
                        save_tasks(tasks)
                        st.rerun()
            if st.button("Delete", key=f"delete_{task['id']}"):
                tasks = [t for t in tasks if t["id"] != task["id"]]
                save_tasks(tasks)
                st.rerun()

    # Test Suite
    st.sidebar.header("Test Suite")

    if st.sidebar.button("Run Unit Tests"):
        result = subprocess.run(
            ["pytest", "../tests/test_basic.py"],
            capture_output=True,
            text=True
        )
        st.code(result.stdout)
        if result.returncode == 0:
            st.sidebar.success("✅ All unit tests passed!")
        else:
            st.sidebar.error("❌ Some tests failed.")

    if st.sidebar.button("Run Parameterization Test"):
        result = subprocess.run(
            ["pytest", "../tests/test_advanced.py", "-k", "test_filter_tasks_by_priority_param"],
            capture_output=True,
            text=True
        )
        st.code(result.stdout)

    if st.sidebar.button("Run Mocking Test"):
        result = subprocess.run(
            ["pytest", "../tests/test_advanced.py", "-k", "test_save_tasks_mock"],
            capture_output=True,
            text=True
        )
        st.code(result.stdout)

    if st.sidebar.button("Run Coverage Report"):
        result = subprocess.run(
            ["pytest", "../tests", "--cov=src.tasks", "--cov-report=term-missing"],
            capture_output=True,
            text=True
        )
        st.code(result.stdout)

    if st.sidebar.button("Generate HTML Report"):
        result = subprocess.run(
            ["pytest", "../tests", "--html=../reports/unit_test_report.html", "--self-contained-html"],
            capture_output=True,
            text=True
        )
        st.code(result.stdout)
        st.sidebar.success("✅ HTML report saved at: reports/unit_test_report.html")

    if st.sidebar.button("Run BDD Tests"):
        result = subprocess.run(
            ["pytest", "../tests/feature"],
            capture_output=True,
            text=True
        )
        st.code(result.stdout)
        if result.returncode == 0:
            st.sidebar.success("✅ All BDD tests passed!")
        else:
            st.sidebar.error("❌ Some BDD tests failed.")



if __name__ == "__main__":
    main()
