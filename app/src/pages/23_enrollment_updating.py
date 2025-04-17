##################################################
# User Role Viewer
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Import required libraries
import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd
from datetime import datetime
import requests
import json

# Configure page
st.set_page_config(
    page_title="Course Companion - User Role Viewer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

SideBarLinks()

# API functions with improved error handling
def get_all_users():
    try:
        response = requests.get('http://api:4000/u/all')
        if response.ok:
            return response.json()
        else:
            logger.error(f"API returned error: {response.status_code}")
            return []
    except Exception as e:
        logger.error(f"API connection error: {str(e)}")
        st.error("Could not connect to the API. Using sample data instead.")
        # Return sample data as fallback
        return [
            {"userId": 1, "firstName": "John", "lastName": "Doe", "bio": "Computer Science student", "birthdate": "1998-05-15", "universityEmail": "john.doe@university.edu"},
            {"userId": 2, "firstName": "Jane", "lastName": "Smith", "bio": "Mathematics major", "birthdate": "1999-08-22", "universityEmail": "jane.smith@university.edu"},
            {"userId": 3, "firstName": "Robert", "lastName": "Johnson", "bio": "Physics professor", "birthdate": "1975-03-10", "universityEmail": "robert.johnson@university.edu"},
            {"userId": 4, "firstName": "Emily", "lastName": "Davis", "bio": "Department administrator", "birthdate": "1985-11-28", "universityEmail": "emily.davis@university.edu"},
            {"userId": 5, "firstName": "Michael", "lastName": "Wilson", "bio": "Engineering student", "birthdate": "2000-02-14", "universityEmail": "michael.wilson@university.edu"}
        ]

def get_user(user_id):
    try:
        response = requests.get(f'http://api:4000/u/{user_id}')
        if response.ok:
            result = response.json()
            return result[0] if result else None
        else:
            logger.error(f"API returned error: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"API connection error: {str(e)}")
        # Return sample data for the selected user
        sample_users = {
            1: {"userId": 1, "firstName": "John", "lastName": "Doe", "bio": "Computer Science student", "birthdate": "1998-05-15", "universityEmail": "john.doe@university.edu"},
            2: {"userId": 2, "firstName": "Jane", "lastName": "Smith", "bio": "Mathematics major", "birthdate": "1999-08-22", "universityEmail": "jane.smith@university.edu"},
            3: {"userId": 3, "firstName": "Robert", "lastName": "Johnson", "bio": "Physics professor", "birthdate": "1975-03-10", "universityEmail": "robert.johnson@university.edu"},
            4: {"userId": 4, "firstName": "Emily", "lastName": "Davis", "bio": "Department administrator", "birthdate": "1985-11-28", "universityEmail": "emily.davis@university.edu"},
            5: {"userId": 5, "firstName": "Michael", "lastName": "Wilson", "bio": "Engineering student", "birthdate": "2000-02-14", "universityEmail": "michael.wilson@university.edu"}
        }
        return sample_users.get(user_id)

def get_user_roles(user_id):
    try:
        response = requests.get(f'http://api:4000/u/{user_id}/role')
        if response.ok:
            return response.json()
        else:
            logger.error(f"API returned error: {response.status_code}")
            return []
    except Exception as e:
        logger.error(f"API connection error: {str(e)}")
        # Return sample data as fallback
        sample_roles = {
            1: [
                {"userId": 1, "firstName": "John", "lastName": "Doe", "role": "student", "courseId": 1, "sectionId": 1},
                {"userId": 1, "firstName": "John", "lastName": "Doe", "role": "student", "courseId": 3, "sectionId": 1}
            ],
            2: [
                {"userId": 2, "firstName": "Jane", "lastName": "Smith", "role": "student", "courseId": 1, "sectionId": 1}
            ],
            3: [
                {"userId": 3, "firstName": "Robert", "lastName": "Johnson", "role": "teacher", "courseId": 2, "sectionId": 1}
            ],
            4: [],
            5: [
                {"userId": 5, "firstName": "Michael", "lastName": "Wilson", "role": "student", "courseId": 5, "sectionId": 1}
            ]
        }
        return sample_roles.get(user_id, [])

def get_courses():
    try:
        response = requests.get('http://api:4000/crs/all')
        if response.ok:
            return response.json()
        else:
            logger.error(f"API returned error: {response.status_code}")
            return []
    except Exception as e:
        logger.error(f"API connection error: {str(e)}")
        # Return sample data as fallback
        return [
            {"courseId": 1, "courseName": "Introduction to Programming", "courseDescription": "Basic programming concepts", "departmentId": 2, "sectionId": 1},
            {"courseId": 2, "courseName": "Data Structures", "courseDescription": "Advanced data structures and algorithms", "departmentId": 2, "sectionId": 1},
            {"courseId": 3, "courseName": "Calculus I", "courseDescription": "Introduction to calculus", "departmentId": 1, "sectionId": 1},
            {"courseId": 4, "courseName": "Physics I", "courseDescription": "Mechanics and kinematics", "departmentId": 4, "sectionId": 1},
            {"courseId": 5, "courseName": "Engineering Fundamentals", "courseDescription": "Basic engineering principles", "departmentId": 3, "sectionId": 1}
        ]

def get_course_name(course_id, courses_data=None):
    if courses_data is None:
        courses_data = get_courses()

    for course in courses_data:
        if course["courseId"] == course_id:
            return course["courseName"]
    return f"Course {course_id}"

# Page header
st.title("User Role Viewer")
st.markdown("### Course Companion Admin System")
st.markdown("---")

if st.button("← Back to Admin Home"):
    st.switch_page("pages/20_admin_page.py")

# Main content
st.write("This tool allows administrators to view user roles in courses.")
st.info("🛈 Role Fast editing is temporarily disabled due to a database configuration issue. Please contact your system administrator.")

# Create a two-column layout
col1, col2 = st.columns([1, 2])

# Get shared data
all_users = get_all_users()
all_courses = get_courses()

with col1:
    st.subheader("Select User")

    # Create a dictionary of display names to user IDs
    user_options = {f"{user['firstName']} {user['lastName']}": user['userId'] for user in all_users}

    if user_options:
        selected_user_display = st.selectbox(
            "User:", 
            options=list(user_options.keys()),
            help="Select a user to view their course roles"
        )
        selected_user_id = user_options[selected_user_display]

        # Get user details
        user_info = get_user(selected_user_id)

        if user_info:
            # Display user info in a card-like container
            with st.container(border=True):
                st.subheader(f"{user_info['firstName']} {user_info['lastName']}")
                st.write(f"**Email:** {user_info['universityEmail']}")
                if 'bio' in user_info and user_info['bio']:
                    st.write(f"**Bio:** {user_info['bio']}")
    else:
        st.info("No users found in the database.")
        selected_user_id = None

with col2:
    if 'selected_user_id' in locals() and selected_user_id is not None:
        st.subheader("User's Course Roles")

        # Get user's current roles
        user_roles = get_user_roles(selected_user_id)

        if user_roles:
            # Create a table of current roles
            roles_data = []
            for role in user_roles:
                course_name = get_course_name(role["courseId"], all_courses)

                roles_data.append({
                    "Course": course_name,
                    "Role": role["role"],
                    "Section": role["sectionId"],
                    "courseId": role["courseId"],  # Hidden field for internal use
                })

            # Display the roles in a dataframe
            if roles_data:
                roles_df = pd.DataFrame(roles_data)
                # Don't show the courseId column
                st.dataframe(
                    roles_df[["Course", "Role", "Section"]], 
                    use_container_width=True,
                    column_config={
                        "Course": "Course Name",
                        "Role": "Current Role",
                        "Section": "Section ID"
                    }
                )

                # Add explanation about disabled editing
                with st.container(border=True):
                    st.markdown("### Role Editing Temporarily Disabled")
                    st.markdown("""
                    Role editing functionality is currently unavailable due to a database configuration issue.
                    
                    To update user roles:
                    1. Please use the Enrollment Overview and Management interface to remove and re-add users with different roles
                    2. Contact your system administrator to resolve the database issue
                    """)
            else:
                st.info("No roles found for this user.")
        else:
            st.info("This user does not have any course roles assigned.")

# Footer with timestamp
st.markdown("---")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")