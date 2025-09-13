# -------------------------------
# Scenario:
# Day 1 : Task: Build a small form that takes name, age (slider) and shows a greeting.
 
# Use only streamlit!
 
# Share the screenshots, Happy Learning guys🤍
# -------------------------------


import streamlit as st

st.title("Greeting Form 🎉")

# Create a form
with st.form("greeting_form"):
    name = st.text_input("Enter your name")
    age = st.slider("Select your age", 1, 100, 25)

    # Submit button
    submitted = st.form_submit_button("Submit")

    if submitted:
        st.success(f"Hello {name}! 👋 You are {age} years old.")