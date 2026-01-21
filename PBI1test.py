import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Goals Management System",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)

# --- PROFESSIONAL STYLING ---
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #0066CC;
        --secondary-color: #003A99;
        --success-color: #28A745;
        --warning-color: #FFC107;
        --danger-color: #DC3545;
        --light-bg: #F8F9FA;
        --border-color: #E0E0E0;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #0066CC 0%, #003A99 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1rem;
        opacity: 0.95;
    }
    
    /* Section styling */
    .section-title {
        border-bottom: 3px solid #0066CC;
        padding-bottom: 0.8rem;
        margin-bottom: 1.5rem;
        font-size: 1.5rem;
        font-weight: 600;
        color: #003A99;
    }
    
    /* Filter section styling */
    .filter-section {
        background-color: #F8F9FA;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #0066CC;
        margin-bottom: 1.5rem;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 6px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,102,204,0.3);
    }
    
    /* Download button styling */
    .stDownloadButton > button {
        background-color: #28A745 !important;
        border-radius: 6px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input,
    .stDateInput > div > div > input,
    .stSelectbox > div > div > select,
    .stMultiSelect > div > div > div {
        border-radius: 6px;
        border: 1px solid #E0E0E0;
        padding: 0.5rem !important;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border-radius: 8px;
        border: 1px solid #E0E0E0;
        overflow: hidden;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        border-bottom: 2px solid #E0E0E0;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.8rem 1.5rem;
        font-weight: 600;
        border-radius: 6px 6px 0 0;
        background-color: #F8F9FA;
        color: #666;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #0066CC !important;
        color: white !important;
    }
    
    /* Metrics styling */
    .metric-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #E0E0E0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

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

# --- PROFESSIONAL HEADER ---
st.markdown("""
<div class="main-header">
    <h1>📊 Goals Management System</h1>
    <p>Admin Reconciliation Dashboard • Real-time Goal Tracking & Analytics</p>
</div>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR FILTERS ---
st.sidebar.markdown("### 🔍 Filter Controls")
st.sidebar.markdown("---")

# Keyword Search
st.sidebar.markdown("**Global Search**")
keyword = st.sidebar.text_input(
    "Keyword Search",
    placeholder="Search by ID, Name, Username...",
    help="Case-insensitive partial match across all fields"
)

# Date Range Rule
st.sidebar.markdown("**Date Range**")
today = datetime.now().date()
one_month_ago = today - timedelta(days=30)
date_range = st.sidebar.date_input(
    "Time Range Filter",
    value=(one_month_ago, today),
    format="DD-MM-YYYY",
    help="Default: Last 30 days"
)

# Progress Status Rule
st.sidebar.markdown("**Status Filter**")
status_options = ["Completed", "Active", "Pending Approval", "Cancelled", "Rejected", "Expired"]
selected_statuses = st.sidebar.multiselect(
    "Progress Status",
    status_options,
    default=["Active", "Completed"],
    help="Select one or more statuses"
)

# --- 4. MAIN INTERFACE ---
st.markdown("---")

# Create tabs with better styling
tab1, tab2 = st.tabs(["📋 Goal Status Report", "📈 Goal Activity Report"])

# Mandatory Export Logic Helper
def validate_export():
    if not isinstance(date_range, tuple) or len(date_range) < 2:
        st.error("Error: Time Range filter is mandatory for exporting data.")
        return False
    return True

# Filtering Helper
def apply_filters(df, date_col, column_filters=None):
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
    
    # Apply Column-level filters
    if column_filters:
        for col, filter_value in column_filters.items():
            if col in filtered.columns and filter_value:
                filtered = filtered[filtered[col].astype(str).str.lower().str.contains(filter_value.lower(), na=False)]
        
    return filtered

# Helper function to display column filters integrated with table
def display_column_filters_in_table(df, prefix):
    """Display filter inputs as part of a table-like interface with 1-second debounce"""
    import time
    
    # Create a filter row styling
    st.markdown("""
    <style>
        .table-filter-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 0.5rem;
            background-color: #E8F1FF;
            padding: 0.8rem;
            border: 1px solid #0066CC;
            border-radius: 6px 6px 0 0;
            margin-bottom: 0;
        }
        .filter-input-cell {
            display: flex;
            align-items: center;
        }
        .filter-input-cell input {
            width: 100%;
            padding: 0.5rem !important;
            border: 1px solid #B0D4FF !important;
            border-radius: 4px !important;
            background-color: white !important;
            font-size: 0.85rem !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Create filter row
    num_cols = len(df.columns)
    cols = st.columns(num_cols)
    filters = {}
    
    st.markdown("<div style='background-color: #E8F1FF; padding: 0.8rem; border: 1px solid #0066CC; border-radius: 6px 6px 0 0; margin-bottom: -1rem;'><strong style='color: #003A99; font-size: 0.9rem;'>🔍 Search by Column:</strong></div>", unsafe_allow_html=True)
    
    filter_cols = st.columns(num_cols)
    for i, col in enumerate(df.columns):
        with filter_cols[i]:
            filter_key = f"{prefix}_{col}_filter"
            filters[col] = st.text_input(
                label=f"🔍 {col}",
                key=filter_key,
                placeholder=f"Search...",
                label_visibility="collapsed"
            )
    
    return filters

# --- TAB 1: GOAL STATUS ---
with tab1:
    st.markdown('<div class="section-title">🎯 Goals Status Management</div>', unsafe_allow_html=True)
    
    # Display metrics
    col_metrics_1, col_metrics_2, col_metrics_3 = st.columns(3)
    with col_metrics_1:
        st.metric("Total Goals", len(status_df), delta=None)
    with col_metrics_2:
        active_count = len(status_df[status_df["Progress Status"] == "Active"])
        st.metric("Active Goals", active_count, delta=None)
    with col_metrics_3:
        completed_count = len(status_df[status_df["Progress Status"] == "Completed"])
        st.metric("Completed Goals", completed_count, delta=None)
    
    st.markdown("---")
    
    # Initialize session state for filter tracking
    if "status_filters_prev" not in st.session_state:
        st.session_state.status_filters_prev = {}
    if "status_filter_time" not in st.session_state:
        st.session_state.status_filter_time = {}
    
    # Display column filters integrated with table
    st.markdown("**Column Filters (Live Search):**")
    status_filters = display_column_filters_in_table(status_df, "status")
    
    # Add debounce: only apply filters if 1 second has passed
    import time
    current_time = time.time()
    filters_changed = status_filters != st.session_state.get("status_filters_prev", {})
    
    # Apply filters with debounce logic
    if filters_changed:
        st.session_state.status_filter_time = current_time
        st.session_state.status_filters_prev = status_filters.copy()
    
    # Check if 1 second has passed since last change
    time_elapsed = current_time - st.session_state.get("status_filter_time", current_time)
    if time_elapsed >= 1 or not filters_changed:
        # Apply all filters including column filters
        filtered_status = apply_filters(status_df, "Created Date", status_filters)
    else:
        # While debouncing, show previous results
        filtered_status = apply_filters(status_df, "Created Date", st.session_state.get("status_filters_prev", {}))
    
    # Display results count
    st.markdown(f"**Results:** {len(filtered_status)} of {len(status_df)} goals")
    
    # Display dataframe with improved styling
    st.dataframe(
        filtered_status,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Progress Status": st.column_config.TextColumn(
                "Status",
                help="Current progress status of the goal"
            ),
            "Current Amount Allocated": st.column_config.NumberColumn(
                "Current Allocated",
                format="$%.2f"
            ),
            "Target Amount": st.column_config.NumberColumn(
                "Target Amount",
                format="$%.2f"
            )
        }
    )
    
    st.markdown("---")
    
    # Export section
    st.markdown("**Export Options**")
    col_export_1, col_export_2 = st.columns(2)
    with col_export_1:
        if st.button("📥 Export Filtered Results", use_container_width=True):
            if validate_export():
                st.download_button(
                    label="Download Filtered CSV",
                    data=filtered_status.to_csv(index=False),
                    file_name=f"goal_status_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    with col_export_2:
        if st.button("📊 Export All Results", use_container_width=True):
            if validate_export():
                st.download_button(
                    label="Download All CSV",
                    data=status_df.to_csv(index=False),
                    file_name=f"goal_status_all_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

# --- TAB 2: GOAL ACTIVITY ---
with tab2:
    st.markdown('<div class="section-title">📊 Goals Activity Log</div>', unsafe_allow_html=True)
    
    # Display metrics
    col_metrics_a, col_metrics_b = st.columns(2)
    with col_metrics_a:
        st.metric("Total Transactions", len(activity_df), delta=None)
    with col_metrics_b:
        total_allocated = activity_df["Amount Allocated"].sum()
        st.metric("Total Amount Allocated", f"${total_allocated:,.2f}", delta=None)
    
    st.markdown("---")
    
    # Sort by latest transaction
    sorted_activity = activity_df.sort_values(by="Transaction Date & Time", ascending=False)
    
    # Initialize session state for filter tracking
    if "activity_filters_prev" not in st.session_state:
        st.session_state.activity_filters_prev = {}
    if "activity_filter_time" not in st.session_state:
        st.session_state.activity_filter_time = {}
    
    # Display column filters integrated with table
    st.markdown("**Column Filters (Live Search):**")
    activity_filters = display_column_filters_in_table(sorted_activity, "activity")
    
    # Add debounce: only apply filters if 1 second has passed
    import time
    current_time = time.time()
    filters_changed = activity_filters != st.session_state.get("activity_filters_prev", {})
    
    # Apply filters with debounce logic
    if filters_changed:
        st.session_state.activity_filter_time = current_time
        st.session_state.activity_filters_prev = activity_filters.copy()
    
    # Check if 1 second has passed since last change
    time_elapsed = current_time - st.session_state.get("activity_filter_time", current_time)
    if time_elapsed >= 1 or not filters_changed:
        # Apply all filters including column filters
        filtered_activity = apply_filters(sorted_activity, "Transaction Date & Time", activity_filters)
    else:
        # While debouncing, show previous results
        filtered_activity = apply_filters(sorted_activity, "Transaction Date & Time", st.session_state.get("activity_filters_prev", {}))
    
    # Display results count
    st.markdown(f"**Results:** {len(filtered_activity)} of {len(activity_df)} transactions")
    
    # Display dataframe
    st.dataframe(
        filtered_activity,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Amount Allocated": st.column_config.NumberColumn(
                "Amount Allocated",
                format="$%.2f"
            ),
            "Amount Post Allocation": st.column_config.NumberColumn(
                "Amount Post Allocation",
                format="$%.2f"
            )
        }
    )
    
    st.markdown("---")
    
    # Export section
    st.markdown("**Export Options**")
    col_export_3, col_export_4 = st.columns(2)
    with col_export_3:
        if st.button("📥 Export Filtered Results", key="activity_filtered", use_container_width=True):
            if validate_export():
                st.download_button(
                    label="Download Filtered CSV",
                    data=filtered_activity.to_csv(index=False),
                    file_name=f"goal_activity_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    with col_export_4:
        if st.button("📊 Export All Results", key="activity_all", use_container_width=True):
            if validate_export():
                st.download_button(
                    label="Download All CSV",
                    data=activity_df.to_csv(index=False),
                    file_name=f"goal_activity_all_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )