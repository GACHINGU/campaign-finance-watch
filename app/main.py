import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data
from utils.risk_engine import calculate_hhi, detect_spike, classify_risk

# -------------------------
# NEW: DATA UPLOADER FUNCTION
# -------------------------

def load_custom_data():
    """Handles user file uploads for CSV, XLSX, and JSON."""
    st.sidebar.header("Upload Campaign Data")
    uploaded_file = st.sidebar.file_uploader(
        "Choose a file", 
        type=["csv", "xlsx", "json"],
        help="Upload a file with columns: party, region, date, amount, donor"
    )

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith('.json'):
                df = pd.read_json(uploaded_file)
            
            # Ensure date column is datetime objects
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
            
            return df
        except Exception as e:
            st.error(f"Error loading file: {e}")
            return None
    
    # Fallback to default data if no file is uploaded
    return load_data()

# -------------------------
# UI & NAVIGATION FUNCTIONS
# -------------------------

def apply_sidebar_filters(df):
    st.sidebar.header("Data Filters")
    
    # Check if required columns exist to avoid crashes with custom uploads
    required_cols = ["party", "region", "date", "donor"]
    if not all(col in df.columns for col in required_cols):
        st.sidebar.warning("Uploaded file is missing required columns.")
        return df

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
        st.download_button("Download Risk Report (.txt)", data=summary_text, file_name="campaign_risk_report.txt")

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

    # Use the new custom loader
    df = load_custom_data()

    if df is not None:
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
    else:
        st.info("Please upload a file in the sidebar to begin analysis.")

if __name__ == "__main__":
    main()