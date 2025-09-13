# -------------------------------
# Water Intake Tracker 💧
 
# Input daily water intake.
 
# Show progress toward a goal (like 3L/day).
 
# Plot weekly hydration chart.
# -------------------------------

import streamlit as st
import matplotlib.pyplot as plt
import datetime

st.set_page_config(page_title="Water Intake Tracker", page_icon="💧", layout="centered")
st.title("💧 Water Intake Tracker")

# -------------------------------
# Config
# -------------------------------
DAILY_GOAL = 3.0  # Liters

# Initialize session state for weekly log
if "water_log" not in st.session_state:
    # Keep a dict: {date: liters}
    st.session_state.water_log = {}

# -------------------------------
# Input Section
# -------------------------------
today = datetime.date.today()
today_str = today.strftime("%Y-%m-%d")

st.subheader("🚰 Log Today’s Water Intake")
water_input = st.text_input("Enter water intake (liters)", key="water_input")

if st.button("Add Intake"):
    if not water_input:
        st.error("❌ Please enter today’s water intake.")
    else:
        try:
            liters = float(water_input)
            if liters <= 0:
                st.error("❌ Intake must be greater than 0.")
            else:
                # Save today's entry (overwrite if already entered)
                st.session_state.water_log[today_str] = liters
                st.success(f"✅ Logged {liters:.2f} L for {today_str}")
        except ValueError:
            st.error("❌ Please enter a valid number.")

# -------------------------------
# Show Today’s Progress
# -------------------------------
if today_str in st.session_state.water_log:
    today_intake = st.session_state.water_log[today_str]
    progress = min(today_intake / DAILY_GOAL, 1.0)

    st.subheader("📊 Today’s Progress")
    st.progress(progress)

    if today_intake < DAILY_GOAL * 0.5:
        st.warning(f"⚠️ You’ve logged {today_intake:.2f} L. Drink more to stay hydrated!")
    elif today_intake < DAILY_GOAL:
        st.info(f"💧 You’ve logged {today_intake:.2f} L. Almost there!")
    else:
        st.success(f"🎉 Goal reached! You’ve logged {today_intake:.2f} L. Great job!")

# -------------------------------
# Weekly Hydration Chart
# -------------------------------
st.subheader("📅 Weekly Hydration Chart")

# Collect last 7 days
dates = [(today - datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
intakes = [st.session_state.water_log.get(d, 0) for d in dates]

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(dates, intakes, color="skyblue", label="Water Intake (L)")
ax.axhline(DAILY_GOAL, color="green", linestyle="--", label=f"Goal ({DAILY_GOAL}L)")
ax.set_ylabel("Liters")
ax.set_xlabel("Date")
ax.set_title("Weekly Hydration")
ax.legend()
plt.xticks(rotation=45)

st.pyplot(fig)
