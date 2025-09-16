import streamlit as st
import sqlite3
import pandas as pd

# Load data from SQLite
conn = sqlite3.connect("packets.db")
df = pd.read_sql_query("SELECT * FROM packets", conn)

# Dashboard layout
st.title("📡 Network Packet Dashboard")
st.dataframe(df)

# Protocol distribution
st.subheader("Protocol Distribution")
st.bar_chart(df['protocol'].value_counts())

