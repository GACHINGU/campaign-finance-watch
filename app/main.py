import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data
from utils.risk_engine import calculate_hhi, detect_spike, classify_risk

# -------------------------
# UI & NAVIGATION FUNCTIONS
# -------------------------

def apply_sidebar_filters(df):
    st.sidebar.header(" Data Filters")
    
    selected_party = st.sidebar.multiselect("Select Party", options=df["party"].unique(), default=df["party"].unique())
    selected_region = st.sidebar.multiselect("Select Region", options=df["region"].unique(), default=df["region"].unique())

    st.sidebar.subheader("Date Range")
    min_date, max_date = df["date"].min(), df["date"].max()
    date_range = st.sidebar.date_input("Select period", value=[min_date, max_date], min_value=min_date, max_value=max_date)
    
    if isinstance(date_range, list) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date

    mask = (
        (df["party"].isin(selected_party)) &
        (df["region"].isin(selected_region)) &
        (df["date"] >= pd.to_datetime(start_date)) &
        (df["date"] <= pd.to_datetime(end_date))
    )
    return df.loc[mask]

def run_alerts(hhi, z_score):
    """Triggers sidebar alerts based on risk thresholds."""
    if hhi > 0.6:
        st.sidebar.error("🚨 ALERT: High Donor Concentration detected!")
    if z_score > 3:
        st.sidebar.warning("⚠️ ALERT: Extreme Spending Spike detected!")

# -------------------------
# PAGE CONTENT FUNCTIONS
# -------------------------

def render_dashboard_overview(df):
    st.header("Campaign Spending Dashboard")
    
    col1, col2 = st.columns(2)
    col1.metric("Total Spending (KES)", f"{df['amount'].sum():,.0f}")
    col2.metric("Unique Donors", df["donor"].nunique())
    
    st.divider()
    st.subheader("Spending Over Time")
    trend = df.groupby("date")["amount"].sum().reset_index()
    st.plotly_chart(px.line(trend, x="date", y="amount", markers=True), use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Funding by Party")
        st.plotly_chart(px.bar(df.groupby("party")["amount"].sum().reset_index(), x="party", y="amount", color="party"), use_container_width=True)
    with col_b:
        st.subheader("Top 10 Donors")
        top_donors = df.groupby("donor")["amount"].sum().sort_values(ascending=False).head(10).reset_index()
        st.plotly_chart(px.bar(top_donors, x="donor", y="amount"), use_container_width=True)

def render_risk_intelligence(df):
    st.header("⚠️ Risk & Compliance Intelligence")
    
    hhi = calculate_hhi(df)
    z_score = detect_spike(df)
    risk_level = classify_risk(hhi, z_score)

    r_col1, r_col2, r_col3 = st.columns(3)
    r_col1.metric("Donor Concentration (HHI)", hhi)
    r_col2.metric("Spending Spike (Z-score)", z_score)
    
    if risk_level == "High": r_col3.error(f"Risk Level: {risk_level}")
    elif risk_level == "Medium": r_col3.warning(f"Risk Level: {risk_level}")
    else: r_col3.success(f"Risk Level: {risk_level}")

    # --- RE-ADDED: RISK REPORT SECTION ---
    with st.expander("📝 Generate & Download Risk Report"):
        summary_text = f"""Campaign Risk Assessment Report
-------------------------------
- Donor Concentration (HHI): {hhi}
- Spending Spike (Z-score): {z_score}
- Overall Risk Level: {risk_level}

Interpretation:
Higher HHI indicates funding concentration among few donors.
Z-score above 2 suggests abnormal spending spikes.
Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}
"""
        st.text(summary_text)
        st.download_button(
            label="Download Risk Report (.txt)",
            data=summary_text,
            file_name="campaign_risk_report.txt",
            mime="text/plain"
        )

    st.divider()
    st.subheader("Party-level Risk Indicators")
    party_risks = []
    for party in df["party"].unique():
        df_p = df[df["party"] == party]
        h_p, z_p = calculate_hhi(df_p), detect_spike(df_p)
        party_risks.append({"Party": party, "HHI": h_p, "Z-score": z_p, "Risk Level": classify_risk(h_p, z_p)})
    st.dataframe(pd.DataFrame(party_risks), use_container_width=True)

def render_data_explorer(df):
    st.header("📄 Data Explorer & Export")
    st.dataframe(df, use_container_width=True)
    st.download_button("Download CSV", data=df.to_csv(index=False), file_name="campaign_data.csv", mime="text/csv")

# -------------------------
# MAIN APP ENTRY POINT
# -------------------------

def main():
    st.set_page_config(page_title="Finance Watch", layout="wide", page_icon="🗳️")

    df = load_data()

    # Sidebar Navigation
    st.sidebar.title("🗳️ Finance Watch")
    page = st.sidebar.radio("Navigation", ["Dashboard Overview", "Risk Intelligence", "Data Explorer"])
    st.sidebar.markdown("---")

    # Filter Logic
    filtered_df = apply_sidebar_filters(df)

    # Alerts Logic
    if not filtered_df.empty:
        run_alerts(calculate_hhi(filtered_df), detect_spike(filtered_df))

    # Page Routing
    if filtered_df.empty:
        st.error("No data found for selected filters.")
    else:
        if page == "Dashboard Overview": render_dashboard_overview(filtered_df)
        elif page == "Risk Intelligence": render_risk_intelligence(filtered_df)
        elif page == "Data Explorer": render_data_explorer(filtered_df)

if __name__ == "__main__":
    main()