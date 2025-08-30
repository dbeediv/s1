import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Load or initialize data
def load_data():
    try:
        return pd.read_csv("food_data.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Item", "ExpiryDate"])

def save_data(df):
    df.to_csv("food_data.csv", index=False)

st.title("🥗 Food Expiry Tracker")
st.write("Track your food items and get notified before they expire.")

# Load data
df = load_data()

# Add new food item
st.subheader("➕ Add New Item")
item = st.text_input("Food Item Name")
expiry = st.date_input("Expiry Date", min_value=datetime.today())

if st.button("Add Item"):
    if item:
        new_data = pd.DataFrame([[item, expiry]], columns=["Item", "ExpiryDate"])
        df = pd.concat([df, new_data], ignore_index=True)
        save_data(df)
        st.success(f"{item} added successfully!")
    else:
        st.warning("Please enter a food item name.")

# Show current items
st.subheader("📋 Your Food Items")
if not df.empty:
    df["ExpiryDate"] = pd.to_datetime(df["ExpiryDate"])
    st.dataframe(df)

    # Check for expiring soon
    st.subheader("⚠️ Items Expiring Soon")
    today = datetime.today()
    upcoming = df[df["ExpiryDate"] <= (today + timedelta(days=3))]
    if not upcoming.empty:
        for _, row in upcoming.iterrows():
            st.error(f"{row['Item']} is expiring on {row['ExpiryDate'].date()}!")
    else:
        st.info("No items expiring soon.")
else:
    st.info("No items added yet.")
