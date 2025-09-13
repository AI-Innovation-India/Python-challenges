# -------------------------------
# Scenario:
# Friends go out for dinner/trip and want to split expenses fairly.
 
# Task:
 
# User enters: total amount + number of people.
 
# Optionally, add each person’s name & contribution.
 
# App calculates how much each person should pay or get back.
# -------------------------------



import streamlit as st

st.set_page_config(page_title="Expense Splitter", page_icon="💸", layout="centered")
st.title("💸 Expense Splitter")

# -------------------------------
# Inputs: Total and Number of People
# -------------------------------
total_amount = st.number_input("Enter total amount (₹)", min_value=0.0, format="%.2f")
num_people = st.number_input("Enter number of people", min_value=1, step=1)

st.write("---")

# -------------------------------
# Optional Contributions
# -------------------------------
st.subheader("Optional: Enter each person's contribution")

contributions = []
for i in range(int(num_people)):
    col1, col2 = st.columns([2, 1])
    with col1:
        name = st.text_input(f"Name of person {i+1}", key=f"name_{i}")
    with col2:
        paid = st.number_input(f"Paid by {name if name else f'Person {i+1}'}", 
                               min_value=0.0, format="%.2f", key=f"paid_{i}")
    # fallback if name empty
    contributions.append((name.strip() if name else f"Person {i+1}", paid))

# -------------------------------
# Helper: Who Pays Whom Settlement
# -------------------------------
def calculate_settlement(contributions, equal_share):
    """Return a list of transactions (payer, receiver, amount)."""
    balances = {name: paid - equal_share for name, paid in contributions}
    debtors = [(n, -bal) for n, bal in balances.items() if bal < -1e-6]  # owes
    creditors = [(n, bal) for n, bal in balances.items() if bal > 1e-6]  # should receive

    settlement = []
    i, j = 0, 0
    while i < len(debtors) and j < len(creditors):
        debtor, owe_amt = debtors[i]
        creditor, recv_amt = creditors[j]

        transfer = min(owe_amt, recv_amt)
        settlement.append((debtor, creditor, transfer))

        # update balances
        debtors[i] = (debtor, owe_amt - transfer)
        creditors[j] = (creditor, recv_amt - transfer)

        # move pointers
        if debtors[i][1] <= 1e-6:  # settled
            i += 1
        if creditors[j][1] <= 1e-6:
            j += 1

    return settlement

# -------------------------------
# Calculate Button
# -------------------------------
if st.button("Calculate Split"):
    if total_amount <= 0:
        st.error("❌ Total amount must be greater than 0.")
    elif num_people <= 0:
        st.error("❌ Number of people must be at least 1.")
    else:
        equal_share = total_amount / num_people
        total_paid = sum(paid for _, paid in contributions)

        # -------------------------------
        # Validation: Contribution mismatch
        # -------------------------------
        if total_paid > 0 and abs(total_paid - total_amount) > 1e-6:
            st.warning(f"⚠️ Contributions entered (₹{total_paid:.2f}) do not match total amount (₹{total_amount:.2f}).")
            st.info("👉 Still showing settlement based on contributions entered.")

        # -------------------------------
        # Individual Results
        # -------------------------------
        st.subheader("📊 Individual Balances")
        for name, paid in contributions:
            balance = paid - equal_share
            if balance > 0:
                st.success(f"💰 {name} should get back ₹{balance:.2f}")
            elif balance < 0:
                st.error(f"❌ {name} should pay ₹{-balance:.2f} more")
            else:
                st.info(f"✅ {name} is settled up")

        # -------------------------------
        # Who Pays Whom Settlement
        # -------------------------------
        st.subheader("🤝 Final Settlement (Who pays whom)")
        settlement = calculate_settlement(contributions, equal_share)

        if not settlement:
            st.info("✅ Everyone is already settled!")
        else:
            for debtor, creditor, amount in settlement:
                st.write(f"➡️ {debtor} pays {creditor} **₹{amount:.2f}**")
