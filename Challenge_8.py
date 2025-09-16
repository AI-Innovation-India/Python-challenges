# -------------------------------
# Currency Converter 💱
 
# Convert between INR, USD, EUR, etc. (static rates).
 
# Simple dropdown + number input.
# -------------------------------


import streamlit as st

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Currency Converter", page_icon="💱", layout="centered")

# Add background image with CSS
page_bg = """
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1624953587687-ef0c0c0af2b6");
    background-size: cover;
    background-attachment: fixed;
}
.block-container {
    background-color: rgba(255, 255, 255, 0.85);
    padding: 2rem;
    border-radius: 15px;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

st.title("💱 Currency Converter")
st.write("Convert easily between INR, USD, EUR, GBP, and JPY (static rates).")

# -------------------------------
# Static Exchange Rates (relative to USD)
# -------------------------------
rates = {
    "USD": 1.0,
    "INR": 83.0,   # 1 USD = 83 INR
    "EUR": 0.92,   # 1 USD = 0.92 EUR
    "GBP": 0.79,   # 1 USD = 0.79 GBP
    "JPY": 147.0   # 1 USD = 147 JPY
}

currencies = list(rates.keys())

# -------------------------------
# User Input
# -------------------------------
st.subheader("🔢 Enter Conversion Details")

amount = st.text_input("Enter amount")
from_currency = st.selectbox("From Currency", currencies, index=0)
to_currency = st.selectbox("To Currency", currencies, index=1)

if st.button("Convert"):
    # Validation
    if not amount:
        st.error("❌ Please enter an amount.")
    else:
        try:
            amount_val = float(amount)
            if amount_val <= 0:
                st.error("❌ Amount must be greater than 0.")
            elif from_currency == to_currency:
                st.warning("⚠️ Both currencies are the same. Nothing to convert.")
            else:
                # Convert using USD as base
                usd_amount = amount_val / rates[from_currency]
                converted = usd_amount * rates[to_currency]
                st.success(f"✅ {amount_val:.2f} {from_currency} = {converted:.2f} {to_currency}")
        except ValueError:
            st.error("❌ Please enter a valid numeric amount.")
