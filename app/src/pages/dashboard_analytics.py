from typing import List, Dict, Any, Tuple
import pandas as pd
import requests 
import streamlit as st 
from modules.nav import SideBarLinks

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()
st.write("Welcome to the dashboard feed pages")

# Create a base url for all analytics requests
BASE_URL = "http://api:4000/stats"  

def send_analytics_get_req(endpoint: str) -> List[Dict[str, Any]]:
    """
    Sends a GET request to the given analytics endpoint w/ error handling
    """
    url = f"{BASE_URL}/{endpoint}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except Exception as e:
        st.error(f"Error fetching data from {endpoint} {e}")
        return []

# App title and description
st.title("Learning Platform Analytics Dashboard")
st.markdown("This dashboard displays key metrics from the learning platform.")

# Create tabs for different analytics sections in the following order:
tab1, tab2, tab3, tab4 = st.tabs([
    "Role Distribution", 
    "Active Hours", 
    "Engagement",
    "System-wide Averages",
])

# Tab 1: Role distro 
with tab1:
    st.header("User Role Distribution")
    # Fetch our role distro data and data bar char
    role_data = send_analytics_get_req("role-distribution")
    
    df_roles = pd.DataFrame(role_data)
    st.bar_chart(df_roles.set_index('role'))

# Tab 2: Active Hours
with tab2:
    st.header("Most Active Hours")
    
    # Retrieve our active hours data
    active_hours_data = send_analytics_get_req("active-hours")
    
    if active_hours_data:
        # Convert our JSON data to a DF and draw a table of it
        df_hours = pd.DataFrame(active_hours_data)
        
        # Draw a table 
        st.table(df_hours)

# Tab 3: Engagement
with tab3:
    st.header("Engagement Analytics")
    
    # Fetch engagement data (tags in this case)
    engagement_data = send_analytics_get_req("engagement")
    
    if engagement_data:
        # Convert to DataFrame
        df_tags = pd.DataFrame(engagement_data)
        
        # Display the data table
        st.subheader("Available Tags")
        st.dataframe(df_tags)
        
# Tab 4 : Section averages
with tab4:
    st.header("Avg Metrics across all course sections")
    
    # Fetch avg enrollment data
    avg_enrollment_data = send_analytics_get_req("avg-enrollment")
    
    if avg_enrollment_data:
        # Convert our JSON data to a DF and draw a table of it
        df_enrollment = pd.DataFrame(avg_enrollment_data)
        st.table(df_enrollment)
        
    # Fetch avg enrollment data
    avg_post_data = send_analytics_get_req("avg-posts")
    
    if avg_post_data:
        # Convert our JSON data to a DF and draw a table of it
        df_posts = pd.DataFrame(avg_post_data)
        st.table(df_posts)