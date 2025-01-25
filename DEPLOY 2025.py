import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from forex_python.converter import CurrencyRates

# Initialize the app
st.set_page_config(page_title="Cross-Border Money Manager", layout="wide", initial_sidebar_state="expanded")
st.title("Cross-Border Money Manager")
st.subheader("Track accounts, manage budgets, and control your spending across borders.")

# Sidebar Inputs
st.sidebar.header("Inputs")

# Add accounts section
st.sidebar.subheader("Add New Account")
account_name = st.sidebar.text_input("Account Name")
account_balance = st.sidebar.number_input("Balance", min_value=0.0, value=0.0, step=0.01)
account_currency = st.sidebar.selectbox("Currency", ["USD", "EUR", "GBP", "JPY", "Others"])
if st.sidebar.button("Add Account"):
    st.session_state.setdefault("accounts", []).append({
        "Account Name": account_name,
        "Balance": account_balance,
        "Currency": account_currency
    })
    st.sidebar.success("Account added successfully!")

# Add budget section
st.sidebar.subheader("Set Monthly Budget")
budget_category = st.sidebar.text_input("Category (e.g., Rent, Food, etc.)")
budget_amount = st.sidebar.number_input("Amount", min_value=0.0, value=0.0, step=0.01)
if st.sidebar.button("Set Budget"):
    st.session_state.setdefault("budgets", []).append({
        "Category": budget_category,
        "Amount": budget_amount
    })
    st.sidebar.success("Budget set successfully!")

# Dashboard Layout
st.header("Dashboard")

# Initialize session states for accounts and budgets
if "accounts" not in st.session_state:
    st.session_state.accounts = []
if "budgets" not in st.session_state:
    st.session_state.budgets = []

# Currency conversion setup
currency_rates = CurrencyRates()
def convert_currency(amount, from_currency, to_currency="USD"):
    if from_currency == to_currency:
        return amount
    try:
        return currency_rates.convert(from_currency, to_currency, amount)
    except Exception as e:
        st.error(f"Currency conversion failed: {e}")
        return amount  # Fallback if conversion fails

# Accounts Overview
st.subheader("Accounts Overview")
accounts_df = pd.DataFrame(st.session_state.accounts)
if not accounts_df.empty:
    accounts_df["Converted Balance (USD)"] = accounts_df.apply(
        lambda row: convert_currency(row["Balance"], row["Currency"]) if pd.notnull(row["Balance"]) else 0, axis=1
    )
    st.dataframe(accounts_df)
else:
    st.write("No accounts added yet.")

# Budget Overview
st.subheader("Budget Overview")
budgets_df = pd.DataFrame(st.session_state.budgets)
if not budgets_df.empty:
    st.dataframe(budgets_df)
else:
    st.write("No budgets set yet.")

# Spending Breakdown Visualization
st.subheader("Spending Breakdown")
if not budgets_df.empty:
    fig, ax = plt.subplots()
    ax.pie(budgets_df["Amount"], labels=budgets_df["Category"], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    ax.set_title("Spending Breakdown by Category")
    st.pyplot(fig)
else:
    st.write("No data available for visualization.")

# Upcoming Bills (Placeholder)
st.subheader("Upcoming Bills")
st.write("Feature coming soon: Track your recurring payments here!")
