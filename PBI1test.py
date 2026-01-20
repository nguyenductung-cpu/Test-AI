import pandas as pd
from datetime import datetime, timedelta

class GoalManagementSystem:
    def __init__(self, goals_df, activities_df):
        """
        Initializes the system with DataFrames for Goal Status and Goal Activity.
        """
        self.goals_df = goals_df
        self.activities_df = activities_df
        self.valid_statuses = ['Completed', 'Active', 'Pending Approval', 'Cancelled', 'Rejected', 'Expired']

    def _apply_keyword_search(self, df, keyword):
        """
        Rule: Case-insensitive, partial match for Goal Name, Child ID, Parent ID, 
        Child Nickname, Parent Username, and Child Access.
        """
        if not keyword:
            return df
        
        keyword = str(keyword).lower()
        search_cols = ['Goal Name', 'Child ID', 'Parent ID', 'Child Nickname', 'Parent Username', 'Child Access']
        
        # Filter columns that actually exist in the dataframe
        available_cols = [col for col in search_cols if col in df.columns]
        
        mask = df[available_cols].apply(
            lambda row: row.astype(str).str.lower().str.contains(keyword).any(), axis=1
        )
        return df[mask]

    def _apply_date_filter(self, df, date_col, start_date, end_date):
        """
        Rule: Filters data within a specific date range.
        Format expected: DD-MM-YYYY
        """
        df[date_col] = pd.to_datetime(df[date_col], dayfirst=True)
        start = pd.to_datetime(start_date, dayfirst=True)
        end = pd.to_datetime(end_date, dayfirst=True)
        
        return df[(df[date_col] >= start) & (df[date_col] <= end)]

    def get_default_date_range(self):
        """
        Rule: Default the range to "Start from today backward 1 month."
        """
        today = datetime.now()
        one_month_ago = today - timedelta(days=30)
        return one_month_ago.strftime('%d-%m-%Y'), today.strftime('%d-%m-%Y')

    def filter_goals_status(self, keyword=None, start_date=None, end_date=None, statuses=None):
        """
        Filters the Goals Status report.
        """
        filtered_df = self.goals_df.copy()
        
        # Keyword Search
        filtered_df = self._apply_keyword_search(filtered_df, keyword)
        
        # Date Filter (Created Date)
        if start_date and end_date:
            filtered_df = self._apply_date_filter(filtered_df, 'Created Date', start_date, end_date)
            
        # Progress Status Filter (Multiple selection)
        if statuses:
            # Ensure statuses are within the valid list
            selected_statuses = [s for s in statuses if s in self.valid_statuses]
            filtered_df = filtered_df[filtered_df['Progress Status'].isin(selected_statuses)]
            
        return filtered_df

    def filter_goals_activity(self, keyword=None, start_date=None, end_date=None):
        """
        Filters the Goals Activity report.
        Rule: Default sort by the latest transaction date and time.
        """
        filtered_df = self.activities_df.copy()
        
        # Keyword Search
        filtered_df = self._apply_keyword_search(filtered_df, keyword)
        
        # Date Filter (Transaction Date & Time)
        if start_date and end_date:
            filtered_df = self._apply_date_filter(filtered_df, 'Transaction Date & Time', start_date, end_date)
            
        # Default Sorting
        filtered_df['Transaction Date & Time'] = pd.to_datetime(filtered_df['Transaction Date & Time'], dayfirst=True)
        filtered_df = filtered_df.sort_values(by='Transaction Date & Time', ascending=False)
        
        return filtered_df

    def validate_and_export(self, filtered_df, is_all=False, date_range_applied=False):
        """
        Rule: Time Range filter mandatory for exporting data.
        Rule: Options for "Export by filter" and "Export all".
        """
        if not date_range_applied and not is_all:
            raise ValueError("Mandatory Export Validation: A date range filter must be applied to export by filter.")
        
        # Logic to generate CSV/Excel file
        file_path = "goal_report_export.csv"
        filtered_df.to_csv(file_path, index=False)
        return f"Report exported successfully to {file_path}"

# Example Usage:
# goals_data = pd.DataFrame(...) 
# activity_data = pd.DataFrame(...)
# system = GoalManagementSystem(goals_data, activity_data)
# results = system.filter_goals_status(keyword="bike", statuses=["Active", "Completed"])