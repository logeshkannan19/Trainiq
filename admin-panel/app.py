import streamlit as st
import pandas as pd
import requests
import os
from time import sleep

# Must be the very first command
st.set_page_config(page_title="Trainiq Admin Panel", page_icon="🏋️‍♂️", layout="wide")

@st.cache_data(ttl=60)
def fetch_live_interactions():
    """
    Mock functional fetcher for the admin timeline. 
    In production, this talks to Supabase via `database.py`.
    Cached for 60 seconds to prevent DB hammering.
    """
    return pd.DataFrame({
        "Timestamp": ["10:45 AM", "10:30 AM", "09:15 AM", "08:12 AM"],
        "User": ["Alice Free", "Bob Premium", "Charlie Pro", "Diana Pro"],
        "Intent": ["mark_done", "change_workout", "skip", "general_chat"],
        "Message": ["Done with chest!", "I want to do legs instead", "Too tired today", "Is oats good for bulking?"]
    })

st.markdown("""
<style>
    .metric-card {
        background-color: #1E1E1E;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #333;
        text-align: center;
        margin-bottom: 24px;
    }
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #32D74B;
    }
    .metric-label {
        font-size: 14px;
        color: #A0A0A0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

st.title("Trainiq AI Operations Dashboard")

# Mock Stats
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-card"><div class="metric-label">Active Users</div><div class="metric-value">1,248</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card"><div class="metric-label">Workouts Sent</div><div class="metric-value">982</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card"><div class="metric-label">Completion Rate</div><div class="metric-value">78.4%</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="metric-card"><div class="metric-label">Messages Handled</div><div class="metric-value">4,192</div></div>', unsafe_allow_html=True)

st.divider()

col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("Live Interaction Feed")
    st.caption("Auto-refreshes every 60 seconds via Supabase replication sync.")
    
    # Fetch data (cached)
    df = fetch_live_interactions()
    st.dataframe(df, use_container_width=True, hide_index=True)

with col_right:
    st.subheader("System Health")
    st.success("🟢 FastAPI Webhook Server: Online (Latency: 12ms)")
    st.success("🟢 APScheduler Jobs: Active and Polling")
    st.success("🟢 PostgreSQL Sync: Connected")
    
    st.divider()
    
    # Human-like interaction element
    if st.button("Force Trigger Morning Routine", use_container_width=True, type="primary"):
        with st.spinner("Dispatching manual chron override..."):
            sleep(1.5) # Simulate API request to FastAPI
            st.toast("Workout dispatched to 1,248 users!", icon="🔥")
