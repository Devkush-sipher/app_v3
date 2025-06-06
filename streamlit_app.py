
import streamlit as st
import pandas as pd
from datetime import date
from utils import load_data

st.set_page_config(page_title="My Life Dashboard", page_icon="🏠", layout="wide")

# Background Pokeball image and footer
st.markdown(
    '''
    <style>
    [data-testid="stApp"] {{
        background-image: url("https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png");
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
    }}
    </style>
    ''', unsafe_allow_html=True
)

st.title("🏠 My Life Dashboard")
st.markdown("Use the sidebar to navigate to different trackers.  
Below is a calendar‑style overview of your sleep, expenses and tasks for this month.")

# Footer text
st.markdown('<div class="footer">made with &lt;3 by Team_pikachu</div>', unsafe_allow_html=True)

sleep_df, exp_df, todo_df = load_data()

# KPI cards
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Sleep Logs", len(sleep_df))
    if not sleep_df.empty:
        st.metric("Avg Sleep (hrs)", f"{sleep_df['duration'].mean():.1f}")
with col2:
    st.metric("Total Paid", f"${{exp_df[exp_df['status']=='Paid']['amount'].sum():,.2f}}")
    st.metric("Pending", f"${{exp_df[exp_df['status']=='Pending']['amount'].sum():,.2f}}")
with col3:
    today = pd.Timestamp(date.today())
    st.metric("Tasks Today", len(todo_df[todo_df['date']==today]))

# Calendar‑style summary
start_month = date.today().replace(day=1)
dates = pd.date_range(start_month, periods=42)
summary = pd.DataFrame({'date': dates})
summary['Sleep (hrs)'] = summary['date'].map(
    lambda d: sleep_df[sleep_df['date']==pd.Timestamp(d.date())]['duration'].sum()
)
summary['Expense ($)'] = summary['date'].map(
    lambda d: exp_df[exp_df['date']==pd.Timestamp(d.date())]['amount'].sum()
)
summary['Tasks'] = summary['date'].map(
    lambda d: len(todo_df[todo_df['date']==pd.Timestamp(d.date())])
)

st.dataframe(
    summary.set_index('date'),
    use_container_width=True,
    hide_index=False
)
