##################################################
# Enrollment Role Updating Page
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Import required libraries
import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd
import requests
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Course Companion - Enrollment Role Updating",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

SideBarLinks()

# Helper functions for API calls
def get_all_users():
    try:
        # Try using api container name for Docker or localhost for local development
        try:
            response = requests.get('http://api:4000/u/all').json()
            return response
        except:
            response = requests.get('http://localhost:4000/u/all').json()
            return response
    except Exception as e:
        logger.error(f"API connection error: {str(e)}")
        st.error("Could not connect to the users API. Using sample data instead.")
        # Return sample data as fallback
        return [
            {
                "bio": "Computer Science major with a passion for AI and machine learning.",
                "birthdate": "Mon, 15 May 2000 00:00:00 GMT",
                "firstName": "Bob",
                "lastName": "Smith",
                "universityEmail": "bsmith@university.edu",
                "userId": 1
            },
            {
                "bio": "Mathematics major interested in cryptography and number theory.",
                "birthdate": "Fri, 22 Oct 1999 00:00:00 GMT",
                "firstName": "Alice",
                "lastName": "Johnson",
                "universityEmail": "ajohnson@university.edu",
                "userId": 2
            },
            {
                "bio": "Physical Education professor specializing in basketball techniques and team strategy.",
                "birthdate": "Sun, 30 Dec 1984 00:00:00 GMT",
                "firstName": "Lebron",
                "lastName": "James",
                "universityEmail": "ljames@university.edu",
                "userId": 3
            }
        ]

def get_all_system_roles():
    try:
        # Try using api container name for Docker or localhost for local development
        try:
            response = requests.get('http://api:4000/system_roles/all').json()
            return response
        except:
            response = requests.get('http://localhost:4000/system_roles/all').json()
            return response
    except Exception as e:
        logger.error(f"API connection error: {str(e)}")
        logger.info("Using session state or sample data for system roles.")
        # Use session state if available, otherwise use sample data
        if 'user_roles' in st.session_state:
            return st.session_state.user_roles
        return [
            {"userId": 1, "role": "student"},
            {"userId": 2, "role": "student"},
            {"userId": 3, "role": "teacher", "prefix": "Prof."}
        ]

def get_user_system_role(user_id):
    try:
        # Try using api container name for Docker or localhost for local development
        try:
            response = requests.get(f'http://api:4000/system_roles/{user_id}').json()
            if response and len(response) > 0:
                return response[0]
            return None
        except:
            response = requests.get(f'http://localhost:4000/system_roles/{user_id}').json()
            if response and len(response) > 0:
                return response[0]
            return None
    except Exception as e:
        logger.error(f"API connection error: {str(e)}")
        # Try to get from session state if available
        if 'user_roles' in st.session_state:
            for role in st.session_state.user_roles:
                if role["userId"] == user_id:
                    return role
        return None

def update_user_system_role(user_id, role_data):
    try:
        # Try using api container name for Docker or localhost for local development
        try:
            response = requests.post(
                f'http://api:4000/system_roles/{user_id}/update', 
                json=role_data,
                headers={"Content-Type": "application/json"}
            ).json()
        except:
            response = requests.post(
                f'http://localhost:4000/system_roles/{user_id}/update', 
                json=role_data,
                headers={"Content-Type": "application/json"}
            ).json()
        
        return True, response.get("message", "User system role updated successfully")
    except Exception as e:
        logger.error(f"API connection error: {str(e)}")
        # Update in session state if API fails
        if 'user_roles' in st.session_state:
            for i, role in enumerate(st.session_state.user_roles):
                if role["userId"] == user_id:
                    st.session_state.user_roles[i] = {**role_data, "userId": user_id}
                    break
            else:
                st.session_state.user_roles.append({**role_data, "userId": user_id})
        return False, f"API connection error: {str(e)}, but updated in local session."

