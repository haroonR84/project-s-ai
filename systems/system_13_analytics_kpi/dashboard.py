import streamlit as st
import pandas as pd

st.set_page_config(page_title="Customer Service Analytics")
st.title("📊 Customer Service Analytics Dashboard")

LOG_FILE = "conversation_logs.csv"

try:
    df = pd.read_csv(LOG_FILE)
except FileNotFoundError:
    st.warning("No conversation data found yet.")
    st.stop()

st.metric("Total Conversations", len(df))
st.metric("Escalations", len(df[df["action"] == "escalate"]))
st.metric("High Priority Issues", len(df[df["priority"] == "high"]))

st.subheader("Channel Distribution")
st.bar_chart(df["channel"].value_counts())

st.subheader("Knowledge vs General AI")
st.bar_chart(df["source"].value_counts())

st.subheader("Recent Conversations")
st.dataframe(df.tail(10))
