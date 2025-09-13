# -------------------------------
# Unit Converter 🔄
 
# Convert: currency, temperature, length, weight.
 
# Show results instantly.
# -------------------------------


import streamlit as st

st.set_page_config(page_title="Unit Converter", page_icon="🔄", layout="centered")
st.title("🔄 Unit Converter")

# -------------------------------
# Converter Type Selection
# -------------------------------
converter_type = st.selectbox(
    "Choose conversion type",
    ["Currency", "Temperature", "Length", "Weight"]
)

# -------------------------------
# Currency Conversion (Static Rates Example)
# -------------------------------
if converter_type == "Currency":
    st.subheader("💱 Currency Converter")
    amount = st.text_input("Enter amount")

    from_currency = st.selectbox("From", ["USD", "EUR", "INR", "GBP"])
    to_currency = st.selectbox("To", ["USD", "EUR", "INR", "GBP"])

    # Fixed exchange rates for demo (can be replaced with API)
    rates = {
        "USD": 1,
        "EUR": 0.92,
        "INR": 83.0,
        "GBP": 0.79
    }

    if amount:
        try:
            amt = float(amount)
            if amt < 0:
                st.error("❌ Amount must be non-negative.")
            else:
                result = amt / rates[from_currency] * rates[to_currency]
                st.metric(label="Converted Amount", value=f"{result:.2f} {to_currency}", delta="Live")
        except ValueError:
            st.error("❌ Please enter a valid number.")

# -------------------------------
# Temperature Conversion
# -------------------------------
elif converter_type == "Temperature":
    st.subheader("🌡️ Temperature Converter")
    temp = st.text_input("Enter temperature")

    from_unit = st.selectbox("From", ["Celsius", "Fahrenheit", "Kelvin"])
    to_unit = st.selectbox("To", ["Celsius", "Fahrenheit", "Kelvin"])

    if temp:
        try:
            t = float(temp)
            result = None

            # Convert to Celsius first
            if from_unit == "Celsius":
                c = t
            elif from_unit == "Fahrenheit":
                c = (t - 32) * 5/9
            elif from_unit == "Kelvin":
                c = t - 273.15

            # Convert Celsius to target
            if to_unit == "Celsius":
                result = c
            elif to_unit == "Fahrenheit":
                result = c * 9/5 + 32
            elif to_unit == "Kelvin":
                result = c + 273.15

            st.metric(label="Converted Temperature", value=f"{result:.2f} {to_unit}", delta="Live")

        except ValueError:
            st.error("❌ Please enter a valid number.")

# -------------------------------
# Length Conversion
# -------------------------------
elif converter_type == "Length":
    st.subheader("📏 Length Converter")
    length = st.text_input("Enter length")

    from_unit = st.selectbox("From", ["Meters", "Kilometers", "Miles", "Feet"])
    to_unit = st.selectbox("To", ["Meters", "Kilometers", "Miles", "Feet"])

    factors = {
        "Meters": 1,
        "Kilometers": 1000,
        "Miles": 1609.34,
        "Feet": 0.3048
    }

    if length:
        try:
            l = float(length)
            if l < 0:
                st.error("❌ Length must be non-negative.")
            else:
                result = l * factors[from_unit] / factors[to_unit]
                st.metric(label="Converted Length", value=f"{result:.2f} {to_unit}", delta="Live")
        except ValueError:
            st.error("❌ Please enter a valid number.")

# -------------------------------
# Weight Conversion
# -------------------------------
elif converter_type == "Weight":
    st.subheader("⚖️ Weight Converter")
    weight = st.text_input("Enter weight")

    from_unit = st.selectbox("From", ["Kilograms", "Grams", "Pounds", "Ounces"])
    to_unit = st.selectbox("To", ["Kilograms", "Grams", "Pounds", "Ounces"])

    factors = {
        "Kilograms": 1,
        "Grams": 0.001,
        "Pounds": 0.453592,
        "Ounces": 0.0283495
    }

    if weight:
        try:
            w = float(weight)
            if w < 0:
                st.error("❌ Weight must be non-negative.")
            else:
                result = w * factors[from_unit] / factors[to_unit]
                st.metric(label="Converted Weight", value=f"{result:.2f} {to_unit}", delta="Live")
        except ValueError:
            st.error("❌ Please enter a valid number.")
