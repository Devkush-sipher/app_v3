import streamlit as st
from datetime import date
from utils import load_data

st.set_page_config(page_title="Medicine Tracker", page_icon="💊")

# Background: (Pokemon Health Center–themed image)
st.markdown(
    """
    <style>
    [data-testid="stApp"] {
        background-image: url("https://images.unsplash.com/photo-1580281657524-bee6ae02117d?auto=format&fit=cover&w=1920&q=80");
        background-size: cover;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("💊 Medicine Tracker")

st.header("Add Medicine Reminder")
category = st.text_input("Add a Category (e.g., Vitamin, Prescription)")
time_of_day = st.selectbox("Time to be Taken", ["Morning", "Afternoon", "Evening", "Night"])
sub_category = st.selectbox("Sub-Category", ["Before Meal", "After Meal"])

if st.button("Save Reminder"):
    # For now, we’re simply showing a confirmation. 
    # You could extend this to save reminders to a CSV or database.
    st.success(f"Saved: {category} | {time_of_day} | {sub_category}")

# (Optional) Show existing reminders—here we just reload data, though no medicine CSV is implemented yet:
# _, exp_df, todo_df = load_data()
# st.write("### Existing Reminders (placeholder)")
# st.write("-- no stored reminders yet --")