# Helper functions for user display
def get_users_with_roles():
    users = get_all_users()
    system_roles = get_all_system_roles()
    
    # Create a dictionary mapping userId to role for faster lookup
    role_map = {}
    for role in system_roles:
        role_map[role["userId"]] = role
    
    users_with_roles = []
    for user in users:
        user_id = user["userId"]
        role_info = role_map.get(user_id, {})
        role = role_info.get("role", "unknown")
        prefix = role_info.get("prefix", "")
        
        users_with_roles.append({
            "userId": user_id,
            "firstName": user["firstName"],
            "lastName": user["lastName"],
            "email": user["universityEmail"],
            "role": role,
            "prefix": prefix,
            "displayName": f"{prefix + ' ' if prefix else ''}{user['firstName']} {user['lastName']}"
        })
    
    return users_with_roles

def get_course_name(course_id):
    courses = [
        {"courseId": 1, "courseName": "Introduction to Programming"},
        {"courseId": 2, "courseName": "Data Structures"},
        {"courseId": 3, "courseName": "Calculus I"},
        {"courseId": 4, "courseName": "Physics I"},
        {"courseId": 5, "courseName": "Engineering Fundamentals"}
    ]
    for course in courses:
        if course["courseId"] == course_id:
            return course["courseName"]
    return f"Course {course_id}"

# Initialize session state for fallback
if 'user_roles' not in st.session_state:
    st.session_state.user_roles = [
        {"userId": 1, "role": "student"},
        {"userId": 2, "role": "student"},
        {"userId": 3, "role": "teacher", "prefix": "Prof."}
    ]

# Page header
st.title("Enrollment Role Updating")
st.markdown("### Course Companion Admin System")
st.markdown("---")

if st.button("\u2190 Back to Admin Home"):
    st.switch_page("pages/20_admin_page.py")

# Get users with their roles
users_with_roles = get_users_with_roles()

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Select User")
    role_filter = st.selectbox("Filter by Role", options=["All", "student", "TA", "teacher", "admin"])
    filtered_users = [user for user in users_with_roles if user["role"] == role_filter] if role_filter != "All" else users_with_roles
    if filtered_users:
        user_options = {user["displayName"]: user["userId"] for user in filtered_users}
        selected_user_display = st.selectbox("Select User", options=list(user_options.keys()))
        selected_user_id = user_options[selected_user_display]
    else:
        st.info("No users found with the selected role filter.")
        selected_user_id = None

with col2:
    if selected_user_id is not None:
        user_info = next((user for user in users_with_roles if user["userId"] == selected_user_id), None)
        if user_info:
            st.subheader(f"Update Roles for {user_info['displayName']}")
            st.markdown(f"**Email:** {user_info['email']}")
            st.markdown(f"**Current System Role:** {user_info['role']}")

            with st.expander("Update System Role", expanded=True):
                with st.form("update_system_role_form"):
                    new_role = st.selectbox("System Role", options=["student", "TA", "teacher", "admin"], index=["student", "TA", "teacher", "admin"].index(user_info["role"]) if user_info["role"] in ["student", "TA", "teacher", "admin"] else 0)
                    prefix = ""
                    if new_role == "teacher":
                        prefix_options = ["", "Prof.", "Dr.", "Instructor", "Mr.", "Ms.", "Mrs."]
                        current_prefix = user_info["prefix"] if "prefix" in user_info and user_info["prefix"] else ""
                        prefix_index = prefix_options.index(current_prefix) if current_prefix in prefix_options else 0
                        prefix = st.selectbox("Title/Prefix", options=prefix_options, index=prefix_index)
                    
                    update_button = st.form_submit_button("Update System Role")
                    if update_button:
                        # Prepare role data for API
                        role_data = {"role": new_role}
                        if new_role == "teacher" and prefix:
                            role_data["prefix"] = prefix
                        
                        # Call API to update role
                        success, message = update_user_system_role(selected_user_id, role_data)
                        
                        if success:
                            st.success(f"System role updated successfully!")
                        else:
                            st.warning(message)
                        
                        logger.info(f"Updated system role for user {selected_user_id} to {new_role}")
                        st.rerun()

# Display all users and their roles
st.markdown("---")
st.subheader("All Users and Roles")
if users_with_roles:
    df = pd.DataFrame(users_with_roles)
    df = df.rename(columns={"firstName": "First Name", "lastName": "Last Name", "email": "Email", "role": "System Role", "prefix": "Prefix", "displayName": "Display Name"})
    st.dataframe(df[["userId", "Display Name", "Email", "System Role", "Prefix"]], use_container_width=True)
else:
    st.info("No users found.")

st.markdown("---")