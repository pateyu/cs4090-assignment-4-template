Feature: To-Do Task Management

  Scenario: Add a new task
    Given the task list is empty
    When I add a task with title "Buy groceries"
    Then the task list should contain 1 task

  Scenario: Task should include a priority
    Given the task list is empty
    When I add a task with priority "High"
    Then the task should have priority "High"

  Scenario: Task should include a category
    Given the task list is empty
    When I add a task with category "Personal"
    Then the task should be categorized as "Personal"

  Scenario: Mark a task as completed
    Given there is a task titled "Workout"
    When I mark the task as completed
    Then the task should be marked completed

  Scenario: Filter tasks by category
    Given there are tasks in multiple categories
    When I filter tasks by category "School"
    Then I should see only tasks in the "School" category


