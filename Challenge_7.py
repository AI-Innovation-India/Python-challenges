# -------------------------------
# Gym Workout Logger 🏋️
 
# Log exercises (sets, reps, weight).
 
# Store history in a table.
 
# Show weekly progress graph.
# -------------------------------

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime

st.set_page_config(page_title="Gym Workout Logger", page_icon="🏋️", layout="centered")
st.title("🏋️ Gym Workout Logger")

# -------------------------------
# Initialize session state
# -------------------------------
if "workout_log" not in st.session_state:
    st.session_state.workout_log = pd.DataFrame(columns=["Date", "Exercise", "Sets", "Reps", "Weight (kg)"])

# -------------------------------
# Input Form
# -------------------------------
st.subheader("➕ Log a New Workout")

exercise = st.text_input("Exercise name (e.g., Bench Press, Squats)")
sets = st.text_input("Number of sets")
reps = st.text_input("Number of reps per set")
weight = st.text_input("Weight used (kg)")

if st.button("Add Workout"):
    # Validation
    if not exercise or not sets or not reps or not weight:
        st.error("❌ Please fill in all fields.")
    else:
        try:
            sets_val = int(sets)
            reps_val = int(reps)
            weight_val = float(weight)

            if sets_val <= 0 or reps_val <= 0 or weight_val <= 0:
                st.error("❌ Sets, reps, and weight must be greater than 0.")
            else:
                today = datetime.date.today().strftime("%Y-%m-%d")
                new_entry = pd.DataFrame(
                    [[today, exercise.strip(), sets_val, reps_val, weight_val]],
                    columns=["Date", "Exercise", "Sets", "Reps", "Weight (kg)"]
                )
                st.session_state.workout_log = pd.concat([st.session_state.workout_log, new_entry], ignore_index=True)
                st.success(f"✅ Logged {sets_val} sets × {reps_val} reps of {exercise} ({weight_val} kg)")
        except ValueError:
            st.error("❌ Please enter valid numbers for sets, reps, and weight.")

# -------------------------------
# Workout History
# -------------------------------
st.subheader("📋 Workout History")

if not st.session_state.workout_log.empty:
    st.dataframe(st.session_state.workout_log, use_container_width=True)
else:
    st.info("ℹ️ No workouts logged yet.")

# -------------------------------
# Weekly Progress Graph
# -------------------------------
st.subheader("📈 Weekly Progress")

if not st.session_state.workout_log.empty:
    selected_exercise = st.selectbox("Select exercise to view progress", st.session_state.workout_log["Exercise"].unique())

    # Filter data for selected exercise
    df_ex = st.session_state.workout_log[st.session_state.workout_log["Exercise"] == selected_exercise]

    # Group by date → track average lifted weight
    df_progress = df_ex.groupby("Date")["Weight (kg)"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df_progress["Date"], df_progress["Weight (kg)"], marker="o", linestyle="-", color="blue")
    ax.set_title(f"Weekly Progress – {selected_exercise}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Average Weight (kg)")
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.info("ℹ️ Log some workouts to see progress.")
