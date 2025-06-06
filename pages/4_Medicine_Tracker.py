
import streamlit as st
from datetime import date
from PIL import Image

st.set_page_config(page_title="Medicine Tracker", page_icon="💊")

# Background
st.markdown(
    '\n<style>\n[data-testid="stApp"] {\n    background-image: url("https://images.unsplash.com/photo-1580281657524-bee6ae02117d?auto=format&fit=cover&w=1920&q=80");\n    background-size: cover;\n    background-attachment: fixed;\n}\n</style>\n', 
    unsafe_allow_html=True
)

st.title("💊 Medicine Tracker")

st.header("Add Medicine Reminder")
category = st.text_input("Add a Category (e.g., Vitamin, Prescription)")
time_of_day = st.selectbox("Time to be Taken", ["Morning", "Afternoon", "Evening", "Night"])
sub_category = st.selectbox("Sub-Category", ["Before Meal", "After Meal"])

if st.button("Save Reminder"):
    st.success(f"Category: {category}, Time: {time_of_day}, Sub-Category: {sub_category} saved!")
