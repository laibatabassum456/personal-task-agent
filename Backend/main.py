from fastapi import FastAPI
from pydantic import BaseModel

from agent import run

from tools import (
    add_task,
    view_tasks,
    complete_task,
    delete_task
)


app = FastAPI(
    title="Personal Task Agent"
)


class UserRequest(BaseModel):
    message: str

# -------------------------
# Models
# -------------------------

class Task(BaseModel):
    task: str
    priority: str = "Medium"






# -------------------------
# Home
# -------------------------

@app.get("/")
def home():

    return {
        "message": "Personal Task Agent Running"
    }



# -------------------------
# AI Agent
# -------------------------

@app.post("/agent")
def ask_agent(data: UserRequest):
    try:
        response = run(data.message)
        return {
            "response": response
        }
    except Exception as e:
        return {
            "error": str(e)
        }

# -------------------------
# Add Task
# -------------------------

@app.post("/add")
def create_task(data: Task):

    result = add_task(
        data.task,
        data.priority
    )

    return {
        "result": result
    }



# -------------------------
# View Tasks
# -------------------------

@app.get("/tasks")
def get_tasks():

    tasks = view_tasks()

    return {
        "tasks": tasks
    }


# -------------------------
# Complete Task
# -------------------------

@app.put("/complete")
def finish_task(data: Task):

    result = complete_task(
        data.task
    )

    return {
        "result": result
    }



# -------------------------
# Delete Task
# -------------------------

@app.delete("/delete")
def remove_task(data: Task):

    result = delete_task(
        data.task
    )

    return {
        "result": result
    }
