import streamlit as st
import subprocess
import sys
import json


st.set_page_config(
    page_title="AI Personal Task Agent",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 AI Personal Task Agent")
st.write("Manage your tasks using natural language.")


# ---------------------------
# Function to run AI Agent
# ---------------------------

def run_agent(command):

    result = subprocess.run(
        [
            sys.executable,
            "Backend/agent.py",
            command
        ],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )

    return result.stdout


# ---------------------------
# Load Tasks
# ---------------------------

def load_tasks():

    try:
        with open("Backend/tasks.json", "r") as file:
            return json.load(file)

    except:
        return []


# ---------------------------
# Menu
# ---------------------------

option = st.selectbox(
    "What do you want to do?",
    [
        "-- Select an option --",
        "➕ Add Task",
        "📋 View Tasks",
        "✅ Complete Task",
        "🗑 Delete Task",
        "🔍 Search Task"
    ]
)


# ---------------------------
# ADD TASK
# ---------------------------

# ---------------------------
# ADD TASK
# ---------------------------

if option == "-- Select an option --":

    st.info(
        "👋 Welcome! Please select an action from the menu above."
    )


elif option == "➕ Add Task":

    task = st.text_input(
        "Enter your task",
        placeholder="Example: Complete AI assignment tomorrow"
    )

    priority = st.selectbox(
        "Priority",
        [
            "High",
            "Medium",
            "Low"
        ]
    )


    if st.button("Create Task"):

        if task.strip():

            command = (
            f"Add {priority} priority task: {task}"
        )

        response = run_agent(command)

        st.subheader("Assistant")
        st.code(response)

    else:
        st.warning("Please enter a task first.")



# ---------------------------
# VIEW TASKS
# ---------------------------

elif option == "📋 View Tasks":

    st.subheader("📋 Your Tasks")

    tasks = load_tasks()


    if not tasks:

        st.info("No tasks found.")

    else:

        for task in tasks:

            st.container(border=True)

            st.markdown(
                f"### 📝 {task['task']}"
            )

            st.write(
                f"⭐ Priority: {task.get('priority','Medium')}"
            )

            st.write(
                f"Status: {task.get('status','Pending')}"
            )



# ---------------------------
# COMPLETE TASK
# ---------------------------

elif option == "✅ Complete Task":

    tasks = load_tasks()


    if tasks:

        selected = st.selectbox(
            "Select task",
            [
                t["task"]
                for t in tasks
            ]
        )


        if st.button("Complete"):

            response = run_agent(
                f"Complete task {selected}"
            )

            st.code(response)


    else:

        st.info("No tasks available.")



# ---------------------------
# DELETE TASK
# ---------------------------

elif option == "🗑 Delete Task":

    tasks = load_tasks()


    if tasks:

        selected = st.selectbox(
            "Select task",
            [
                t["task"]
                for t in tasks
            ]
        )


        if st.button("Delete"):

            response = run_agent(
                f"Delete task {selected}"
            )

            st.code(response)


    else:

        st.info("No tasks available.")



# ---------------------------
# SEARCH TASK
# ---------------------------

elif option == "🔍 Search Task":

    keyword = st.text_input(
        "Search keyword"
    )


    if st.button("Search"):

        response = run_agent(
            f"Search task {keyword}"
        )

        st.code(response)