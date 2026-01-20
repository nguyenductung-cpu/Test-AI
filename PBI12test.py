import streamlit as st
import pandas as pd
from datetime import datetime, date

# --- MOCK DATA SETUP ---
def load_mock_data():
    goals = pd.DataFrame([
        {"Child ID": "C001", "Nickname": "Tobi", "Goal Name": "New Bike", "Parent Username": "JohnDoe", "Status": "Active", "Created Date": date(2025, 12, 1), "Target": 200, "Current": 50},
        {"Child ID": "C002", "Nickname": "Mila", "Goal Name": "Laptop", "Parent Username": "JaneSmith", "Status": "Completed", "Created Date": date(2025, 11, 15), "Target": 1000, "Current": 1000},
        {"Child ID": "C003", "Nickname": "Leo", "Goal Name": "Skateboard", "Parent Username": "JohnDoe", "Status": "Pending Approval", "Created Date": date(2025, 12, 20), "Target": 80, "Current": 10},
    ])
    return goals

# --- SCREEN 1: ADMIN MANAGEMENT (PBI 1) ---
def admin_screen():
    st.header("🔍 Caleb Admin: Goal Management")
    df = load_mock_data()

    # Sidebar Filters
    st.sidebar.subheader("Filters")
    keyword = st.sidebar.text_input("Keyword Search", help="Search Goal Name, Child ID, or Parent Username")
    status_filter = st.sidebar.multiselect("Progress Status", 
                                          options=["Active", "Completed", "Pending Approval", "Cancelled", "Rejected", "Expired"],
                                          default=["Active", "Completed", "Pending Approval"])
    date_range = st.sidebar.date_input("Created Date Range", [date(2025, 11, 1), date.today()])

    # Apply Logic
    filtered_df = df[df['Status'].isin(status_filter)]
    if keyword:
        k = keyword.lower()
        filtered_df = filtered_df[
            filtered_df['Goal Name'].str.lower().str.contains(k) | 
            filtered_df['Child ID'].str.lower().str.contains(k) | 
            filtered_df['Parent Username'].str.lower().str.contains(k)
        ]
    
    # Display Table
    st.subheader("Goals Status Report")
    st.dataframe(filtered_df, use_container_width=True)
    
    if st.button("📥 Export by Filter (CSV)"):
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button("Click to Download", csv, "filtered_report.csv", "text/csv")

# --- SCREEN 2: PN TEMPLATE TESTER (PBI 2) ---
def notification_screen():
    st.header("🔔 Push Notification Logic Tester")
    st.info("Change the values below to see how the notification message automatically hides fields that didn't change.")

    col1, col2 = st.columns(2)
    with col1:
        st.write("**Current Values**")
        curr_name = st.text_input("Goal Name", "Mountain Bike")
        curr_target = st.text_input("Target Amount", "S$150")
        curr_end = st.date_input("Target End Date", date(2026, 6, 1))
    
    with col2:
        st.write("**Previous Values (Before Edit)**")
        prev_name = st.text_input("Prev Goal Name", "Bike")
        prev_target = st.text_input("Prev Target Amount", "S$100")
        prev_end = st.date_input("Prev Target End Date", date(2026, 6, 1))

    # Business Logic for PN
    edits = []
    if curr_name != prev_name:
        edits.append(f"• The goal name has been changed from {prev_name} to {curr_name}.")
    if curr_target != prev_target:
        edits.append(f"• The target amount has been changed from {prev_target} to {curr_target}.")
    if curr_end != prev_end:
        edits.append(f"• The end date has been changed from {prev_end} to {curr_end}.")

    # Generate Message
    st.divider()
    st.subheader("Live Preview")
    message = f"Your parent has made some changes to your goal {curr_name}! 😊\n\n" + "\n".join(edits)
    
    st.code(message, language="markdown")
    
    if not edits:
        st.warning("No changes detected. The 'Edit' shortfields are omitted per Business Rule.")

# --- MAIN APP NAVIGATION ---
st.set_page_config(page_title="PBI Testing Suite", layout="wide")
page = st.sidebar.radio("Go to Screen:", ["Admin Reports (PBI 1)", "PN Logic Tester (PBI 2)"])

if page == "Admin Reports (PBI 1)":
    admin_screen()
else:
    notification_screen()