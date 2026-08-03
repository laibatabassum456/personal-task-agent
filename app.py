import streamlit as st
import subprocess
import sys
import json
# ---------------------------
# Load Tasks Function
# ---------------------------

def load_tasks():

    try:
        with open("Backend/tasks.json", "r") as file:
            return json.load(file)

    except:
        return []

st.set_page_config(
    page_title="AI Personal Task Agent",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 AI Personal Task Agent")
st.write("Manage your tasks using natural language.")

# ---------------------------
# SIDEBAR DASHBOARD
# ---------------------------

tasks = load_tasks()

total_tasks = len(tasks)

completed_tasks = len(
    [
        t for t in tasks
        if t.get("status") == "Completed"
    ]
)

pending_tasks = total_tasks - completed_tasks

high_priority = len(
    [
        t for t in tasks
        if t.get("priority") == "High"
    ]
)


with st.sidebar:

    st.header("📊 Dashboard")

    st.metric(
        "📋 Total Tasks",
        total_tasks
    )

    st.metric(
        "⏳ Pending",
        pending_tasks
    )

    st.metric(
        "✅ Completed",
        completed_tasks
    )

    st.metric(
        "🔥 High Priority",
        high_priority
    )

progress = (
    completed_tasks / total_tasks
    if total_tasks > 0 else 0
)

st.sidebar.subheader("📈 Progress")

st.sidebar.progress(progress)

st.sidebar.write(
    f"{completed_tasks}/{total_tasks} Tasks Completed"
)


st.divider()

st.write(
        "AI Personal Task Agent"
    )

st.caption(
        "Powered by Groq + Streamlit"
    )
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
        ["High", "Medium", "Low"]
    )

    if st.button("Create Task"):

        if task.strip():

            command = f"Add {priority} priority task: {task}"

            response = run_agent(command)

            st.subheader("Assistant")
            st.code(response)

            # Refresh the page so the new task appears immediately
            st.rerun()

        else:
            st.warning("Please enter a task first.")



# ---------------------------
# VIEW TASKS
# ---------------------------

 # ---------------------------
# VIEW TASKS
# ---------------------------

elif option == "📋 View Tasks":

    st.subheader("📋 Your Tasks")

    tasks = load_tasks()

    if not tasks:
        st.info("🎯 No tasks yet! Add your first task.")

    else:

        # Filter
        filter_option = st.selectbox(
            "Filter Tasks",
            [
                "All",
                "Pending",
                "Completed",
                "High Priority"
            ]
        )

        filtered_tasks = tasks

        if filter_option == "Pending":
            filtered_tasks = [
                t for t in tasks
                if t.get("status") == "Pending"
            ]

        elif filter_option == "Completed":
            filtered_tasks = [
                t for t in tasks
                if t.get("status") == "Completed"
            ]

        elif filter_option == "High Priority":
            filtered_tasks = [
                t for t in tasks
                if t.get("priority") == "High"
            ]

        # Show every task
        for task in filtered_tasks:

            with st.container(border=True):

                st.markdown(f"### 📝 {task['task']}")

                col1, col2 = st.columns(2)

                with col1:
                    st.write(
                        f"⭐ Priority: {task.get('priority','Medium')}"
                    )

                    st.write(
                        f"📅 Due: {task.get('due_date','Not specified')}"
                    )

                with col2:

                    status = task.get("status","Pending")

                    if status == "Completed":
                        st.success("✅ Completed")
                    else:
                        st.warning("⏳ Pending")

                action_col1, action_col2 = st.columns(2)

                with action_col1:

                    if status != "Completed":

                        if st.button(
                            "✅ Complete",
                            key=f"complete_{task['task']}"
                        ):

                            run_agent(
                                f"Complete task {task['task']}"
                            )

                            st.rerun()

                with action_col2:

                    if st.button(
                        "🗑 Delete",
                        key=f"delete_{task['task']}"
                    ):

                        run_agent(
                            f"Delete task {task['task']}"
                        )

                        st.rerun()

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