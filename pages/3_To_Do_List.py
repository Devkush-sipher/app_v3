import streamlit as st
import pandas as pd
from datetime import date
from utils import load_data, save_task

st.set_page_config(page_title="To-Do List", page_icon="✅")

# Background: (you can replace this URL with any To-Do or productivity-themed image)
st.markdown(
    """
    <style>
    [data-testid="stApp"] {
        background-image: url("https://images.unsplash.com/photo-1521412644187-c49fa049e84d?auto=format&fit=cover&w=1920&q=80");
        background-size: cover;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("✅ To-Do List")

# Add new task
st.header("Add Task")
task_date = st.date_input("Date", value=date.today())
task_text = st.text_input("Task Description")
task_status = st.selectbox("Status", ["Pending", "In Progress", "Completed"])

if st.button("Add Task"):
    if task_text.strip() != "":
        save_task(task_date, task_text, task_status)
        st.success("Task added! Refresh to see updates.")
    else:
        st.error("Please enter a task description.")

# Fetch and display tasks
_, _, todo_df = load_data()
st.subheader("Tasks")
if todo_df.empty:
    st.info("No tasks yet.")
else:
    todo_df = todo_df.sort_values(["date", "status"])
    edited = st.data_editor(
        todo_df,
        num_rows="dynamic",
        use_container_width=True,
        key="todo_editor"
    )
    if st.button("Save Changes"):
        # Overwrite CSV with edited DataFrame
        edited.to_csv("data/todo.csv", index=False)
        st.success("Changes saved!")
