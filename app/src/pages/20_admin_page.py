##################################################
# Admin Page for Course Companion
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Import required libraries
import streamlit as st
from modules.nav import SideBarLinks

# Configure page
st.set_page_config(
    page_title="Course Companion - Admin",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set up navigation
SideBarLinks()

# Page header
st.title("Course Companion Admin")
st.markdown("### System Administration Dashboard")

# Main content
st.markdown("""
Welcome to the Course Companion administration interface. 
Select an administrative function from the options below:
""")

# Create columns for the admin options
col1, col2 = st.columns(2)

with col1:
    # Department & Course Management
    st.markdown("### Departments & Courses")
    st.markdown("Manage academic departments and course offerings.")
    if st.button("Manage Departments & Courses", use_container_width=True, type="primary"):
        logger.info("Navigating to Department & Course management")
        st.switch_page("pages/21_admin_departments_courses.py")
    
    # User Management
    st.markdown("### Enrollment Overview and Management")
    st.markdown("Add or remove users and manage roles.")
    if st.button("Manage Users", use_container_width=True, type="primary"):
        logger.info("Navigating to User management")
        st.switch_page("pages/22_enrollment_management.py")

with col2:
    # Enrollment Management
    st.markdown("### User Role Editor")
    st.markdown("Control which users are enrolled in each course.")
    if st.button("Manage Enrollments", use_container_width=True, type="primary"):
        logger.info("Navigating to Enrollment management")
        st.switch_page("pages/23_enrollment_updating.py")
    
# Show the course companion logo
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("assets/course-companion-logo.svg", width=300)

# Footer
st.markdown("---")
