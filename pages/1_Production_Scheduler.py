import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="Production Scheduler", page_icon="🗓️", layout="wide")

st.title("🗓️ Production & Batch Scheduler")

# Load Data
conn = sqlite3.connect("globus_sterile.db")
df = pd.read_sql("SELECT * FROM production", conn)
conn.close()

# Filters
col1, col2 = st.columns(2)
with col1:
    machine_filter = st.multiselect("Machine ID", options=df['Machine_ID'].unique(), default=df['Machine_ID'].unique())
with col2:
    status_filter = st.multiselect("Job Status", options=df['Job_Status'].unique(), default=df['Job_Status'].unique())

filtered_df = df[df['Machine_ID'].isin(machine_filter) & df['Job_Status'].isin(status_filter)]

# Gantt Chart
st.subheader("Production Timeline")
if not filtered_df.empty:
    # Ensure dates are datetime
    filtered_df['Scheduled_Start'] = pd.to_datetime(filtered_df['Scheduled_Start'])
    filtered_df['Scheduled_End'] = pd.to_datetime(filtered_df['Scheduled_End'])
    
    fig = px.timeline(filtered_df, x_start="Scheduled_Start", x_end="Scheduled_End", 
                      y="Machine_ID", color="Job_Status",
                      hover_data=["Job_ID", "Operation_Type", "Part_ID"],
                      title="Gantt Chart: Machine Schedules",
                      color_discrete_sequence=px.colors.qualitative.Plotly)
    fig.update_yaxes(categoryorder="total ascending")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data matches the filters.")

# Batch Recommendations
st.subheader("⚡ Recommended Batches (Prioritized)")
st.markdown("Jobs with high priority due to stockouts or efficiency:")

# Simple logic: Pending jobs + High efficiency or Random priority
recommendations = df[df['Job_Status'] == 'Pending'].copy()
if not recommendations.empty:
    st.dataframe(recommendations[['Job_ID', 'Part_ID', 'Operation_Type', 'Scheduled_Start', 'Optimization_Category']], use_container_width=True)
else:
    st.info("No pending batches to schedule.")
