import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, date, time, timedelta
from utils import load_data, save_sleep

st.set_page_config(page_title="Sleep Tracker", page_icon="😴")

# Background: (you can replace this URL with any preferred sleep-themed image)
st.markdown(
    """
    <style>
    [data-testid="stApp"] {
        background-image: url("https://images.unsplash.com/photo-1444703686981-a3abbc4d4fe3?auto=format&fit=cover&w=1920&q=80");
        background-size: cover;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.image("https://i.imgur.com/9NYeDKY.png", width=120)
st.title("😴 Sleep Tracker")

# Add new sleep log
st.header("Add New Sleep Log")
col1, col2 = st.columns(2)
with col1:
    sleep_date = st.date_input("Date", value=date.today())
    start_time = st.time_input("Bed Time", value=time(23, 0))
with col2:
    end_time = st.time_input("Wake Time", value=time(7, 0))

if st.button("Add Log"):
    start_dt = datetime.combine(sleep_date, start_time)
    # If user sets a wake time earlier than bed time, assume next day
    end_dt = datetime.combine(
        sleep_date + timedelta(days=1 if end_time < start_time else 0),
        end_time
    )
    save_sleep(start_dt, end_dt)
    st.success("Sleep log saved! Refresh to see the updated chart.")

# Fetch sleep data and plot
sleep_df, _, _ = load_data()
if sleep_df.empty:
    st.info("No sleep data yet. Add one above to see the chart.")
else:
    st.subheader("Sleep Duration by Date")
    # Line chart: day vs. hours slept
    line_chart = alt.Chart(sleep_df).mark_line(point=True).encode(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("duration:Q", title="Hours Slept"),
        tooltip=["date:T", "duration:Q"]
    ).properties(height=400)
    st.altair_chart(line_chart, use_container_width=True)

    st.dataframe(sleep_df.sort_values("date", ascending=False), use_container_width=True)
