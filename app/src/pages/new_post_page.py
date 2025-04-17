import logging
from typing import Any, Dict
import requests
import streamlit as st
from modules.nav import SideBarLinks
from pages.course_feed_page import add_ret_to_home_button

logger = logging.getLogger(__name__)

# Set this page as the active page
st.session_state["active_page"] = "new_post_page"

# Display the appropriate sidebar links and buttons for the role of the logged in user
add_ret_to_home_button()
SideBarLinks()

# TODO: Refactor actually retrieve from sesion state
st.session_state["active_user_id"] = 1
 

# Create an expander to add a new post that reveals an web form
with st.expander("What's on your mind?"):
    with st.form("create_new_post_form"):
        
        # Take the post title, announcement boolean, and content from the user input
        title : str = st.text_input("Title")
        isAnnouncement : bool = st.checkbox("Is this an announcement?")
        content : str = st.text_area("Content", placeholder="Write post content here")

        submit_button = st.form_submit_button("Create post") 
        
        # When the form is submitted, create a new post by combining the user-inputted
        # data with the session state metadata on the active user and active course
        if submit_button:
            post_data : Dict[str, Any]= {
                "title" : title,
                "content":content,
                "isAnnouncement" : isAnnouncement,
                "authorId": st.session_state["active_user_id"],
                "courseId": st.session_state["active_course_id"],
                "sectionId": st.session_state["active_section_id"]
            }
            # Send a POST request to our /posts/create endpoint
            response : Dict[str, Any] = requests.post(
                "http://api:4000/po/posts/create",
                json=post_data,
                headers={"Content-Type" : "application/json"}
            )
            
            st.write(response.json())