
import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, date, time, timedelta
from utils import load_data, save_sleep

st.set_page_config(page_title="Sleep Tracker", page_icon="😴")

# Background
st.markdown('\n<style>\n[data-testid="stApp"] {\n    background-image: url("https://images.unsplash.com/photo-1444703686981-a3abbc4d4fe3?auto=format&fit=cover&w=1920&q=80");\n    background-size: cover;\n    background-attachment: fixed;\n}\n</style>\n', unsafe_allow_html=True)

# Title with Pikachu
st.image("https://i.imgur.com/9NYeDKY.png", width=150)
st.title("😴 Sleep Tracker")

# Add new log
st.header("Add New Sleep Log")
col1, col2 = st.columns(2)
with col1:
    sleep_date = st.date_input("Date", value=date.today())
    start_time = st.time_input("Bed Time", value=time(23, 0))
with col2:
    end_time = st.time_input("Wake Time", value=time(7, 0))

if st.button("Add Log"):
    start_dt = datetime.combine(sleep_date, start_time)
    end_dt = datetime.combine(
        sleep_date + timedelta(days=1 if end_time < start_time else 0),
        end_time
    )
    save_sleep(start_dt, end_dt)
    st.success("Sleep log saved! Refresh to see the updated chart.")

# Line plot: day vs hours slept
sleep_df, _, _ = load_data()
if sleep_df.empty:
    st.info("No sleep data yet.")
else:
    st.subheader("Sleep Duration by Date")
    line_chart = alt.Chart(sleep_df).mark_line(point=True).encode(
        x=alt.X('date:T', title="Date"),
        y=alt.Y('duration:Q', title="Hours Slept"),
        tooltip=['date:T','duration:Q']
    ).properties(height=400)
    st.altair_chart(line_chart, use_container_width=True)

    st.dataframe(sleep_df.sort_values('date', ascending=False), use_container_width=True)
