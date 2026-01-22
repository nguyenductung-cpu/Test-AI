# Business Specification Document
## Goals Management System - Admin Reconciliation Dashboard

**Document Version:** 1.0  
**Date Created:** January 22, 2026  
**Status:** Active  

---

## Executive Summary

This document outlines the functional and non-functional requirements for the Goals Management System, a Streamlit-based application designed to provide administrators with real-time goal tracking and analytics. The system enables reconciliation of child savings goals through comprehensive status and activity reporting with professional data visualization.

---

## System Overview

The Goals Management System is a web-based admin reconciliation dashboard consisting of two primary reporting modules:
1. **Goals Status Report Module:** Real-time tracking of child savings goal progress
2. **Goals Activity Report Module:** Comprehensive transaction log and activity tracking

---

## Requirements Specification

### Module 1: Goals Status Report

#### REQ-1.1: Display Application Header
**EARS Notation:**  
`When` the application initializes, `the system shall` display a professional main header containing the title "📊 Goals Management System" and subtitle "Admin Reconciliation Dashboard • Real-time Goal Tracking & Analytics" with a linear gradient background (#0066CC to #003A99).

**Priority:** High  
**Category:** UI/UX  

---

#### REQ-1.2: Configure Page Settings
**EARS Notation:**  
`When` the application initializes, `the system shall` configure the Streamlit page with page title "Goals Management System", wide layout, expanded sidebar state, and disabled menu items.

**Priority:** High  
**Category:** Configuration  

---

#### REQ-1.3: Load Goal Status Mock Data
**EARS Notation:**  
`When` the application initializes, `the system shall` load and cache mock data containing goal status information with the following columns: Child ID, Nickname, Access, Parent ID, Parent Username, Goal Name, Current Amount Allocated, Target Amount, Created Date, Target End Date, Actual End Date, and Progress Status.

**Minimum Records:** 3 sample goals  
**Priority:** High  
**Category:** Data Management  

---

#### REQ-1.4: Load Goal Activity Mock Data
**EARS Notation:**  
`When` the application initializes, `the system shall` load and cache mock transaction data with the following columns: Transaction Date & Time, Child ID, Nickname, Child Access, Parent ID, Parent Username, Goal Name, Amount Allocated, and Amount Post Allocation.

**Minimum Records:** 3 sample transactions  
**Priority:** High  
**Category:** Data Management  

---

#### REQ-1.5: Display Tab Navigation
**EARS Notation:**  
`When` the Goals Status Report module loads, `the system shall` display two tabs: "📋 Goal Status Report" and "📈 Goal Activity Report" allowing users to switch between status and activity views.

**Priority:** High  
**Category:** Navigation  

---

#### REQ-1.6: Display Goal Status Metrics
**EARS Notation:**  
`When` the Goal Status Report tab is active, `the system shall` display three metric cards in a three-column layout showing: Total Goals, Active Goals, and Completed Goals with accurate counts from the dataset.

**Priority:** High  
**Category:** Analytics  

---

#### REQ-1.7: Display Goal Status Data Table
**EARS Notation:**  
`When` the Goal Status Report tab is active, `the system shall` display a native Streamlit dataframe containing all goal status records with full container width, index hidden, and custom column formatting for Status, Current Allocated, and Target Amount.

**Formatting:**
- Progress Status: Display as text column
- Current Amount Allocated: Display as currency with $%.2f format
- Target Amount: Display as currency with $%.2f format

**Priority:** High  
**Category:** Display  

---

#### REQ-1.8: Export All Goal Status Data
**EARS Notation:**  
`Given` the Goal Status Report tab is active, `when` the user clicks the "📥 Export All Data" button, `the system shall` generate and provide a downloadable CSV file containing all goal status records with timestamp in filename.

**Filename Format:** goal_status_all_YYYYMMDD_HHMMSS.csv  
**Priority:** Medium  
**Category:** Export  

---

#### REQ-1.9: Display Goal Status Statistics
**EARS Notation:**  
`Given` the Goal Status Report tab is active, `when` the user clicks the "📊 View Statistics" button, `the system shall` display an info box showing total goals count, active goals count, and completed goals count.

**Priority:** Medium  
**Category:** Analytics  

---

#### REQ-1.10: Display Goal Activity Metrics
**EARS Notation:**  
`When` the Goal Activity Report tab is active, `the system shall` display two metric cards in a two-column layout showing: Total Transactions and Total Amount Allocated with aggregated values from the activity dataset.

**Priority:** High  
**Category:** Analytics  

---

#### REQ-1.11: Display Goal Activity Data Table
**EARS Notation:**  
`When` the Goal Activity Report tab is active, `the system shall` display a native Streamlit dataframe containing all goal activity records sorted by Transaction Date & Time in descending order, with full container width, index hidden, and custom column formatting for monetary amounts.

**Formatting:**
- Amount Allocated: Display as currency with $%.2f format
- Amount Post Allocation: Display as currency with $%.2f format
- Sort Order: Latest transactions first

**Priority:** High  
**Category:** Display  

---

#### REQ-1.12: Export All Goal Activity Data
**EARS Notation:**  
`Given` the Goal Activity Report tab is active, `when` the user clicks the "📥 Export All Data" button, `the system shall` generate and provide a downloadable CSV file containing all goal activity records with timestamp in filename.

**Filename Format:** goal_activity_all_YYYYMMDD_HHMMSS.csv  
**Priority:** Medium  
**Category:** Export  

---

#### REQ-1.13: Display Goal Activity Statistics
**EARS Notation:**  
`Given` the Goal Activity Report tab is active, `when` the user clicks the "📊 View Statistics" button, `the system shall` display an info box showing total transaction count and sum of all amounts allocated.

**Priority:** Medium  
**Category:** Analytics  

---

#### REQ-1.14: Convert Date Formats
**EARS Notation:**  
`When` mock data is loaded, `the system shall` automatically convert date strings (format: DD-MM-YYYY) to pandas datetime objects for Created Date field and convert transaction timestamps (format: DD-MM-YYYY HH:MM:SS) to datetime objects for Transaction Date & Time field to enable proper date-based sorting and filtering.

**Priority:** Medium  
**Category:** Data Processing  

---

#### REQ-1.15: Apply Professional CSS Styling
**EARS Notation:**  
`When` any page element is rendered, `the system shall` apply professional CSS styling including the following color scheme: primary #0066CC, secondary #003A99, success #28A745, warning #FFC107, danger #DC3545, light background #F8F9FA, and border color #E0E0E0.

**Styling Elements:**
- Header with gradient background and shadow
- Section titles with bottom border accent
- Filter sections with left border highlight
- Rounded buttons with hover effects
- Styled input fields
- Professional dataframe styling
- Tab styling with active state highlighting
- Metric cards with shadow and border

**Priority:** Medium  
**Category:** UI/UX  

---

## Data Model

### Goals Status Entity

| Attribute | Data Type | Constraints |
|-----------|-----------|-------------|
| Child ID | String | Unique, Required (Format: C-XXX) |
| Nickname | String | Required |
| Access | Enum | One of: Full, Limited |
| Parent ID | String | Required (Format: P-XXX) |
| Parent Username | String | Required |
| Goal Name | String | Required |
| Current Amount Allocated | Decimal | Required, >= 0 |
| Target Amount | Decimal | Required, > 0 |
| Created Date | Date | Required (Format: DD-MM-YYYY) |
| Target End Date | Date | Required (Format: DD-MM-YYYY) |
| Actual End Date | Date | Optional (Format: DD-MM-YYYY) |
| Progress Status | Enum | One of: Active, Completed, Pending Approval |

### Goals Activity Entity

| Attribute | Data Type | Constraints |
|-----------|-----------|-------------|
| Transaction Date & Time | DateTime | Required (Format: DD-MM-YYYY HH:MM:SS) |
| Child ID | String | Required (Format: C-XXX) |
| Nickname | String | Required |
| Child Access | Enum | One of: Full, Limited |
| Parent ID | String | Required (Format: P-XXX) |
| Parent Username | String | Required |
| Goal Name | String | Required |
| Amount Allocated | Decimal | Required, > 0 |
| Amount Post Allocation | Decimal | Required, >= Amount Allocated |

### Progress Status Codes

| Status | Description |
|--------|-------------|
| Active | Goal is currently in progress, has not reached target |
| Completed | Goal has reached the target amount |
| Pending Approval | Goal awaiting administrative approval |

### Access Levels

| Level | Description |
|-------|-------------|
| Full | Child has unrestricted access to goal functions |
| Limited | Child has restricted access to certain functions |

---

## Non-Functional Requirements

#### NFR-1: Performance
**EARS Notation:**  
`When` the application loads mock data and renders dataframes, `the system shall` complete initialization and display within 3 seconds for datasets containing up to 1000 records.

**Priority:** High  

---

#### NFR-2: Data Caching
**EARS Notation:**  
`When` the application initializes, `the system shall` use Streamlit's @st.cache_data decorator to cache mock data and prevent unnecessary reloading on page reruns.

**Priority:** High  

---

#### NFR-3: Usability
**EARS Notation:**  
`When` a user interacts with export buttons or metric displays, `the system shall` provide immediate visual feedback and generate downloadable files with accurate timestamps and data.

**Priority:** High  

---

#### NFR-4: Data Accuracy
**EARS Notation:**  
`When` currency values are displayed in dataframes, `the system shall` format all amounts using currency notation (format: $%.2f) to ensure financial data clarity.

**Priority:** High  

---

#### NFR-5: Browser Compatibility
**EARS Notation:**  
`When` the application is accessed via browser, `the system shall` support modern web browsers including Chrome, Firefox, Safari, and Edge with versions released within the last 24 months.

**Priority:** Medium  

---

## Use Cases and User Scenarios

### Use Case 1: View Goal Status Overview
**Actor:** Admin User  
**Precondition:** Application is running and loaded  
**Main Flow:**
1. User accesses the application
2. System displays the Goals Status Report tab by default
3. User views metric cards showing total goals, active goals, and completed goals
4. User reviews the complete goal status table with all record details
5. User exports data if needed in CSV format

**Postcondition:** Admin has complete visibility into goal status

---

### Use Case 2: Review Goal Activity Transactions
**Actor:** Admin User  
**Precondition:** Application is running and Goal Activity Report tab is accessible  
**Main Flow:**
1. User clicks on the Goal Activity Report tab
2. System displays metric cards with transaction count and total allocated amounts
3. User views activity log sorted by latest transactions first
4. User reviews transaction details including amounts and timestamps
5. User exports transaction data if needed in CSV format

**Postcondition:** Admin has visibility into transaction history and activity patterns

---

## User Stories Summary

### US-1: Admin Goal Status Monitoring
As an admin user, I need to view and analyze child savings goals through a comprehensive status dashboard so that I can monitor progress, identify active goals, and generate reports for reconciliation purposes.

**Acceptance Criteria:**
- System displays total goals, active goals, and completed goals metrics
- All goal status records are visible in a professional data table
- Currency amounts are properly formatted with $ prefix and decimal places
- Export functionality generates timestamped CSV files
- Data loads and displays within 3 seconds

### US-2: Admin Transaction Auditing
As an admin user, I need to review goal activity transactions with chronological ordering so that I can audit fund allocations, verify transaction accuracy, and maintain comprehensive activity records.

**Acceptance Criteria:**
- All transactions are sorted by date with latest first
- Transaction metrics show total count and aggregate amounts
- Currency values in activity log are properly formatted
- Export includes complete transaction details with timestamps
- Metric calculations are accurate and real-time

---

## Glossary

| Term | Definition |
|------|-----------|
| Admin User | System administrator responsible for goal reconciliation and reporting |
| Mock Data | Sample test data used for application demonstration and testing |
| CSV Export | Comma-separated values file format used for data export and analysis |
| Reconciliation Dashboard | Administrative interface for verifying and auditing goal data |
| Goal Status | Current progress state of a child's savings objective |
| Transaction | Individual allocation of funds toward a savings goal |
| Amount Allocated | Funds contributed to a goal in a specific transaction |
| Amount Post Allocation | Total goal balance after a transaction is completed |
| Access Level | Permission level assigned to child user (Full or Limited) |
| Data Caching | Streamlit technique to prevent unnecessary data reloading |
| Dataframe | Tabular data structure used for displaying records |

---

## Technical Architecture Notes

### Frontend Framework
- **Technology:** Streamlit
- **Styling:** Custom CSS with professional color scheme
- **Layout:** Responsive wide layout with column-based design

### Data Management
- **Data Source:** Mock data generated programmatically
- **Caching:** Streamlit @st.cache_data decorator for performance
- **Date Format:** DD-MM-YYYY (displayed and stored)
- **Currency Format:** $X,XXX.XX with dollar sign and two decimal places

### Export Functionality
- **Format:** CSV (Comma-Separated Values)
- **Encoding:** UTF-8
- **Filename Convention:** {report_type}_all_YYYYMMDD_HHMMSS.csv
- **Timestamp Generation:** System datetime at export time

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | January 22, 2026 | AI Assistant | Initial specification document based on PBI1test.py with EARS notation |

---

## Document Approval and Sign-Off

This document is subject to review and approval by the following stakeholders:

- [ ] Product Manager
- [ ] Development Lead  
- [ ] QA Lead
- [ ] Business Owner

**Approval Date:** _______________

**Approved By:** _________________

---

**End of Document**
