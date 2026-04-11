import streamlit as st
import pandas as pd

st.markdown("<h1 style='text-align: center;'>💰 Expense Tracker</h1>", unsafe_allow_html=True)

# Store data
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# Input section
st.subheader("Add Expense")

amount = st.number_input("Amount", min_value=0)
category = st.selectbox("Category", ["Food", "Travel", "Shopping", "Other"])
date = st.date_input("Date")
desc = st.text_input("Description")

if st.button("Add Expense"):
    st.session_state.expenses.append({
        "Amount": amount,
        "Category": category,
        "Date": date,
        "Description": desc
    })

# Convert to table
df = pd.DataFrame(st.session_state.expenses)

# Show data
st.subheader("Expense List")

if not df.empty:
    st.write(df)

    # Total
    total = df["Amount"].sum()
    st.subheader(f"Total Expense: ₹ {total}")

    # Filter
    filter_cat = st.selectbox("Filter", ["All", "Food", "Travel", "Shopping", "Other"])

    if filter_cat != "All":
        filtered_df = df[df["Category"] == filter_cat]
        st.write(filtered_df)

    # Download
    st.download_button("Download CSV", df.to_csv(index=False), "expenses.csv")

else:
    st.write("No expenses added yet.")