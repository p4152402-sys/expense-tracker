import streamlit as st
import pandas as pd
from auth import login, signup
from db import create_tables
from expenses import add_expense, get_expenses

st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="centered")


# Create DB tables
create_tables()

# Login state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ================= LOGIN / SIGNUP =================
if not st.session_state.logged_in:

    menu = ["Login", "Signup"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        st.title("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = login(username, password)

            if user:
                st.session_state.logged_in = True
                st.session_state.user_id = user[0]
                st.success("Logged in!")
                st.rerun()
            else:
                st.error("Invalid credentials")

    elif choice == "Signup":
        st.title("Create Account")

        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")

        if st.button("Signup"):
            signup(new_user, new_pass)
            st.success("Account created! Go to Login")

# ================= EXPENSE TRACKER =================
else:
    

    st.markdown("""
    <style>
    body {
        background-color: #f5f7fa;
    }
    h1 {
        text-align: center;
    }
    .stButton>button {
        background: linear-gradient(to right, #4CAF50, #2e7d32);
        color: white;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("💰 Expense Tracker")

    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # Store data
    

    # Input section
    col1, col2 = st.columns(2)

    with col1:
        amount = st.number_input("Amount", min_value=0)
        category = st.selectbox("Category", ["Food", "Travel", "Shopping", "Other"])

    with col2:
        date = st.date_input("Date")
        desc = st.text_input("Description")

    if st.button("➕ Add Expense"):
        if amount > 0:
            add_expense(st.session_state.user_id, amount, category, str(date), desc)
            st.success("Expense Added!")

    data = get_expenses(st.session_state.user_id)
    df = pd.DataFrame(data, columns=["Amount", "Category", "Date", "Description"])
    st.markdown("---")
    st.subheader("📊 Dashboard")

    if not df.empty:
        total = df["Amount"].sum()
        st.metric("Total Expense", f"₹ {total}")

        filter_cat = st.selectbox("Filter", ["All", "Food", "Travel", "Shopping", "Other"])
        if filter_cat != "All":
            df = df[df["Category"] == filter_cat]

        st.dataframe(df, use_container_width=True)

        st.subheader("📈 Insights")
        cat_data = df.groupby("Category")["Amount"].sum()

        st.write("Category-wise Expenses")
        st.bar_chart(cat_data)

        st.write("Expense Distribution")
        st.line_chart(cat_data)

        st.download_button("📥 Download Report", df.to_csv(index=False), "expenses.csv")

    else:
        st.info("No expenses added yet")