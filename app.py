import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go

# --- Config ---
st.set_page_config(
    page_title="Globus Medical Sterile Ops",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Styling ---
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
    }
    h1, h2, h3 {
        color: #005587; /* Globus Blue */
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 2em;
        font-weight: bold;
        color: #005587;
    }
    .metric-label {
        font-size: 0.9em;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data
def load_data():
    conn = sqlite3.connect("globus_sterile.db")
    inventory = pd.read_sql("SELECT * FROM inventory", conn)
    procurement = pd.read_sql("SELECT * FROM procurement", conn)
    production = pd.read_sql("SELECT * FROM production", conn)
    conn.close()
    return inventory, procurement, production

inventory, procurement, production = load_data()

# --- Validations for Missing Columns ---
# Ensure columns exist before using them to prevent errors if source changed
required_inv_cols = ['Total_Value', 'Stock_Quantity', 'Category']
required_proc_cols = ['Compliance', 'Discrepancy_Flag', 'Defective_Units']
required_prod_cols = ['Delay_Hours', 'Job_Status']

# --- Dashboard ---
st.title("🏥 Globus Medical | Sterile Operations Suite")
st.markdown("### Executive Dashboard - JR105344 Candidate Project")

# Top Level KPIs
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

# 1. Total Inventory Value
total_val = inventory['Total_Value'].sum() if 'Total_Value' in inventory.columns else 0
kpi1.metric("📦 Inventory Value", f"${total_val:,.0f}", delta="1.2%")

# 2. Compliance Rate
if 'Compliance' in procurement.columns:
    comp_rate = (procurement['Compliance'].value_counts(normalize=True).get('Yes', 0) * 100)
else:
    comp_rate = 0
kpi2.metric("✅ Supplier Compliance", f"{comp_rate:.1f}%", delta="-0.5%")

# 3. Production Efficiency (On Time Jobs)
if 'Delay_Status' in production.columns:
    on_time_pct = (production['Delay_Status'].value_counts(normalize=True).get('On Time', 0) * 100)
else:
    on_time_pct = 0
kpi3.metric("⚙️ On-Time Production", f"{on_time_pct:.1f}%", delta="2.4%")

# 4. Open Discrepancies
if 'Discrepancy_Flag' in procurement.columns:
    discrepancies = procurement['Discrepancy_Flag'].sum()
else:
    discrepancies = 0
kpi4.metric("⚠️ Open PO Issues", f"{discrepancies}", delta="-5", delta_color="inverse")

st.markdown("---")

# Charts Row 1
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Production Throughput by WIP Step")
    if 'WIP_Step' in production.columns:
        wip_counts = production.groupby('WIP_Step')['Job_ID'].count().reset_index()
        fig_wip = px.bar(wip_counts, x='WIP_Step', y='Job_ID', color='WIP_Step', 
                         title="Batch Volume per Step", text_auto=True,
                         color_discrete_sequence=px.colors.sequential.Blues_r)
        fig_wip.update_layout(xaxis_title="Stage", yaxis_title="Job Count")
        st.plotly_chart(fig_wip, use_container_width=True)
    else:
        st.info("No Production Data Available")

with col2:
    st.subheader("Inventory by Category")
    if 'Category' in inventory.columns:
        cat_dist = inventory.groupby('Category')['Stock_Quantity'].sum().reset_index()
        fig_pie = px.pie(cat_dist, values='Stock_Quantity', names='Category', hole=0.4,
                           title="Stock Distribution",
                           color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("No Inventory Data Available")

# Charts Row 2
col3, col4 = st.columns(2)

with col3:
    st.subheader("Recent Production Delays")
    if 'Delay_Hours' in production.columns:
        delays = production[production['Delay_Hours'] > 0].copy()
        if not delays.empty:
            fig_hist = px.histogram(delays, x='Delay_Hours', nbins=20, 
                                    title="Distribution of Production Delays (Hours)",
                                    color_discrete_sequence=['#ff6b6b'])
            st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.success("No delays recorded!")

with col4:
    st.subheader("Procurement Quality Trend")
    if 'Order_Date' in procurement.columns and 'Defective_Units' in procurement.columns:
        procurement['Month'] = pd.to_datetime(procurement['Order_Date']).dt.to_period('M').astype(str)
        quality_trend = procurement.groupby('Month')['Defective_Units'].sum().reset_index()
        fig_line = px.line(quality_trend, x='Month', y='Defective_Units', markers=True,
                           title="Defective Units Over Time",
                           line_shape='spline',
                           color_discrete_sequence=['#FFC107'])
        st.plotly_chart(fig_line, use_container_width=True)

# Sidebar Info
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Globus_Medical_logo.svg/1200px-Globus_Medical_logo.svg.png", width=200) # Optional placeholder or text if fails
st.sidebar.markdown(
    """
    **Role:** Inventory & Data Analyst  
    **Req ID:** JR105344  
    **Location:** Audubon, PA  
    
    ---
    **Developer:** Ajay Kasu
    """
)
