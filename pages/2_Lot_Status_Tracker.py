import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="Lot Status Tracker", page_icon="🏷️", layout="wide")

st.title("🏷️ Lot Status & WIP Tracker")

# Load Data
conn = sqlite3.connect("globus_sterile.db")
df = pd.read_sql("SELECT * FROM production", conn)
conn.close()

# KPI Row
st.markdown("### Process Bottlenecks")
cols = st.columns(len(df['WIP_Step'].unique()))
avg_times = df.groupby('WIP_Step')['Processing_Time'].mean().sort_values(ascending=False)

# Display avg processing time per step
for step, time_val in avg_times.items():
    st.metric(f"Avg Time: {step}", f"{time_val:.1f} mins")

# Heatmap: Job Count by Step and Status
st.subheader("WIP Heatmap Concentration")
heatmap_data = df.groupby(['WIP_Step', 'Job_Status']).size().reset_index(name='Count')
if not heatmap_data.empty:
    fig_heat = px.density_heatmap(heatmap_data, x="WIP_Step", y="Job_Status", z="Count", 
                                  title="Job Concentration (Step vs Status)",
                                  color_continuous_scale="Viridis", text_auto=True)
    st.plotly_chart(fig_heat, use_container_width=True)

# Detailed Lot Search
st.subheader("🔍 Trace Lot / Job")
search_id = st.text_input("Enter Job ID or Lot Number (Data is simulated)", "")
if search_id:
    result = df[df['Job_ID'].astype(str).str.contains(search_id, case=False)]
    if not result.empty:
        st.dataframe(result, use_container_width=True)
    else:
        st.warning("Lot ID not found.")
else:
    st.dataframe(df[['Job_ID', 'Part_ID', 'WIP_Step', 'Job_Status', 'Actual_Start', 'Actual_End', 'Delay_Status']], use_container_width=True)
