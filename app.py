import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(page_title="Employee Shift Tracker", layout="wide")

st.title("🕒 Employee Overtime & Shift Tracker")

# Load Data (Replace with your GitHub raw URL or local path)
@st.cache_data
def load_data():
    # Example: df = pd.read_excel("your_github_raw_url_here.xlsx")
    df = pd.read_excel("employee_shifts.xlsx")
    
    # Mapping shift durations
    shift_hours = {'A': 6, 'B': 8, 'C': 10}
    df['Total Hours'] = df['Shift Type'].map(shift_hours)
    
    # Ensure date is in a readable format
    df['Shift Date'] = pd.to_datetime(df['Shift Date']).dt.date
    return df

try:
    df = load_data()

    # Sidebar Search
    st.sidebar.header("Search Filters")
    search_type = st.sidebar.radio("Search by:", ["Employee Name", "Employee Code"])
    query = st.sidebar.text_input(f"Enter {search_type}")

    if query:
        # Filtering logic
        if search_type == "Employee Code":
            # Handle numeric search
            filtered_df = df[df['Employee Code'].astype(str).str.contains(query)]
        else:
            # Handle name search (case-insensitive)
            filtered_df = df[df['Employee Name'].str.contains(query, case=False, na=False)]

        if not filtered_df.empty:
            # Display Metrics
            total_hrs = filtered_df['Total Hours'].sum()
            st.metric(label=f"Total Hours for '{query}'", value=f"{total_hrs} hrs")

            # Display Table
            st.subheader("Shift Details")
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.warning("No records found for that search.")
    else:
        st.info("👈 Enter an Employee Name or Code in the sidebar to begin.")
        st.subheader("All Shift Records")
        st.write(df)

except Exception as e:
    st.error(f"Error loading file: {e}")
    st.info("Make sure 'employee_shifts.xlsx' is in the same folder as this script.")
