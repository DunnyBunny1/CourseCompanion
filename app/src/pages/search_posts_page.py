from typing import Tuple, List, Dict, Optional, Any
from pprint import pformat
from datetime import datetime 
import logging
from matplotlib import pyplot as plt
import pandas as pd

import streamlit as st
from modules.nav import SideBarLinks
from pages.course_feed_page import add_ret_to_home_button
import requests

logger = logging.getLogger(__name__)

# Set this page as the active page
st.session_state["active_page"] = "search_posts_page"

# Display the appropriate sidebar links and buttons for the role of the logged in user
add_ret_to_home_button()
SideBarLinks()

 
# Create an expander to add a new post that reveals a web form
with st.expander("Run a search query"):
    with st.form("search_query_form"):
        # Take different seach terms from the user input form - if
        # nothing is provided, we get the empty string / False
        title_keywords : str = st.text_input("Title Keywords")
        content_keywords : str = st.text_input("Content Keywords")
        
        # Make the date filters both optional
        use_created_date = st.checkbox("Filter by creation date")
        if use_created_date:
            created_at = st.date_input("Created-at date")
        else: 
            created_at = None
            
        use_updated_at = st.checkbox("Filter by updated-at date")
        if use_updated_at:
            updated_at = st.date_input("Updated-at date")
        else: 
            updated_at = None
        
        submit_button = st.form_submit_button("Search posts") 
        
        # When the form is submitted, create a new queyr by combining the user-inputted
        # data with the session state metadata on the active user and active course
        if submit_button:
            # Create our base search for the required search teerm s 
            query_param_data : Dict[str, Any]= {
                "courseId": st.session_state["active_course_id"],
                "sectionId": st.session_state["active_section_id"],
            }
            
            # Add optional search terms if present
            if title_keywords: 
                query_param_data.update({"title" : title_keywords})
            if content_keywords: 
                query_param_data.update({"content" : content_keywords})
            if created_at: 
                query_param_data.update({"createdAt" : created_at})
            if updated_at: 
                query_param_data.update({"updatedAt" : updated_at})
            # Send a GET request to our /posts - this is our search endpoint - our
            # search criteria is inside the query params 
            response : Dict[str, Any] = requests.get(
                "http://api:4000/po/posts",
                params=query_param_data,
            ).json()
            
            # st.write(response.json())
            # Check if the response contains posts and convert to DataFrame
            if response and isinstance(response, list) and len(response) > 0:
                # Convert the JSON data to a DataFrame
                df = pd.DataFrame(response)
                
                # Display the DataFrame with pagination
                st.subheader("Search Results (DataFrame View)")
                
                # Select the most relevant columns to display
                display_columns = ['title', 'content', 'createdAt']
                display_columns = [col for col in display_columns if col in df.columns]
                
                if len(display_columns) > 0:
                    st.dataframe(df[display_columns])
                else:
                    st.dataframe(df)
                
                # Display number of results found
                st.success(f"Found {len(df)} results matching your search criteria.")
            else:
                st.warning("No results found matching your search criteria.")