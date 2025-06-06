
import streamlit as st
import pandas as pd
import altair as alt
from datetime import date, timedelta
from utils import load_data, save_expense

st.set_page_config(page_title="Expense Tracker", page_icon="💰")

# Background
st.markdown('\n<style>\n[data-testid="stApp"] {\n    background-image: url("https://images.unsplash.com/photo-1526040652367-ac003a0475fe?auto=format&fit=cover&w=1920&q=80");\n    background-size: cover;\n    background-attachment: fixed;\n}\n</style>\n', unsafe_allow_html=True)

st.title("💰 Expense Tracker")

# Pre‑defined categories
default_categories = ["Food", "Rent", "Travel", "Entertainment", "Utilities", "Health", "Debt", "Other"]

st.header("Add Expense")
col1, col2, col3 = st.columns(3)
with col1:
    exp_date = st.date_input("Date", value=date.today())
    amount = st.number_input("Amount ($)", min_value=0.0, step=0.01, format="%.2f")
with col2:
    category_choice = st.selectbox("Choose Category", default_categories + ["--Add new--"])
    if category_choice == "--Add new--":
        category = st.text_input("New Category")
    else:
        category = category_choice
with col3:
    status = st.selectbox("Status", ["Paid", "Pending"])

if st.button("Add Expense"):
    if category and amount:
        save_expense(exp_date, amount, category, status)
        st.success("Expense saved! Refresh to see the update.")
    else:
        st.error("Please enter both amount and category.")

_, exp_df, _ = load_data()
st.subheader("Overview")
if exp_df.empty:
    st.info("No expenses recorded.")
else:
    # Pie chart (Paid only) by category
    st.write("### Spending Breakdown by Category (Paid)")
    paid_df = exp_df[exp_df['status']=="Paid"]
    if not paid_df.empty:
        pie = alt.Chart(paid_df).mark_arc().encode(
            theta='sum(amount):Q',
            color=alt.Color('category:N', legend=None),
            tooltip=['category:N','sum(amount):Q']
        ).properties(width=400, height=400)
        st.altair_chart(pie, use_container_width=False)

    st.write("### Detailed Log")
    st.dataframe(exp_df.sort_values('date', ascending=False), use_container_width=True)

    # Weekly spend (last 7 days)
    st.write("### Last 7 Days Spending")
    last_week_start = pd.Timestamp(date.today() - timedelta(days=6))
    last7 = exp_df[exp_df['date'] >= last_week_start]
    if not last7.empty:
        weekly_sum = last7.groupby('date')['amount'].sum().reset_index()
        bar = alt.Chart(weekly_sum).mark_bar().encode(
            x='date:T',
            y='amount:Q'
        ).properties(height=300)
        st.altair_chart(bar, use_container_width=True)
