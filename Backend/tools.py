"""
The agent's toolbox.

Each tool is two things:
  1. A SCHEMA  -> what the model sees (name, description, parameters).
     The description is how the model decides WHEN to use the tool, so write it well.
  2. A FUNCTION -> the real code that runs when the model asks for that tool.

The schemas use the OpenAI-style "function" shape, because that's what Groq speaks
(and most other providers too). If you switch providers, the JSON schema inside
"parameters" usually stays exactly the same — only the wrapper changes.

TOOL_SCHEMAS is the menu handed to the model.
TOOL_FUNCTIONS maps a tool name to the function that does the work.
"""

import os
import datetime
import json
from groq import Groq
from dotenv import load_dotenv

import config

load_dotenv()

# One shared client for tools that need to call the model (e.g. research).
# Groq() reads GROQ_API_KEY from the environment — never pass a key here.
_client = Groq()







# ----------------------------------------------------
# ADD TASK TOOL
# ----------------------------------------------------

add_task_schema = {
    "type": "function",
    "function": {
        "name": "add_task",
        "description": "Add a new task to the user's task list.",
        "parameters": {
            "type": "object",
            "properties": {
                "task": {
                    "type": "string",
                    "description": "The task that the user wants to add."
                },
                "priority": {
                    "type": "string",
                    "description": "Task priority: High, Medium or Low."
                }
            },
            "required": ["task"]
        }
    }
}

view_tasks_schema = {
    "type": "function",
    "function": {
        "name": "view_tasks",
        "description": "Show all saved tasks.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
}
complete_task_schema = {
    "type": "function",
    "function": {
        "name": "complete_task",
        "description": "Mark a task as completed.",
        "parameters": {
            "type": "object",
            "properties": {
                "task": {
                    "type": "string",
                    "description": "Name of the task to mark as completed."
                }
            },
            "required": ["task"]
        }
    }
}
delete_task_schema = {
    "type": "function",
    "function": {
        "name": "delete_task",
        "description": "Delete a task from the task list.",
        "parameters": {
            "type": "object",
            "properties": {
                "task": {
                    "type": "string",
                    "description": "Name of the task to delete."
                }
            },
            "required": ["task"]
        }
    }
}

search_task_schema = {
    "type": "function",
    "function": {
        "name": "search_task",
        "description": "Search for tasks by keyword.",
        "parameters": {
            "type": "object",
            "properties": {
                "keyword": {
                    "type": "string",
                    "description": "Keyword to search in task names."
                }
            },
            "required": ["keyword"]
        }
    }
}

def add_task(task, priority="Medium"):

    file_name = "tasks.json"

    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            tasks = json.load(file)
    else:
        tasks = []

    tasks.append({
        "task": task,
        "priority": priority,
        "status": "Pending"
    })

    with open(file_name, "w") as file:
        json.dump(tasks, file, indent=4)

    return f"Task '{task}' added successfully."
def view_tasks():

    file_name = "tasks.json"

    if not os.path.exists(file_name):
        return "No tasks found."

    with open(file_name, "r") as file:
        tasks = json.load(file)

    if len(tasks) == 0:
        return "Your task list is empty."

    output = "📋 Your Tasks\n\n"

    for i, task in enumerate(tasks, start=1):
        output += (
            f"{i}. {task['task']}\n"
            f"Priority: {task['priority']}\n"
            f"Status: {task['status']}\n\n"
        )

    return output

def complete_task(task):

    file_name = "tasks.json"

    if not os.path.exists(file_name):
        return "No tasks found."

    with open(file_name, "r") as file:
        tasks = json.load(file)

    matches = []

    for item in tasks:
        if task.lower() in item["task"].lower():
            matches.append(item)

    if len(matches) == 1:
        matches[0]["status"] = "Completed"

        with open(file_name, "w") as file:
            json.dump(tasks, file, indent=4)

        return f"Task '{matches[0]['task']}' marked as completed."

    elif len(matches) > 1:
        return f"Multiple tasks found: {[m['task'] for m in matches]}"

    else:
        return f"Task '{task}' not found."
def delete_task(task):

    file_name = "tasks.json"

    if not os.path.exists(file_name):
        return "No tasks found."

    with open(file_name, "r") as file:
        tasks = json.load(file)

    updated_tasks = [t for t in tasks if t["task"].lower() != task.lower()]

    if len(updated_tasks) == len(tasks):
        return f"Task '{task}' not found."

    with open(file_name, "w") as file:
        json.dump(updated_tasks, file, indent=4)

    return f"Task '{task}' deleted successfully."
def search_task(keyword):

    file_name = "tasks.json"

    if not os.path.exists(file_name):
        return "No tasks found."

    with open(file_name, "r") as file:
        tasks = json.load(file)

    results = []

    for task in tasks:
        if keyword.lower() in task["task"].lower():
            results.append(task)

    if not results:
        return f"No tasks found containing '{keyword}'."

    output = "🔍 Matching Tasks\n\n"

    for i, task in enumerate(results, start=1):
        output += (
            f"{i}. {task['task']}\n"
            f"Priority: {task['priority']}\n"
            f"Status: {task['status']}\n\n"
        )

    return output

# ---------------------------------------------------------------------------
# Registries the agent uses.
# ---------------------------------------------------------------------------

TOOL_SCHEMAS = [
    add_task_schema,
    view_tasks_schema,
    complete_task_schema,
    delete_task_schema,
    search_task_schema,
]
TOOL_FUNCTIONS = {
    "add_task": add_task,
    "view_tasks": view_tasks,
    "complete_task": complete_task,
    "delete_task": delete_task,
    "search_task": search_task,
}