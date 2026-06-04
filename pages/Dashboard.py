import streamlit as st

from utils.data_loader import load_activity

from utils.analytics import *

df = load_activity()

st.title("📊 Dashboard")

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Total Steps",
    total_steps(df)
)

col2.metric(
    "Average Steps",
    average_steps(df)
)

col3.metric(
    "Calories",
    total_calories(df)
)

col4.metric(
    "Avg Calories",
    average_calories(df)
)
