##################################################
# User Role Editor
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
    page_title="Course Companion - User Role Editor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

SideBarLinks()

# API functions with fallback mechanism
def get_all_users():
    try:
        # Try using api container name for Docker or localhost for local development
        try:
            response = requests.get('http://api:4000/u/all')
            return response.json()
        except:
            response = requests.get('http://localhost:4000/u/all')
            return response.json()
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
        # Try using api container name for Docker or localhost for local development
        try:
            response = requests.get(f'http://api:4000/u/{user_id}')
            result = response.json()
            return result[0] if result else None
        except:
            response = requests.get(f'http://localhost:4000/u/{user_id}')
            result = response.json()
            return result[0] if result else None
    except Exception as e:
        logger.error(f"API connection error: {str(e)}")
        st.error("Could not connect to the API. Using sample data instead.")
        # Return sample data as fallback for the selected user
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
        # Try using api container name for Docker or localhost for local development
        try:
            response = requests.get(f'http://api:4000/u/{user_id}/role')
            return response.json()
        except:
            response = requests.get(f'http://localhost:4000/u/{user_id}/role')
            return response.json()
    except Exception as e:
        logger.error(f"API connection error: {str(e)}")
        st.error("Could not connect to the API. Using sample data instead.")
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

def add_user_role(user_id, role, course_id, section_id):
    try:
        data = {
            "user_role": role,
            "user_course": course_id,
            "user_section": section_id
        }
        # Try using api container name for Docker or localhost for local development
        try:
            response = requests.post(f'http://api:4000/u/{user_id}/create/role', json=data)
            return response.status_code == 200
        except:
            response = requests.post(f'http://localhost:4000/u/{user_id}/create/role', json=data)
            return response.status_code == 200
    except Exception as e:
        logger.error(f"API connection error: {str(e)}")
        st.error("Could not connect to the API. Operation not completed.")
        return False

def remove_user_role(user_id, course_id, section_id):
    try:
        data = {
            "user_course": course_id,
            "user_section": section_id
        }
        # Try using api container name for Docker or localhost for local development
        try:
            response = requests.delete(f'http://api:4000/u/{user_id}/delete/role', json=data)
            return response.status_code == 200
        except:
            response = requests.delete(f'http://localhost:4000/u/{user_id}/delete/role', json=data)
            return response.status_code == 200
    except Exception as e:
        logger.error(f"API connection error: {str(e)}")
        st.error("Could not connect to the API. Operation not completed.")
        return False

def get_courses():
    try:
        # Try using api container name for Docker or localhost for local development
        try:
            response = requests.get('http://localhost:4000/crs/all')
            return response.json()
        except:
            response = requests.get('')
            return response.json()
    except Exception as e:
        logger.error(f"API connection error: {str(e)}")
        st.error("Could not connect to the API for courses. Using sample data instead.")
        # Return sample data as fallback
        return [
            {"courseId": 1, "courseName": "Introduction to Programming"},
            {"courseId": 2, "courseName": "Data Structures"},
            {"courseId": 3, "courseName": "Calculus I"},
            {"courseId": 4, "courseName": "Physics I"},
            {"courseId": 5, "courseName": "Engineering Fundamentals"}
        ]

# Helper functions
def get_course_name(course_id):
    courses = get_courses()
    for course in courses:
        if course["courseId"] == course_id:
            return course["courseName"]
    return f"Course {course_id}"

# Page header
st.title("User Role Editor")
st.markdown("### Course Companion Admin System")
st.markdown("---")

if st.button("← Back to Admin Home"):
    st.switch_page("pages/20_admin_page.py")

# Main content
st.write("This tool allows administrators to manage user roles in courses.")

# Create a three-column layout
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.subheader("Select User")
    
    # Get all users from API
    all_users = get_all_users()
    
    # Create a dictionary of display names to user IDs
    user_options = {f"{user['firstName']} {user['lastName']}": user['userId'] for user in all_users}
    
    if user_options:
        selected_user_display = st.selectbox("User:", options=list(user_options.keys()))
        selected_user_id = user_options[selected_user_display]
        
        # Get user details
        user_info = get_user(selected_user_id)
        
        if user_info:
            st.write(f"**Email:** {user_info['universityEmail']}")
            if 'bio' in user_info and user_info['bio']:
                st.write(f"**Bio:** {user_info['bio']}")
    else:
        st.info("No users found in the database.")
        selected_user_id = None

with col2:
    if 'selected_user_id' in locals() and selected_user_id is not None:
        st.subheader("Current Course Roles")
        
        # Get user's current roles
        user_roles = get_user_roles(selected_user_id)
        
        if user_roles:
            # Create a table of current roles
            roles_data = []
            for role in user_roles:
                course_name = get_course_name(role["courseId"])
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
                st.dataframe(roles_df[["Course", "Role", "Section"]], use_container_width=True)
                
                # Add a way to select a role to remove
                st.subheader("Remove Role")
                
                # Create options for each role
                role_options = {f"{r['Course']} (Section {r['Section']})": (r["courseId"], r["Section"]) for r in roles_data}
                
                if role_options:
                    selected_role_display = st.selectbox("Select role to remove:", options=list(role_options.keys()))
                    selected_course_id, selected_section_id = role_options[selected_role_display]
                    
                    if st.button("Remove Selected Role"):
                        with st.spinner("Removing role..."):
                            success = remove_user_role(selected_user_id, selected_course_id, selected_section_id)
                            if success:
                                st.success(f"Role removed successfully!")
                                st.rerun()
                            else:
                                st.error("Failed to remove role. Please try again.")
            else:
                st.info("No roles found for this user.")
        else:
            st.info("This user does not have any course roles assigned.")

with col3:
    if 'selected_user_id' in locals() and selected_user_id is not None:
        st.subheader("Add New Role")
        
        # Get all courses
        all_courses = get_courses()
        
        # Get user's current roles
        user_roles = get_user_roles(selected_user_id)
        
        # Extract course IDs that the user is already enrolled in
        enrolled_course_ids = set()
        for role in user_roles:
            enrolled_course_ids.add(role["courseId"])
        
        # Filter out courses the user is already enrolled in
        available_courses = [course for course in all_courses if course["courseId"] not in enrolled_course_ids]
        
        if available_courses:
            with st.form("add_role_form"):
                # Course selection
                course_options = {course["courseName"]: course["courseId"] for course in available_courses}
                selected_course = st.selectbox("Course:", options=list(course_options.keys()))
                course_id = course_options[selected_course]
                
                # Role selection
                role_options = ["student", "TA", "teacher"]
                role = st.selectbox("Role:", options=role_options)
                
                # Section selection
                section = st.number_input("Section:", min_value=1, value=1)
                
                # Submit button
                submitted = st.form_submit_button("Add Role")
                
                if submitted:
                    with st.spinner("Adding role..."):
                        success = add_user_role(selected_user_id, role, course_id, section)
                        if success:
                            st.success("Role added successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to add role. Please try again.")
        else:
            st.info("This user is already enrolled in all available courses.")

st.markdown("---")
st.caption("Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))