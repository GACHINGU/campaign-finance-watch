import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data

st.set_page_config(page_title="Campaign Finance Watch", layout="wide")

st.title("Campaign Finance Watch Tool Prototype")

# Load data
df = load_data()

# -------------------------
# Sidebar Filters
# -------------------------
st.sidebar.header("Filters")

selected_party = st.sidebar.multiselect(
    "Select Party",
    options=df["party"].unique(),
    default=df["party"].unique()
)

selected_region = st.sidebar.multiselect(
    "Select Region",
    options=df["region"].unique(),
    default=df["region"].unique()
)

filtered_df = df[
    (df["party"].isin(selected_party)) &
    (df["region"].isin(selected_region))
]

# -------------------------
# KPIs
# -------------------------
total_spending = filtered_df["amount"].sum()
total_donors = filtered_df["donor"].nunique()

col1, col2 = st.columns(2)

col1.metric("Total Spending (KES)", f"{total_spending:,.0f}")
col2.metric("Unique Donors", total_donors)

# -------------------------
# Spending Over Time
# -------------------------
st.subheader("Spending Over Time")

trend = filtered_df.groupby("date")["amount"].sum().reset_index()

fig1 = px.line(trend, x="date", y="amount", markers=True)
st.plotly_chart(fig1, use_container_width=True)

# -------------------------
# Top Donors
# -------------------------
st.subheader("Top Donors")

top_donors = (
    filtered_df.groupby("donor")["amount"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig2 = px.bar(top_donors, x="donor", y="amount")
st.plotly_chart(fig2, use_container_width=True)

# -------------------------
# Party Comparison
# -------------------------
st.subheader("Party Funding Comparison")

party_totals = (
    filtered_df.groupby("party")["amount"]
    .sum()
    .reset_index()
)

fig3 = px.bar(party_totals, x="party", y="amount")
st.plotly_chart(fig3, use_container_width=True)