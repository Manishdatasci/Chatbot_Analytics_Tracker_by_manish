import streamlit as st
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt

# For CSV path
CSV_FILE = "chat_logs.csv"

# For creating CSV with columns if it doesn't exist
if not os.path.exists(CSV_FILE):
    df_init = pd.DataFrame(columns=["timestamp", "user_id", "query", "topic", "rating"])
    df_init.to_csv(CSV_FILE, index=False)

# For loading data
df = pd.read_csv(CSV_FILE)

# --- Sidebar: for adding New Entry ---
st.sidebar.title("➕ Add Chat Log Entry")

with st.sidebar.form("log_form"):
    user_id = st.text_input("User ID")
    query = st.text_area("Query")
    topic = st.text_input("Topic")
    rating = st.slider("Rating (1 to 5)", 1, 5)
    submitted = st.form_submit_button("Submit")

    if submitted:
        if user_id and query and topic:
            new_entry = pd.DataFrame([{
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "user_id": user_id,
                "query": query,
                "topic": topic,
                "rating": rating
            }])
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv(CSV_FILE, index=False)
            st.success("✅ Entry successfully added!")
        else:
            st.warning("⚠️ Please fill in all fields before submitting.")

# --- For Main Dashboard ---
st.title("📊 Chatbot Analytics Dashboard")

# For showing columns
st.subheader("📄 CSV Columns:")
st.json({i: col for i, col in enumerate(df.columns)})

# Total Queries
st.metric("📥 Total Queries", len(df))

# Average Rating
if not df.empty and "rating" in df:
    avg_rating = round(df["rating"].mean(), 2)
    st.metric("⭐ Average Rating", avg_rating)
else:
    st.metric("⭐ Average Rating", "N/A")

# Most Asked Topics
if not df.empty and "topic" in df:
    topic_counts = df["topic"].value_counts()
    st.subheader("📌 Most Asked Topics")
    st.bar_chart(topic_counts)
else:
    st.subheader("📌 Most Asked Topics")
    st.write("No data yet.")

# Query Trend Over Time
if not df.empty and "timestamp" in df:
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])
    df['date'] = df['timestamp'].dt.date
    trend = df['date'].value_counts().sort_index()
    st.subheader("📈 Queries Over Time")
    st.line_chart(trend)
else:
    st.subheader("📈 Queries Over Time")
    st.write("No date data available.")

# Now for showing All Logs
st.subheader("📋 All Chat Logs")
st.dataframe(df[::-1])  # Latest first


# ---In Footer ---
st.markdown("---")
st.markdown("🛠️ Developed by **Manish Kumar **")
