# Business Specification Document
## Caleb Goals Management System

**Document Version:** 1.0  
**Date Created:** January 22, 2026  
**Status:** Active  

---

## Executive Summary

This document outlines the functional and non-functional requirements for the Caleb Goals Management System, a Streamlit-based application designed to manage child savings goals. The system includes administrative goal management capabilities and push notification templating features.

---

## System Overview

The Caleb Goals Management System consists of two primary modules:
1. **Admin Management Module (PBI 1):** Administrative interface for viewing and managing goals
2. **Push Notification Logic Tester (PBI 2):** Dynamic notification message generation based on goal edits

---

## Requirements Specification

### Module 1: Admin Management System (PBI 1)

#### REQ-1.1: Display Goals Dashboard
**EARS Notation:**  
`When` the admin user accesses the application, `the system shall` display a header titled "🔍 Caleb Admin: Goal Management" with a professional gradient background styling.

**Priority:** High  
**Category:** UI/UX  

---

#### REQ-1.2: Load Mock Goal Data
**EARS Notation:**  
`When` the application initializes, `the system shall` load mock data containing at least three child goals with the following attributes: Child ID, Nickname, Goal Name, Parent Username, Status, Created Date, Target Amount, and Current Amount.

**Priority:** High  
**Category:** Data Management  

---

#### REQ-1.3: Keyword Search Functionality
**EARS Notation:**  
`Given` the user enters a keyword in the search field, `when` the keyword is submitted, `the system shall` filter the goals list to display only records matching the keyword in Goal Name, Child ID, or Parent Username fields using case-insensitive comparison.

**Priority:** High  
**Category:** Search & Filtering  

---

#### REQ-1.4: Status-Based Filtering
**EARS Notation:**  
`Given` a multiselect filter for Progress Status exists in the sidebar, `when` the user selects one or more status options from ["Active", "Completed", "Pending Approval", "Cancelled", "Rejected", "Expired"], `the system shall` display only goals matching the selected statuses.

**Acceptance Criteria:**
- Default selected statuses: Active, Completed, Pending Approval
- Multiple selections are supported
- Filter updates immediately upon selection change

**Priority:** High  
**Category:** Search & Filtering  

---

#### REQ-1.5: Date Range Filtering
**EARS Notation:**  
`Given` a date range picker is available in the sidebar, `when` the user selects a date range for "Created Date Range", `the system shall` display only goals created within the selected date range inclusive of both start and end dates.

**Default Value:** November 1, 2025 to current date  
**Priority:** Medium  
**Category:** Search & Filtering  

---

#### REQ-1.6: Combined Filter Logic
**EARS Notation:**  
`When` multiple filters (keyword, status, date range) are active simultaneously, `the system shall` apply all filters using AND logic such that only goals satisfying all filter criteria are displayed.

**Priority:** High  
**Category:** Search & Filtering  

---

#### REQ-1.7: Display Filtered Results in Table
**EARS Notation:**  
`When` filters are applied, `the system shall` render the filtered results in a responsive data table using Streamlit's dataframe component with full container width.

**Displayed Columns:** Child ID, Nickname, Goal Name, Parent Username, Status, Created Date, Target, Current  
**Priority:** High  
**Category:** Display  

---

#### REQ-1.8: Export Filtered Data to CSV
**EARS Notation:**  
`Given` the filtered goals are displayed, `when` the user clicks the "📥 Export by Filter (CSV)" button, `the system shall` generate a CSV file containing only the filtered goals and provide a download link.

**Filename Convention:** filtered_report.csv  
**Format:** Comma-separated values with UTF-8 encoding  
**Priority:** Medium  
**Category:** Export/Reporting  

---

