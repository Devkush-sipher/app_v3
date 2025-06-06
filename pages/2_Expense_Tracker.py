import streamlit as st
import pandas as pd
import altair as alt
from datetime import date, timedelta
from utils import load_data, save_expense

st.set_page_config(page_title="Expense Tracker", page_icon="💰")

# Background: (you can replace this URL with any preferred expense-themed image)
st.markdown(
    """
    <style>
    [data-testid="stApp"] {
        background-image: url("https://images.unsplash.com/photo-1515165562835-cbc6a6b75bb0?auto=format&fit=cover&w=1920&q=80");
        background-size: cover;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("💰 Expense Tracker")

# Pre-defined categories (feel free to add more)
default_categories = ["Food", "Rent", "Travel", "Entertainment", "Utilities", "Health", "Debt", "Other"]

# Add new expense
st.header("Add New Expense")
col1, col2, col3 = st.columns(3)
with col1:
    exp_date = st.date_input("Date", value=date.today())
    amount = st.number_input("Amount ($)", min_value=0.0, step=0.01)
with col2:
    category = st.selectbox("Category", default_categories)
    status = st.selectbox("Status", ["Paid", "Pending"])
with col3:
    description = st.text_input("Description (optional)")

if st.button("Add Expense"):
    if amount > 0:
        save_expense(exp_date, amount, category, status)
        st.success("Expense saved! Refresh to see updates.")
    else:
        st.error("Enter a valid amount.")

# Fetch and display expense data
_, exp_df, _ = load_data()

if exp_df.empty:
    st.info("No expenses logged yet.")
else:
    st.write("### Detailed Log")
    st.dataframe(exp_df.sort_values("date", ascending=False), use_container_width=True)

    # Last 7 days spending
    st.write("### Last 7 Days Spending")
    last_week_start = pd.Timestamp(date.today() - timedelta(days=6))
    last7 = exp_df[exp_df["date"] >= last_week_start]
    if not last7.empty:
        weekly_sum = last7.groupby("date")["amount"].sum().reset_index()
        bar = alt.Chart(weekly_sum).mark_bar().encode(
            x="date:T",
            y="amount:Q",
            tooltip=["date:T", "amount:Q"]
        ).properties(height=300)
        st.altair_chart(bar, use_container_width=True)
    else:
        st.info("No expenses in the last 7 days.")
