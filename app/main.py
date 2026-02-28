import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data
from utils.risk_engine import calculate_hhi, detect_spike, classify_risk

st.set_page_config(page_title="Campaign Finance Watch", layout="wide")
st.title("Campaign Finance Watch Dashboard")

# -------------------------
# Load Data
# -------------------------
df = load_data()

# -------------------------
# Sidebar Filters
# -------------------------
st.sidebar.header("Filters")

# Party & Region
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

# Date range
st.sidebar.subheader("Date Range")
min_date = df["date"].min()
max_date = df["date"].max()
start_date, end_date = st.sidebar.date_input(
    "Select date range",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Donor filter
selected_donors = st.sidebar.multiselect(
    "Select Donors",
    options=df["donor"].unique(),
    default=df["donor"].unique()
)

# Apply filters
filtered_df = df[
    (df["party"].isin(selected_party)) &
    (df["region"].isin(selected_region)) &
    (df["donor"].isin(selected_donors)) &
    (df["date"] >= pd.to_datetime(start_date)) &
    (df["date"] <= pd.to_datetime(end_date))
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
# Risk Analysis
# -------------------------
hhi = calculate_hhi(filtered_df)
z_score = detect_spike(filtered_df)
risk_level = classify_risk(hhi, z_score)

st.subheader("⚠️ Risk Monitoring Panel")
col1, col2, col3 = st.columns(3)
col1.metric("Donor Concentration (HHI)", hhi)
col2.metric("Spending Spike (Z-score)", z_score)
col3.metric("Overall Risk Level", risk_level)

# -------------------------
# Risk Summary Text + Download
# -------------------------
st.subheader("Risk Summary")
summary_text = f"""
Campaign Risk Assessment:

- Donor Concentration (HHI): {hhi}
- Spending Spike (Z-score): {z_score}
- Overall Risk Level: {risk_level}

Interpretation:
Higher HHI indicates funding concentration among few donors.
Z-score above 2 suggests abnormal spending spike.
"""
st.text(summary_text)

st.download_button(
    label="Download Risk Report",
    data=summary_text,
    file_name="campaign_risk_report.txt",
    mime="text/plain"
)

# -------------------------
# Party-level Risk Table
# -------------------------
st.subheader("Party-level Risk Indicators")
party_risks = []
for party in filtered_df["party"].unique():
    df_party = filtered_df[filtered_df["party"] == party]
    hhi_party = calculate_hhi(df_party)
    z_party = detect_spike(df_party)
    risk_party = classify_risk(hhi_party, z_party)
    party_risks.append([party, hhi_party, z_party, risk_party])

party_risks_df = pd.DataFrame(party_risks, columns=["Party","HHI","Z-score","Risk Level"])
st.dataframe(party_risks_df)

# -------------------------
# Spending Over Time
# -------------------------
st.subheader("Spending Over Time")
trend = filtered_df.groupby("date")["amount"].sum().reset_index()
trend["z_score"] = (trend["amount"] - trend["amount"].mean()) / trend["amount"].std()
trend["anomaly"] = trend["z_score"].abs() > 2

fig1 = px.line(trend, x="date", y="amount", markers=True)
anomalies = trend[trend["anomaly"]]
fig1.add_scatter(
    x=anomalies["date"],
    y=anomalies["amount"],
    mode="markers",
    marker=dict(size=10, color="red"),
    name="Anomaly"
)
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
# Donor Contribution Share
# -------------------------
st.subheader("Donor Contribution Share")
donor_share = filtered_df.groupby("donor")["amount"].sum().reset_index()
fig4 = px.pie(donor_share, values="amount", names="donor")
st.plotly_chart(fig4, use_container_width=True)

# -------------------------
# Party Funding Comparison
# -------------------------
st.subheader("Party Funding Comparison")
party_totals = filtered_df.groupby("party")["amount"].sum().reset_index()
fig3 = px.bar(party_totals, x="party", y="amount")
st.plotly_chart(fig3, use_container_width=True)