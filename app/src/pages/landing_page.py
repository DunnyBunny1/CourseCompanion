# Set up basic logging infrastructure

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks

SideBarLinks()

import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

st.markdown(f"### Welcome, {st.session_state['persona']}")


def display_course_feed_button():
    if st.button("Course Feed Page", 
                type = 'primary', 
                use_container_width=True):
        logger.info("Visiting the course feed page...")
        st.switch_page('pages/course_feed_page.py')

def display_admin_page_button(): 
    if st.button('Admin Page', 
                type = 'primary', 
                use_container_width=True):
        st.switch_page('pages/20_admin_page.py')

def display_analytics_page_button(): 
    if st.button('Dashboard Analytics', 
                type = 'primary', 
                use_container_width=True):
        st.switch_page('pages/dashboard_analytics.py')
        
        
# Display the buttons for the pages that the signed in user persona
# is allowed to view 
# Students have access to the course feed page 
if st.session_state["persona"] == "Bob":
    st.write(f"You are allowed to view the course feed page")
    display_course_feed_button()
    
# Admins have access to both the analytics and admin pages
elif st.session_state["persona"] == "Veronica":
    st.write(f"You are allowed to view the analytics & admin pages")
    display_analytics_page_button()
    display_admin_page_button()
    
# Teachers have access to both the course feed and analytics
elif st.session_state["persona"] == "Prof. James":
    st.write(f"You are allowed to view the course feed & analytics pages")    
    display_course_feed_button()
    display_analytics_page_button()

# Teaching Assistants have access to both the course feed and analytics
elif st.session_state["persona"] == "Jane":
    st.write(f"You are allowed to view the course feed & analytics pages")    
    display_course_feed_button()
    display_analytics_page_button()
    