#### REQ-1.9: Sidebar Navigation
**EARS Notation:**  
`When` the application initializes, `the system shall` display a sidebar filter section with a professional background color (#F8F9FA) and a left border accent (#0066CC) containing all filter controls.

**Priority:** Medium  
**Category:** UI/UX  

---

### Module 2: Push Notification Logic Tester (PBI 2)

#### REQ-2.1: Display Notification Logic Tester Interface
**EARS Notation:**  
`When` the user navigates to the "PN Logic Tester (PBI 2)" screen, `the system shall` display a header titled "🔔 Push Notification Logic Tester" with an informational message explaining the functionality.

**Priority:** High  
**Category:** UI/UX  

---

#### REQ-2.2: Current Values Input Panel
**EARS Notation:**  
`When` the notification logic tester loads, `the system shall` display a "Current Values" input panel in the left column containing three editable fields: Goal Name, Target Amount, and Target End Date.

**Default Values:**
- Goal Name: "Mountain Bike"
- Target Amount: "S$150"
- Target End Date: June 1, 2026

**Priority:** High  
**Category:** Input  

---

#### REQ-2.3: Previous Values Input Panel
**EARS Notation:**  
`When` the notification logic tester loads, `the system shall` display a "Previous Values (Before Edit)" input panel in the right column containing three editable fields matching the current values structure.

**Default Values:**
- Previous Goal Name: "Bike"
- Previous Target Amount: "S$100"
- Previous Target End Date: June 1, 2026

**Priority:** High  
**Category:** Input  

---

#### REQ-2.4: Goal Name Change Detection
**EARS Notation:**  
`When` the current goal name differs from the previous goal name, `the system shall` include the message: "• The goal name has been changed from {previous_name} to {current_name}." in the edits list.

**Priority:** High  
**Category:** Business Logic  

---

#### REQ-2.5: Target Amount Change Detection
**EARS Notation:**  
`When` the current target amount differs from the previous target amount, `the system shall` include the message: "• The target amount has been changed from {previous_amount} to {current_amount}." in the edits list.

**Priority:** High  
**Category:** Business Logic  

---

#### REQ-2.6: Target End Date Change Detection
**EARS Notation:**  
`When` the current target end date differs from the previous target end date, `the system shall` include the message: "• The end date has been changed from {previous_date} to {current_date}." in the edits list.

**Priority:** High  
**Category:** Business Logic  

---

#### REQ-2.7: Generate Notification Message
**EARS Notation:**  
`When` at least one change is detected between current and previous values, `the system shall` generate a notification message with the format: "Your parent has made some changes to your goal {current_goal_name}! 😊\n\n{list_of_changes}".

**Priority:** High  
**Category:** Business Logic  

---

#### REQ-2.8: Display Live Preview
**EARS Notation:**  
`When` the notification message is generated, `the system shall` display the complete message in a code preview block with markdown language highlighting in the "Live Preview" section.

**Priority:** High  
**Category:** Display  

---

#### REQ-2.9: No Changes Warning
**EARS Notation:**  
`If` no changes are detected between current and previous values, `then` `the system shall` display a warning message stating: "No changes detected. The 'Edit' shortfields are omitted per Business Rule."

**Priority:** Medium  
**Category:** Display  

---

#### REQ-2.10: Dynamic Message Updates
**EARS Notation:**  
`When` the user modifies any input value in either the Current Values or Previous Values panels, `the system shall` automatically recalculate the changes and update the live preview message in real-time without requiring a button click.

**Priority:** High  
**Category:** Interactivity  

---

### Cross-Cutting Requirements

#### REQ-3.1: Professional UI Styling
**EARS Notation:**  
`When` any page element is rendered, `the system shall` apply professional CSS styling using a color scheme with primary color #0066CC, secondary color #003A99, success color #28A745, warning color #FFC107, and danger color #DC3545.

**Priority:** Medium  
**Category:** UI/UX  

---

#### REQ-3.2: Page Configuration
**EARS Notation:**  
`When` the application initializes, `the system shall` configure the Streamlit page with:
- Page title: "PBI Testing Suite"
- Layout: Wide
- Initial sidebar state: Expanded
- Menu items: Disabled

**Priority:** Medium  
**Category:** Configuration  

---

#### REQ-3.3: Navigation Menu
**EARS Notation:**  
`When` the application is running, `the system shall` display a sidebar radio button navigation menu with two options: "Admin Reports (PBI 1)" and "PN Logic Tester (PBI 2)" allowing users to switch between modules.

**Priority:** High  
**Category:** Navigation  

---

#### REQ-3.4: Data Persistence
**EARS Notation:**  
`When` a user switches between modules or refreshes the application, `the system shall` reload mock data from the data source ensuring consistency and preventing data loss.

**Priority:** Medium  
**Category:** Data Management  

---

#### REQ-3.5: Responsive Design
**EARS Notation:**  
`When` the application window is resized, `the system shall` maintain responsive layout behavior using Streamlit's column and container components ensuring usability on various screen sizes.

**Priority:** Medium  
**Category:** UI/UX  

---

## Data Model

### Goals Entity

| Attribute | Data Type | Constraints |
|-----------|-----------|-------------|
| Child ID | String | Unique, Required |
| Nickname | String | Required |
| Goal Name | String | Required, Max 100 chars |
| Parent Username | String | Required |
| Status | Enum | One of: Active, Completed, Pending Approval, Cancelled, Rejected, Expired |
| Created Date | Date | Required |
| Target | Decimal | Required, > 0 |
| Current | Decimal | Required, >= 0, <= Target |

### Status Codes

| Status | Description |
|--------|-------------|
| Active | Goal is currently in progress |
| Completed | Goal has reached the target amount |
| Pending Approval | Goal awaiting parent approval |
| Cancelled | Goal was cancelled by parent |
| Rejected | Goal was rejected by admin |
| Expired | Goal has passed its target end date without completion |

---

## Non-Functional Requirements

#### NFR-1: Performance
**EARS Notation:**  
`When` filters are applied to goals list containing up to 1000 records, `the system shall` update the display within 2 seconds.

**Priority:** High  

---

#### NFR-2: Usability
**EARS Notation:**  
`When` a user interacts with the application, `the system shall` provide immediate visual feedback for all actions including button clicks, filter selections, and data exports.

**Priority:** High  

---

#### NFR-3: Data Export Security
**EARS Notation:**  
`When` data is exported to CSV, `the system shall` encode all data using UTF-8 and ensure no sensitive parent credentials are included in the export file.

**Priority:** High  

---

#### NFR-4: Browser Compatibility
**EARS Notation:**  
`When` the application is accessed, `the system shall` support modern web browsers including Chrome, Firefox, Safari, and Edge with versions released within the last 24 months.

**Priority:** Medium  

---

## User Stories Summary

### PBI 1: Admin Goal Management
As an admin user, I need to view and filter child savings goals so that I can monitor progress, generate reports, and manage the system effectively.

**Acceptance Criteria:**
- Filter by keyword across multiple fields
- Filter by goal status with multiple selection
- Filter by goal creation date range
- Export filtered results to CSV
- Display all results in an organized table format

### PBI 2: Push Notification Template Tester
As a developer, I need to test push notification logic so that I can ensure parents receive accurate update messages when goals are edited, showing only the fields that actually changed.

**Acceptance Criteria:**
- Compare current and previous goal values
- Dynamically generate notification messages
- Show only changed fields in the notification
- Display live preview of generated messages
- Handle scenarios with no changes gracefully

---

## Glossary

| Term | Definition |
|------|-----------|
| Admin User | Administrator with access to goal management tools |
| Mock Data | Sample data used for testing and demonstration |
| CSV Export | Comma-separated values file format for data export |
| Live Preview | Real-time display of generated content without save/refresh |
| Goal Status | Current state of a child's savings goal |
| Target Amount | Desired savings amount for a goal |
| Parent | User who manages child's goals and savings |
| Child | User whose savings goals are being tracked |

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | January 22, 2026 | AI Assistant | Initial specification document with EARS notation |

---

## Document Approval

This document is subject to review and approval by the following stakeholders:

- [ ] Product Manager
- [ ] Development Lead
- [ ] QA Lead
- [ ] Business Owner

---

**End of Document**
