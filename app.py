import streamlit as st
import pandas as pd
import plotly.express as px
from db import init_db, fetch_metrics, log_interaction

# Initialize DB
init_db()

st.set_page_config(page_title="Chatbot Analytics Dashboard", layout="wide")
PASSWORD = "admin123"
password = st.text_input("Please enter the correct password to view the dashboard.", type="password")

if password != PASSWORD:
    st.warning("🔒 Access restricted. Please enter the correct password.")
    st.stop()

# Session flag for data refresh
if "data_refresh" not in st.session_state:
    st.session_state.data_refresh = True

if st.session_state.data_refresh:
    metrics = fetch_metrics()
    st.session_state.metrics = metrics
    st.session_state.data_refresh = False
else:
    metrics = st.session_state.metrics

# Dashboard UI
st.title("🤖 Chatbot Analytics Dashboard")
st.markdown("Monitor your chatbot's interactions and satisfaction levels")

col1, col2, col3 = st.columns(3)
col1.metric("Total Interactions", metrics["total_queries"])
col2.metric("Average Rating", f"{metrics['average_rating']:.2f}")
col3.metric("Unique Topics", len(metrics["most_common_topics"]))

st.subheader("📊 Topic Distribution")
topic_count = pd.DataFrame(metrics["most_common_topics"], columns=["Topic", "Count"])
fig1 = px.bar(topic_count, x='Topic', y='Count', color='Topic', height=400)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("📈 Satisfaction Over Time")
df = pd.DataFrame(metrics["raw_data"], columns=["timestamp", "rating"])
df['timestamp'] = pd.to_datetime(df['timestamp'])
fig2 = px.line(df, x='timestamp', y='rating', title='Satisfaction Trend', markers=True)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("📝 Log New Interaction")
with st.form("log_form"):
    new_topic = st.text_input("Conversation Topic")
    new_rating = st.slider("Satisfaction Rating", 0.0, 5.0, 3.0, step=0.1)
    submitted = st.form_submit_button("Log Interaction")
    if submitted:
        if new_topic.strip() == "":
            st.error("Please enter a valid topic.")
        else:
            log_interaction(new_topic.strip(), new_rating)
            st.success("Interaction logged successfully!")
            st.session_state.data_refresh = True
            st.rerun()

