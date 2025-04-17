##################################################
# This is the main/entry-point file for the 
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks

# streamlit supports reguarl and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(layout = 'wide')

# If a user is at this page, we assume they are not 
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false. 
st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel. 
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
SideBarLinks()

# ***************************************************
#    The major content of this page
# ***************************************************

# set the title of the page and provide a simple prompt. 
logger.info("Loading the Home page of the app")
st.title('Welcome to Course Companion :)')
st.write('\n\n')
st.write('### HI! Which page would you like to visit?')

# Show the course companion logo logo 
# Center the image with Streamlit's layout options
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image("assets/course-companion-logo.svg", width=500)


if st.button("Course Feed Page", 
            type = 'primary', 
            use_container_width=True):
    logger.info("Visiting the course feed page...")
    st.switch_page('pages/course_feed_page.py')

if st.button('Admin Page', 
            type = 'primary', 
            use_container_width=True):
    st.switch_page('pages/20_admin_page.py')

if st.button('Dashboard Analytics', 
            type = 'primary', 
            use_container_width=True):
    st.switch_page('pages/dashboard_analytics.py')



