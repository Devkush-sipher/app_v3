import streamlit as st
import pandas as pd
from datetime import date
from utils import load_data

# Page configuration
st.set_page_config(page_title="My Life Dashboard", page_icon="🏠", layout="wide")

# Pokéball background & footer CSS
st.markdown(
    """
    <style>
    [data-testid="stApp"] {
        background-image: url("https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png");
        background-size: cover;
        background-attachment: fixed;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 10px;
        width: 100%;
        text-align: center;
        font-weight: bold;
        color: white;
        font-size: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and instructions (no hyperlinks, just mention sidebar)
st.title("🏠 My Life Dashboard")
st.markdown(
    """
    Use the sidebar to navigate to different trackers.  
    Below is a calendar-style overview of your sleep, expenses, and tasks for this month.
    """,
    unsafe_allow_html=True
)

# Footer text
st.markdown('<div class="footer">made with &lt;3 by Team_pikachu</div>', unsafe_allow_html=True)

# Load data
sleep_df, exp_df, todo_df = load_data()

# Show three KPI cards at the top
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Sleep Logs", len(sleep_df))
    if not sleep_df.empty:
        avg_sleep = sleep_df["duration"].mean()
        st.metric("Avg Sleep (hrs)", f"{avg_sleep:.1f}")
with col2:
    paid_sum = exp_df[exp_df["status"] == "Paid"]["amount"].sum() if not exp_df.empty else 0.0
    pend_sum = exp_df[exp_df["status"] == "Pending"]["amount"].sum() if not exp_df.empty else 0.0
    st.metric("Total Paid", f"${paid_sum:,.2f}")
    st.metric("Pending", f"${pend_sum:,.2f}")
with col3:
    today = pd.Timestamp(date.today())
    tasks_today = len(todo_df[todo_df["date"] == today]) if not todo_df.empty else 0
    st.metric("Tasks Today", tasks_today)

# Build a 6-week (42-day) calendar-style summary for the current month
start_month = date.today().replace(day=1)
dates = pd.date_range(start_month, periods=42)
summary = pd.DataFrame({"date": dates})

summary["Sleep (hrs)"] = summary["date"].map(
    lambda d: sleep_df.loc[sleep_df["date"] == pd.Timestamp(d.date()), "duration"].sum()
)
summary["Expense ($)"] = summary["date"].map(
    lambda d: exp_df.loc[exp_df["date"] == pd.Timestamp(d.date()), "amount"].sum()
)
summary["Tasks"] = summary["date"].map(
    lambda d: len(todo_df.loc[todo_df["date"] == pd.Timestamp(d.date())])
)

st.dataframe(
    summary.set_index("date"),
    use_container_width=True,
    hide_index=False
)
