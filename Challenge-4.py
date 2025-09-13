
# -------------------------------
# BMI Calculator 🏋️
 
# Inputs: height & weight.
 
# Output: BMI value + health category (Underweight/Normal/Overweight)
# -------------------------------


import streamlit as st
import pandas as pd

st.set_page_config(page_title="BMI Calculator", page_icon="🏋️", layout="centered")
st.title("🏋️ BMI Calculator")

# -------------------------------
# Inputs
# -------------------------------
height = st.text_input("Enter your height in cm")
weight = st.text_input("Enter your weight in kg")

# -------------------------------
# Calculate Button
# -------------------------------
if st.button("Calculate BMI"):
    # Validation: Empty inputs
    if not height or not weight:
        st.error("❌ Please enter both height and weight.")
    else:
        try:
            h = float(height)
            w = float(weight)

            # Validation: Non-positive values
            if h <= 0 or w <= 0:
                st.error("❌ Height and weight must be greater than 0.")
            else:
                # BMI formula (kg / m²)
                h_m = h / 100  # convert cm → m
                bmi = w / (h_m ** 2)

                # Health Category
                if bmi < 18.5:
                    category = "Underweight"
                    st.warning(f"⚠️ Your BMI is {bmi:.2f} → {category}")
                elif 18.5 <= bmi < 25:
                    category = "Normal"
                    st.success(f"✅ Your BMI is {bmi:.2f} → {category}")
                elif 25 <= bmi < 30:
                    category = "Overweight"
                    st.info(f"ℹ️ Your BMI is {bmi:.2f} → {category}")
                else:
                    category = "Obese"
                    st.error(f"❌ Your BMI is {bmi:.2f} → {category}")

                # -------------------------------
                # BMI Interpretation Table (WHO)
                # -------------------------------
                st.write("---")
                st.subheader("📊 BMI Classification (WHO Standard)")

                data = {
                    "BMI Range": ["< 18.5", "18.5 – 24.9", "25 – 29.9", "≥ 30"],
                    "Category": ["Underweight", "Normal", "Overweight", "Obese"]
                }
                df = pd.DataFrame(data)
                st.table(df)

        except ValueError:
            st.error("❌ Please enter valid numeric values for height and weight.")
