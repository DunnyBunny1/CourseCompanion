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
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Course Companion - Enrollment Role Updating",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set up navigation
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
            response = requests.get('http://api:4000/crs/all')
            return response.json()
        except:
            response = requests.get('http://localhost:4000/crs/all')
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
def get_course_name(course_id, section_id):
    courses = get_courses()
    for course in courses:
        if course["courseId"] == course_id and course["sectionId"] == section_id:
            return course["courseName"]
    return f"Course {course_id} (Section {section_id})"


def format_user_display_name(user):
    return f"{user['firstName']} {user['lastName']}"

# Page header
st.title("Enrollment Role Updating")
st.markdown("### Course Companion Admin System")
st.markdown("---")

# Back button
if st.button("← Back to Admin Home"):
    st.switch_page("pages/20_admin_page.py")

# Get all users from API
all_users = get_all_users()

# Convert to a more usable format
users_list = []
for user in all_users:
    users_list.append({
        "userId": user["userId"],
        "firstName": user["firstName"],
        "lastName": user["lastName"],
        "email": user["universityEmail"],
        "displayName": f"{user['firstName']} {user['lastName']}"
    })

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Select User")
    
    # We don't have a global role in the DB schema from what we can see
    user_options = {user["displayName"]: user["userId"] for user in users_list}
    
    if user_options:
        selected_user_display = st.selectbox("Select User", options=list(user_options.keys()))
        selected_user_id = user_options[selected_user_display]
    else:
        st.info("No users found in the database.")
        selected_user_id = None

with col2:
    if selected_user_id is not None:
        # Get user details
        user_info = get_user(selected_user_id)
        
        if user_info:
            st.subheader(f"Edit Enrollments for {user_info['firstName']} {user_info['lastName']}")
            st.markdown(f"**Email:** {user_info['universityEmail']}")
            if 'bio' in user_info and user_info['bio']:
                st.markdown(f"**Bio:** {user_info['bio']}")
            
            # Get user's course roles
            user_roles = get_user_roles(selected_user_id)
            
            with st.expander("Course Enrollments", expanded=True):
                if user_roles:
                    st.subheader("Current Course Enrollments")
                    for role in user_roles:
                        col_course, col_role, col_section, col_action = st.columns([2, 1, 1, 1])
                        with col_course:
                            course_name = get_course_name(role["courseId"], role["sectionId"])
                            st.write(f"**{course_name}**")
                        with col_role:
                            st.write(f"Role: {role['role']}")
                        with col_section:
                            st.write(f"Section: {role['sectionId']}")
                        with col_action:
                            if st.button(f"Remove", key=f"remove_{role['courseId']}_{role['sectionId']}"):
                                with st.spinner("Removing enrollment..."):
                                    success = remove_user_role(selected_user_id, role["courseId"], role["sectionId"])
                                    if success:
                                        st.success(f"Removed enrollment successfully!")
                                        st.rerun()
                else:
                    st.info("This user is not enrolled in any courses.")
                
               # Add new enrollment section
st.subheader("Add New Course Enrollment")

# Get all available courses
available_courses = get_courses()

# Filter out courses the user is already enrolled in
enrolled_course_ids = [role["courseId"] for role in user_roles]
available_courses = [
    course for course in available_courses
    if course["courseId"] not in enrolled_course_ids
]

if available_courses:
    with st.form("add_enrollment_form"):
        # Course dropdown
        course_options = {
            course["courseName"]: course["courseId"]
            for course in available_courses
        }
        selected_course = st.selectbox(
            "Select Course", options=list(course_options.keys())
        )
        selected_course_id = course_options[selected_course]

        # Role dropdown
        role_options = ["student", "TA", "teacher"]
        new_course_role = st.selectbox(
            "Role in Course", options=role_options
        )

        # Section input
        section_id = st.number_input(
            "Section ID", min_value=1, value=1
        )

        # Submit button
        add_button = st.form_submit_button("Add Enrollment")

        if add_button:
            with st.spinner("Adding enrollment…"):
                ok = add_user_role(
                    selected_user_id,
                    new_course_role,
                    selected_course_id,
                    section_id
                )
                if ok:
                    st.success("Added enrollment successfully!")
                    st.rerun()
                else:
                    st.error(
                        "Failed to add enrollment. "
                        "Check the logs or your network tab for details."
                    )
else:
    st.info("This user is already enrolled in all available courses.")

st.markdown("---")
st.subheader("All Users")
if users_list:
    df = pd.DataFrame(users_list)
    df = df.rename(columns={"firstName": "First Name", "lastName": "Last Name", "email": "Email", "displayName": "Display Name"})
    st.dataframe(df[["userId", "Display Name", "Email"]], use_container_width=True)
else:
    st.info("No users found.")

# Add a section to show all course enrollments
with st.expander("View All Course Enrollments"):
    # We'll need to fetch all users and their roles
    all_enrollments = []
    
    with st.spinner("Loading all enrollments..."):
        for user in users_list:
            user_roles = get_user_roles(user["userId"])
            for role in user_roles:
                course_name = get_course_name(role["courseId"], role["sectionId"])
                all_enrollments.append({
                    "User ID": user["userId"],
                    "User Name": f"{user['firstName']} {user['lastName']}",
                    "Course ID": role["courseId"],
                    "Course Name": course_name,
                    "Role": role["role"],
                    "Section ID": role["sectionId"]
                })
    
    if all_enrollments:
        st.dataframe(pd.DataFrame(all_enrollments), use_container_width=True)
    else:
        st.info("No course enrollments found.")

st.markdown("---")
st.caption("Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))