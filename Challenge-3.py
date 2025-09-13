
# -------------------------------
# Simple Calculator ➕➖✖️➗
 
# Inputs: two numbers + operation.
 
# Output: result.
# -------------------------------

import streamlit as st

st.set_page_config(page_title="Simple Calculator", page_icon="🧮", layout="centered")
st.title("🧮 Simple Calculator")

# -------------------------------
# Inputs
# -------------------------------
num1 = st.text_input("Enter first number")
num2 = st.text_input("Enter second number")

operation = st.selectbox("Select operation", ["➕ Addition", "➖ Subtraction", "✖️ Multiplication", "➗ Division"])

# -------------------------------
# Calculate Button
# -------------------------------
if st.button("Calculate"):
    # Validation: Empty input
    if not num1 or not num2:
        st.error("❌ Please enter both numbers.")
    else:
        try:
            a = float(num1)
            b = float(num2)

            result = None
            if operation.startswith("➕"):
                result = a + b
            elif operation.startswith("➖"):
                result = a - b
            elif operation.startswith("✖️"):
                result = a * b
            elif operation.startswith("➗"):
                if b == 0:
                    st.error("❌ Division by zero is not allowed.")
                else:
                    result = a / b
            else:
                st.error("❌ Invalid operation selected.")

            if result is not None:
                st.success(f"✅ Result: {result}")

        except ValueError:
            st.error("❌ Please enter valid numbers.")
