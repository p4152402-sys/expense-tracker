import streamlit as st
import pandas as pd

st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="centered")

# Custom CSS
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

# Store data
if "data" not in st.session_state:
    st.session_state.data = []

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
        st.session_state.data.append({
            "Amount": amount,
            "Category": category,
            "Date": str(date),
            "Description": desc
        })

df = pd.DataFrame(st.session_state.data)

st.markdown("---")
st.subheader("📊 Dashboard")

if not df.empty:
    # Total
    total = df["Amount"].sum()
    st.metric("Total Expense", f"₹ {total}")

    # Filter
    filter_cat = st.selectbox("Filter", ["All", "Food", "Travel", "Shopping", "Other"])
    if filter_cat != "All":
        df = df[df["Category"] == filter_cat]

    # Table
    st.dataframe(df, use_container_width=True)

    # 📊 Charts Section
    st.subheader("📈 Insights")

    # Category-wise sum
    cat_data = df.groupby("Category")["Amount"].sum()

    st.write("Category-wise Expenses")
    st.bar_chart(cat_data)

    st.write("Expense Distribution")
    st.line_chart(cat_data)

    # Download
    st.download_button("📥 Download Report", df.to_csv(index=False), "expenses.csv")

else:
    st.info("No expenses added yet")