import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="Compliance Monitor", page_icon="🛡️", layout="wide")

st.title("🛡️ FDA / AdvaMed Compliance Monitor")

conn = sqlite3.connect("globus_sterile.db")
procurement = pd.read_sql("SELECT * FROM procurement", conn)
production = pd.read_sql("SELECT * FROM production", conn)
conn.close()

# KPI Cards
col1, col2 = st.columns(2)

non_comp_pos = procurement[procurement['Compliance'] == 'No']
failed_jobs = production[production['Job_Status'] == 'Failed']

col1.metric("Non-Compliant POs", len(non_comp_pos), delta="Critical", delta_color="inverse")
col2.metric("Quarantined Lots (Failed)", len(failed_jobs), delta="Action Needed", delta_color="inverse")

# Report 1: Supplier Compliance
st.subheader("🚫 Non-Compliant Supplier Orders")
if not non_comp_pos.empty:
    st.dataframe(non_comp_pos[['PO_ID', 'Supplier', 'Date', 'Compliance', 'Defective_Units']], use_container_width=True)
else:
    st.success("100% Supplier Compliance Achieved!")

# Report 2: Production Quality / Quarantine
st.subheader("☣️ Quarantined / Failed Production Jobs")
if not failed_jobs.empty:
    st.dataframe(failed_jobs[['Job_ID', 'Part_ID', 'WIP_Step', 'Machine_ID', 'Job_Status']], use_container_width=True)
else:
    st.success("No Failed Jobs in Production.")

# Audit Trail (Mock)
st.subheader("📋 System Audit Trail (Last 5 Entries)")
audit_data = {
    "Timestamp": ["2026-01-05 08:00:01", "2026-01-05 09:12:33", "2026-01-05 10:45:10", "2026-01-05 14:20:00", "2026-01-05 16:55:42"],
    "User": ["System", "J.Doe", "Admin", "System", "A.Kasu"],
    "Action": ["Batch Schedule Update", "Inv Adjustment", "User Access Revoke", "PO Sync", "Report Gen"],
    "Status": ["Success", "Success", "Success", "Success", "Success"]
}
st.table(pd.DataFrame(audit_data))
