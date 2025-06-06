import streamlit as st
import pandas as pd
from datetime import date
from utils import load_data, load_medicine

st.set_page_config(page_title="My Life Dashboard", page_icon="🏠", layout="wide")

# -------------------------------------------------------------
# 1) Embed the Pokéball image (base64-encoded) as the dashboard background
# -------------------------------------------------------------
dashboard_bg_b64 = """
data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/... (full base64 string here)
"""

st.markdown(
    f"""
    <style>
    [data-testid="stApp"] {{
        background-image: url("{dashboard_bg_b64}");
        background-size: cover;
        background-attachment: fixed;
    }}
    .footer {{
        position: fixed;
        left: 0;
        bottom: 10px;
        width: 100%;
        text-align: center;
        font-weight: bold;
        color: white;
        font-size: 14px;
    }}
    .medications-table {{
        background: rgba(255, 255, 255, 0.8);
        border-radius: 8px;
        padding: 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------
# 2) Page Title & Instructions
# -------------------------------------------------------------
st.title("🏠 My Life Dashboard")
st.markdown(
    """
    Use the sidebar to navigate to different trackers.  
    Below is a calendar-style overview of your sleep, expenses, and tasks for this month, 
    along with any active medicine reminders.
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------
# 3) Footer Text
# -------------------------------------------------------------
st.markdown('<div class="footer">made with ❤️ by Team_pikachu</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# 4) Load All Data
# -------------------------------------------------------------
sleep_df, exp_df, todo_df = load_data()
med_df = load_medicine()

# -------------------------------------------------------------
# 5) Show Three KPI Cards (Sleep, Expenses, Tasks)
# -------------------------------------------------------------
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Sleep Logs", len(sleep_df))
    if not sleep_df.empty:
        st.metric("Avg Sleep (hrs)", f"{sleep_df['duration'].mean():.1f}")
with col2:
    paid_sum = exp_df[exp_df["status"] == "Paid"]["amount"].sum() if not exp_df.empty else 0.0
    pend_sum = exp_df[exp_df["status"] == "Pending"]["amount"].sum() if not exp_df.empty else 0.0
    st.metric("Total Paid", f"${paid_sum:,.2f}")
    st.metric("Pending", f"${pend_sum:,.2f}")
with col3:
    today = pd.Timestamp(date.today())
    tasks_today = len(todo_df[todo_df["date"] == today]) if not todo_df.empty else 0
    st.metric("Tasks Today", tasks_today)

# -------------------------------------------------------------
# 6) Calendar-Style Summary for Sleep, Expenses, Tasks
# -------------------------------------------------------------
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

st.dataframe(summary.set_index("date"), use_container_width=True, hide_index=False)

# -------------------------------------------------------------
# 7) Medicine Reminders Section
# -------------------------------------------------------------
if not med_df.empty:
    st.markdown("## 💊 Active Medicine Reminders")
    # Pivot table: rows = Medicine Category, columns = Time of Day, cell = Before/After Meal
    pivot = med_df.pivot(
        index="category",
        columns="time_of_day",
        values="sub_category",
        aggfunc=lambda x: ", ".join(x),
    ).fillna("")
    st.markdown('<div class="medications-table">', unsafe_allow_html=True)
    st.dataframe(pivot, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("No medicine reminders set yet. Go to the Medicine Tracker page to add one.")
