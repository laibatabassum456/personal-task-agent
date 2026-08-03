import streamlit as st
import subprocess
import sys

st.set_page_config(
    page_title="AI Personal Task Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Personal Task Agent")
st.write("Manage your tasks using natural language.")

user_input = st.text_input(
    "Enter your command",
    placeholder="Example: Add a high priority task called Study AI"
)

if st.button("Send"):

    if user_input.strip():

        with st.spinner("Thinking..."):

            result = subprocess.run(
                [sys.executable, "Backend/agent.py", user_input],
                capture_output=True,
                text=True,
                encoding="utf-8"
            )

        st.subheader("Assistant")

        st.code(result.stdout)

        if result.stderr:
            st.error(result.stderr)