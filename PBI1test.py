import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Caleb Admin - Goals Management", layout="wide")

# --- 2. MOCK DATA GENERATOR ---
# Created with the exact column names specified in PBI#1 EARS section
@st.cache_data
def load_data():
    # Goals Status Fields
    status_cols = [
        "Child ID", "Nickname", "Access", "Parent ID", "Parent Username", 
        "Goal Name", "Current Amount Allocated", "Target Amount", 
        "Created Date", "Target End Date", "Actual End Date", "Progress Status"
    ]
    
    # Goals Activity Fields
    activity_cols = [
        "Transaction Date & Time", "Child ID", "Nickname", "Child Access", 
        "Parent ID", "Parent Username", "Goal Name", "Amount Allocated", 
        "Amount Post Allocation"
    ]

    # Mocking rows to match column definitions
    status_mock = [
        ["C-001", "Alex", "Full", "P-100", "user_parent_1", "New Bike", 50.0, 200.0, "15-01-2026", "01-02-2026", None, "Active"],
        ["C-002", "Bella", "Limited", "P-101", "user_parent_2", "Lego Set", 100.0, 100.0, "01-01-2026", "20-01-2026", "20-01-2026", "Completed"],
        ["C-003", "Charlie", "Full", "P-100", "user_parent_1", "Savings", 25.0, 1000.0, "20-12-2025", "01-01-2027", None, "Pending Approval"]
    ]
    
    activity_mock = [
        ["20-01-2026 14:30:00", "C-001", "Alex", "Full", "P-100", "user_parent_1", "New Bike", 10.0, 50.0],
        ["19-01-2026 09:15:00", "C-002", "Bella", "Limited", "P-101", "user_parent_2", "Lego Set", 50.0, 100.0],
        ["21-01-2026 10:00:00", "C-001", "Alex", "Full", "P-100", "user_parent_1", "New Bike", 5.0, 55.0]
    ]

    df_status = pd.DataFrame(status_mock, columns=status_cols)
    df_activity = pd.DataFrame(activity_mock, columns=activity_cols)
    
    # Convert dates to datetime objects for filtering
    df_status["Created Date"] = pd.to_datetime(df_status["Created Date"], dayfirst=True)
    df_activity["Transaction Date & Time"] = pd.to_datetime(df_activity["Transaction Date & Time"], dayfirst=True)
    
    return df_status, df_activity

status_df, activity_df = load_data()

# --- 3. SIDEBAR FILTERS ---
st.sidebar.header("Filter Rules")

# Keyword Search (Goal Name, Child ID, Parent ID, Child Nickname, Parent Username, Child Access)
keyword = st.sidebar.text_input("Keyword Search", placeholder="Partial match, case-insensitive")

# Date Range Rule: Default to "Start from today backward 1 month"
today = datetime.now().date()
one_month_ago = today - timedelta(days=30)
date_range = st.sidebar.date_input(
    "Time Range Filter (DD-MM-YYYY)",
    value=(one_month_ago, today),
    format="DD-MM-YYYY"
)

# Progress Status Rule: Multiple selection dropdown
status_options = ["Completed", "Active", "Pending Approval", "Cancelled", "Rejected", "Expired"]
selected_statuses = st.sidebar.multiselect("Progress Status", status_options, default=["Active", "Completed"])

# --- 4. MAIN INTERFACE ---
st.title("Admin Reconciliation Dashboard")

tab1, tab2 = st.tabs(["Goal Status Report", "Goal Activity Report"])

# Mandatory Export Logic Helper
def validate_export():
    if not isinstance(date_range, tuple) or len(date_range) < 2:
        st.error("Error: Time Range filter is mandatory for exporting data.")
        return False
    return True

# Filtering Helper
def apply_filters(df, date_col):
    filtered = df.copy()
    
    # Apply Keyword (Case-insensitive partial match across all specified fields)
    if keyword:
        search_cols = ["Goal Name", "Child ID", "Parent ID", "Nickname", "Parent Username"]
        # Only search columns that exist in the current dataframe
        available_cols = [c for c in search_cols if c in filtered.columns]
        mask = filtered[available_cols].apply(lambda row: row.astype(str).str.lower().str.contains(keyword.lower()).any(), axis=1)
        filtered = filtered[mask]
    
    # Apply Multi-select Status
    if "Progress Status" in filtered.columns and selected_statuses:
        filtered = filtered[filtered["Progress Status"].isin(selected_statuses)]
        
    # Apply Date Range
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        filtered = filtered[(filtered[date_col] >= start) & (filtered[date_col] <= end)]
        
    return filtered

# --- TAB 1: GOAL STATUS ---
with tab1:
    st.subheader("Goals Status Management")
    filtered_status = apply_filters(status_df, "Created Date")
    st.dataframe(filtered_status, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Export by Filter (Status)"):
            if validate_export():
                st.download_button("Download CSV", filtered_status.to_csv(index=False), "goal_status_filtered.csv", "text/csv")
    with col2:
        if st.button("Export All (Status)"):
            if validate_export():
                # Requirement: Export all is still subject to the 1-month mandatory date constraint
                st.download_button("Download CSV", status_df.to_csv(index=False), "goal_status_all.csv", "text/csv")

# --- TAB 2: GOAL ACTIVITY ---
with tab2:
    st.subheader("Goals Activity Log")
    # Rule: Sort by the latest transaction date and time by default
    sorted_activity = activity_df.sort_values(by="Transaction Date & Time", ascending=False)
    filtered_activity = apply_filters(sorted_activity, "Transaction Date & Time")
    
    st.dataframe(filtered_activity, use_container_width=True)
    
    col3, col4 = st.columns(2)
    with col3:
        if st.button("Export by Filter (Activity)"):
            if validate_export():
                st.download_button("Download CSV", filtered_activity.to_csv(index=False), "goal_activity_filtered.csv", "text/csv")
    with col4:
        if st.button("Export All (Activity)"):
            if validate_export():
                st.download_button("Download CSV", activity_df.to_csv(index=False), "goal_activity_all.csv", "text/csv")