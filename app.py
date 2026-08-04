import streamlit as st
import subprocess
import sys
import json
import datetime
import plotly.express as px


# ---------------------------
# Page Config
# ---------------------------

st.set_page_config(
    page_title="AI Personal Task Agent",
    page_icon="🤖",
    layout="wide"
)


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
# Task Statistics
# ---------------------------

def task_statistics(tasks):

    completed = 0
    pending = 0

    priority_count = {
        "High": 0,
        "Medium": 0,
        "Low": 0
    }

    for task in tasks:

        if task.get("status") == "Completed":
            completed += 1
        else:
            pending += 1

        priority = task.get(
            "priority",
            "Low"
        )

        if priority in priority_count:
            priority_count[priority] += 1

    return completed, pending, priority_count



# ---------------------------
# Run AI Agent
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
# Title
# ---------------------------

st.title(
    "🤖 AI Personal Task Agent"
)

st.caption(
    "Your intelligent productivity assistant powered by Groq AI"
)

st.write(
    "Manage your tasks using natural language."
)



# ---------------------------
# Load Data FIRST
# ---------------------------

tasks = load_tasks()

completed_chart, pending_chart, priority_chart = task_statistics(tasks)

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



# ---------------------------
# Sidebar Dashboard
# ---------------------------

with st.sidebar:

    st.header(
        "📊 Dashboard"
    )


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "📋 Total",
            total_tasks
        )

        st.metric(
            "⏳ Pending",
            pending_tasks
        )


    with col2:

        st.metric(
            "✅ Done",
            completed_tasks
        )

        st.metric(
            "🔥 High",
            high_priority
        )


    progress = (
        completed_tasks / total_tasks
        if total_tasks > 0 else 0
    )


    st.subheader(
        "📈 Progress"
    )


    st.progress(progress)

    st.write(
        f"{completed_tasks}/{total_tasks} Completed"
    )



# ---------------------------
# AI ASSISTANT
# ---------------------------

st.subheader(
    "💬 AI Assistant"
)


option = st.selectbox(
    "Choose an action",
    [
        "-- Select an option --",
        "➕ Add Task",
        "📋 View Tasks",
        "✅ Complete Task",
        "🗑 Delete Task",
        "🔍 Search Task"
    ],
    key="main_action"
)
# ---------------------------
# ADD TASK
# ---------------------------

if option == "-- Select an option --":

    st.info(
        "👋 Select an action from the menu above."
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
        ],
        key="add_priority"
    )


    due_date = st.date_input(
        "📅 Due Date",
        value=datetime.date.today(),
        min_value=datetime.date.today()
    )


    if st.button(
        "Create Task",
        key="create_task"
    ):

        if task.strip():

            command = (
                f"Add a {priority} priority task "
                f"'{task}' due on {due_date}"
            )


            response = run_agent(command)


            st.subheader(
                "🤖 AI Response"
            )


            with st.container(border=True):

                st.success(response)


            st.rerun()


        else:

            st.warning(
                "Please enter a task."
            )



# ---------------------------
# VIEW TASKS
# ---------------------------

elif option == "📋 View Tasks":

    st.subheader(
        "📋 Your Tasks"
    )


    tasks = load_tasks()


    if not tasks:

        st.info(
            "🎯 No tasks available."
        )


    else:

        filter_option = st.selectbox(
            "Filter Tasks",
            [
                "All",
                "Pending",
                "Completed",
                "High Priority"
            ],
            key="filter_tasks"
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



        for task in filtered_tasks:


            with st.container(border=True):

                st.markdown(
                    f"### 📝 {task['task']}"
                )


                st.write(
                    f"📅 Due: {task.get('due_date','Not specified')}"
                )


                priority = task.get(
                    "priority",
                    "Medium"
                )


                if priority == "High":

                    st.error(
                        "🔴 High Priority"
                    )


                elif priority == "Medium":

                    st.warning(
                        "🟡 Medium Priority"
                    )


                else:

                    st.success(
                        "🟢 Low Priority"
                    )


                status = task.get(
                    "status",
                    "Pending"
                )


                if status == "Completed":

                    st.success(
                        "✅ Completed"
                    )


                else:

                    st.warning(
                        "⏳ Pending"
                    )



                col1, col2 = st.columns(2)


                with col1:

                    if status != "Completed":

                        if st.button(
                            "✅ Complete",
                            key=f"complete_{task['id']}"
                        ):

                            run_agent(
                                f"Complete task {task['task']}"
                            )

                            st.rerun()



                with col2:

                    if st.button(
                        "🗑 Delete",
                        key=f"delete_{task['id']}"
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
            ],
            key="complete_select"
        )


        if st.button(
            "Complete Task",
            key="complete_btn"
        ):

            response = run_agent(
                f"Complete task {selected}"
            )

            st.success(response)

            st.rerun()


    else:

        st.info(
            "No tasks available."
        )



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
            ],
            key="delete_select"
        )


        if st.button(
            "Delete Task",
            key="delete_btn"
        ):

            response = run_agent(
                f"Delete task {selected}"
            )


            st.success(response)

            st.rerun()


    else:

        st.info(
            "No tasks available."
        )



# ---------------------------
# SEARCH TASK
# ---------------------------

elif option == "🔍 Search Task":

    keyword = st.text_input(
        "Search keyword"
    )


    if st.button(
        "Search",
        key="search_btn"
    ):

        response = run_agent(
            f"Search task {keyword}"
        )

        st.success(response)
# ---------------------------
# ANALYTICS DASHBOARD
# ---------------------------

st.divider()

st.subheader("📊 Task Analytics")


# Reload latest tasks
analytics_tasks = load_tasks()

completed_chart, pending_chart, priority_chart = task_statistics(
    analytics_tasks
)


# Completion chart

status_data = {
    "Status": [
        "Completed",
        "Pending"
    ],
    "Count": [
        completed_chart,
        pending_chart
    ]
}


fig = px.pie(
    status_data,
    names="Status",
    values="Count",
    title="Completion Status",
    hole=0.4
)



# Priority chart

priority_data = {
    "Priority": list(priority_chart.keys()),
    "Count": list(priority_chart.values())
}


fig2 = px.bar(
    priority_data,
    x="Priority",
    y="Count",
    title="Priority Levels"
)



col1, col2 = st.columns(2)


with col1:

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    st.plotly_chart(
        fig2,
        use_container_width=True
    )