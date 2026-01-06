import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="Inventory Master", page_icon="📦", layout="wide")

st.title("📦 Inventory Master & Warehouse")

conn = sqlite3.connect("globus_sterile.db")
df = pd.read_sql("SELECT * FROM inventory", conn)
conn.close()

# Summary Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Items", len(df))
col2.metric("Total Value", f"${df['Total_Value'].sum():,.2f}")
reorder_count = len(df[df['Reorder_Status'] == 'Reorder Now'])
col3.metric("Items to Reorder", reorder_count, delta=f"-{reorder_count}", delta_color="inverse")

# Reorder List
if reorder_count > 0:
    st.warning("⚠️ CRITICAL: The following items are below reorder point (30% of stock)")
    reorder_list = df[df['Reorder_Status'] == 'Reorder Now']
    st.dataframe(reorder_list[['Part_ID', 'Description', 'Stock_Quantity', 'Reorder_Point', 'Supplier', 'Bin_Location']], use_container_width=True)

# ABC Analysis
st.subheader("ABC Analysis (Pareto Principle)")
df_sorted = df.sort_values('Total_Value', ascending=False)
df_sorted['Cumulative_Value'] = df_sorted['Total_Value'].cumsum()
df_sorted['Cumulative_Percent'] = 100 * df_sorted['Cumulative_Value'] / df_sorted['Total_Value'].sum()

def get_abc_class(x):
    if x <= 80: return 'A'
    elif x <= 95: return 'B'
    else: return 'C'

df_sorted['ABC_Class'] = df_sorted['Cumulative_Percent'].apply(get_abc_class)

fig_abc = px.scatter(df_sorted, x='Stock_Quantity', y='Total_Value', color='ABC_Class', 
                     hover_data=['Part_ID', 'Description'], log_x=True, log_y=True,
                     title="Inventory ABC Classification (Value vs Quantity)",
                     color_discrete_map={'A': 'red', 'B': 'orange', 'C': 'green'})
st.plotly_chart(fig_abc, use_container_width=True)

# Warehouse View
st.subheader("Warehouse Layout View")
if 'Bin_Location' in df.columns:
    # Just a simple treemap to simulate warehouse bins
    df_tree = df[df['Stock_Quantity'] > 0]
    fig_tree = px.treemap(df_tree, path=['Bin_Location', 'Part_ID'], values='Stock_Quantity',
                          title="Warehouse Stock by Bin Location", color='Stock_Quantity', color_continuous_scale='Blues')
    st.plotly_chart(fig_tree, use_container_width=True)
