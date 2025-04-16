##################################################
# Admin Enrollment Management Page
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
import json
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Course Companion - Enrollment Management",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set up navigation
SideBarLinks()

# Helper functions for API calls
def get_user(user_id):
    try:
        # Try using api container name for Docker or localhost for local development
        try:
            response = requests.get(f'http://api:4000/u/{user_id}').json()
        except:
            response = requests.get(f'http://localhost:4000/u/{user_id}').json()
        
        if response and len(response) > 0:
            return response[0]  # API returns an array, get the first item
        return None
    except Exception as e:
        logger.error(f"API connection error: {str(e)}")
        return None

def get_user_role(user_id):
    try:
        # Try using api container name for Docker or localhost for local development
        try:
            response = requests.get(f'http://api:4000/u/{user_id}/role').json()
            return response
        except:
            response = requests.get(f'http://localhost:4000/u/{user_id}/role').json()
            return response
    except Exception as e:
        logger.error(f"API connection error: {str(e)}")
        return []

def add_user_role(user_id, role_data):
    try:
        # Try using api container name for Docker or localhost for local development
        try:
            response = requests.post(
                f'http://api:4000/u/{user_id}/create/role', 
                json=role_data,
                headers={"Content-Type": "application/json"}
            ).json()
        except:
            response = requests.post(
                f'http://localhost:4000/u/{user_id}/create/role', 
                json=role_data,
                headers={"Content-Type": "application/json"}
            ).json()
        
        return True, response.get("message", "User enrolled successfully")
    except Exception as e:
        logger.error(f"API connection error: {str(e)}")
        return False, f"API connection error: {str(e)}"

def delete_user_role(user_id, role_data):
    try:
        # Try using api container name for Docker or localhost for local development
        try:
            response = requests.delete(
                f'http://api:4000/u/{user_id}/delete/role', 
                json=role_data,
                headers={"Content-Type": "application/json"}
            ).json()
        except:
            response = requests.delete(
                f'http://localhost:4000/u/{user_id}/delete/role', 
                json=role_data,
                headers={"Content-Type": "application/json"}
            ).json()
        
        return True, response.get("message", "User enrollment removed successfully")
    except Exception as e:
        logger.error(f"API connection error: {str(e)}")
        return False, f"API connection error: {str(e)}"

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
        # Return sample data matching the format of the actual API response
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

def get_all_courses():
    # Return sample data directly since the courses API isn't available yet
    return [
        {"courseId": 1, "courseName": "Introduction to Programming", "courseDescription": "Fundamentals of programming using Python", "departmentId": 1, "sectionId": 1},
        {"courseId": 2, "courseName": "Data Structures", "courseDescription": "Advanced data structures and algorithms", "departmentId": 1, "sectionId": 2},
        {"courseId": 3, "courseName": "Calculus I", "courseDescription": "Introduction to differential and integral calculus", "departmentId": 2, "sectionId": 1},
        {"courseId": 4, "courseName": "Physics I", "courseDescription": "Mechanics and thermodynamics", "departmentId": 3, "sectionId": 1},
        {"courseId": 5, "courseName": "Engineering Fundamentals", "courseDescription": "Basic principles of engineering design", "departmentId": 4, "sectionId": 1}
    ]

def get_all_departments():
    try:
        # Try using api container name for Docker or localhost for local development
        try:
            response = requests.get('http://api:4000/dept/all').json()
            return response
        except:
            response = requests.get('http://localhost:4000/dept/all').json()
            return response
    except Exception as e:
        logger.error(f"API connection error: {str(e)}")
        st.error("Could not connect to the departments API. Using sample data instead.")
        # Return sample data as fallback
        return [
            {"departmentId": 1, "departmentName": "Mathematics", "description": "Department focused on mathematical theory and applications"},
            {"departmentId": 2, "departmentName": "Computer Science", "description": "Department focused on computation, programming, and algorithmic thinking"},
            {"departmentId": 3, "departmentName": "Spanish", "description": "Department focused on Spanish language and culture"},
            {"departmentId": 4, "departmentName": "Sports", "description": "Department focused on physical education and sports"}
        ]

def get_department_name(dept_id, departments_data):
    for dept in departments_data:
        if dept["departmentId"] == dept_id:
            return dept["departmentName"]
    return "Unknown Department"

# Get enrollments by joining user and course data
def get_all_enrollments():
    # This would be replaced with actual API call in the future
    # For now, we'll create enrollments from user roles
    enrollments = []
    users = get_all_users()
    courses = get_all_courses()
    departments = get_all_departments()
    
    # Get user roles for each user
    for user in users:
        user_roles = get_user_role(user["userId"])
        
        # If no roles found, continue to next user
        if not user_roles:
            continue
        
        # Create enrollment records from roles
        for role in user_roles:
            course_id = role.get("courseId")
            course = next((c for c in courses if c["courseId"] == course_id), None)
            
            if course:
                department_id = course.get("departmentId")
                department_name = next((d["departmentName"] for d in departments if d["departmentId"] == department_id), "Unknown Department")
                
                enrollments.append({
                    "userId": user["userId"],
                    "firstName": user["firstName"],
                    "lastName": user["lastName"],
                    "email": user["universityEmail"],
                    "role": role.get("role"),
                    "courseId": course_id,
                    "courseName": course.get("courseName"),
                    "sectionId": role.get("sectionId"),
                    "departmentId": department_id,
                    "departmentName": department_name
                })
    
    # If no enrollments found, return sample data
    if not enrollments:
        return [
            {
                "userId": 1,
                "firstName": "John",
                "lastName": "Doe",
                "email": "john.doe@university.edu",
                "role": "student",
                "courseId": 1,
                "courseName": "Introduction to Programming",
                "sectionId": 1,
                "departmentId": 1,
                "departmentName": "Computer Science"
            },
            {
                "userId": 2,
                "firstName": "Jane",
                "lastName": "Smith",
                "email": "jane.smith@university.edu",
                "role": "student",
                "courseId": 2,
                "courseName": "Data Structures",
                "sectionId": 1,
                "departmentId": 1,
                "departmentName": "Computer Science"
            },
            {
                "userId": 3,
                "firstName": "Robert",
                "lastName": "Johnson",
                "email": "robert.johnson@university.edu",
                "role": "teacher",
                "courseId": 1,
                "courseName": "Introduction to Programming",
                "sectionId": 1,
                "departmentId": 1,
                "departmentName": "Computer Science"
            }
        ]
    
    return enrollments

# Page header
st.title("Enrollment Management")
st.markdown("### Course Companion Admin System")
st.markdown("---")

# Back button
if st.button("← Back to Admin Home"):
    st.switch_page("pages/20_admin_page.py")

# Main content
tab1, tab2 = st.tabs(["Enrollment Overview", "Manage Enrollments"])

# Enrollment Overview Tab
with tab1:
    st.header("Enrollment Overview")
    
    # Get enrollment data
    enrollments = get_all_enrollments()
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Department filter
        departments = get_all_departments()
        dept_options = {"All Departments": None}
        dept_options.update({dept["departmentName"]: dept["departmentId"] for dept in departments})
        
        selected_dept_name = st.selectbox(
            "Filter by Department",
            options=list(dept_options.keys())
        )
        
        dept_filter = dept_options[selected_dept_name]
    
    with col2:
        # Course filter
        courses = get_all_courses()
        
        # Filter courses by department if selected
        if dept_filter:
            filtered_courses = [c for c in courses if c["departmentId"] == dept_filter]
        else:
            filtered_courses = courses
        
        course_options = {"All Courses": None}
        course_options.update({course["courseName"]: course["courseId"] for course in filtered_courses})
        
        selected_course_name = st.selectbox(
            "Filter by Course",
            options=list(course_options.keys())
        )
        
        course_filter = course_options[selected_course_name]
    
    with col3:
        # Role filter
        role_options = {
            "All Roles": None,
            "Students": "student",
            "Teachers": "teacher",
            "Administrators": "admin"
        }
        
        selected_role_name = st.selectbox(
            "Filter by Role",
            options=list(role_options.keys())
        )
        
        role_filter = role_options[selected_role_name]
    
    # Apply filters
    filtered_enrollments = enrollments
    
    if dept_filter:
        filtered_enrollments = [e for e in filtered_enrollments if e["departmentId"] == dept_filter]
    
    if course_filter:
        filtered_enrollments = [e for e in filtered_enrollments if e["courseId"] == course_filter]
    
    if role_filter:
        filtered_enrollments = [e for e in filtered_enrollments if e["role"] == role_filter]
    
    # Display filtered enrollments
    if filtered_enrollments:
        # Convert to DataFrame for display
        enrollments_df = pd.DataFrame(filtered_enrollments)
        
        # Create a formatted display name
        enrollments_df["User"] = enrollments_df["firstName"] + " " + enrollments_df["lastName"]
        
        # Select and rename columns for display
        display_df = enrollments_df[["User", "email", "role", "courseName", "sectionId", "departmentName"]]
        display_df.columns = ["User", "Email", "Role", "Course", "Section", "Department"]
        
        st.dataframe(display_df, use_container_width=True)
        
        # Display statistics
        st.subheader("Enrollment Statistics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Count by department
            if "departmentName" in enrollments_df.columns:
                dept_counts = enrollments_df["departmentName"].value_counts().reset_index()
                dept_counts.columns = ["Department", "Count"]
                st.write("Enrollments by Department")
                st.dataframe(dept_counts, use_container_width=True)
        
        with col2:
            # Count by course
            if "courseName" in enrollments_df.columns:
                course_counts = enrollments_df["courseName"].value_counts().reset_index()
                course_counts.columns = ["Course", "Count"]
                st.write("Enrollments by Course")
                st.dataframe(course_counts, use_container_width=True)
        
        # Role distribution
        if "role" in enrollments_df.columns:
            st.subheader("Role Distribution")
            role_counts = enrollments_df["role"].value_counts().reset_index()
            role_counts.columns = ["Role", "Count"]
            
            # Create a bar chart
            st.bar_chart(role_counts.set_index("Role"))
    else:
        st.info("No enrollments found with the selected filters.")

# Manage Enrollments Tab
with tab2:
    st.header("Manage Enrollments")
    
    # Create two sections: Add enrollment and Remove enrollment
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Add New Enrollment")
        
        # Step 1: Select course
        departments = get_all_departments()
        dept_options = {dept["departmentName"]: dept["departmentId"] for dept in departments}
        
        selected_dept_name = st.selectbox(
            "Department",
            options=list(dept_options.keys()),
            key="add_dept"
        )
        
        dept_filter = dept_options[selected_dept_name]
        
        # Filter courses by department
        courses = get_all_courses()
        filtered_courses = [c for c in courses if c["departmentId"] == dept_filter]
        
        course_options = {course["courseName"]: course["courseId"] for course in filtered_courses}
        
        if course_options:
            selected_course_name = st.selectbox(
                "Course",
                options=list(course_options.keys()),
                key="add_course"
            )
            
            selected_course_id = course_options[selected_course_name]
            
            # Section selection
            section_id = st.number_input("Section ID", min_value=1, value=1, key="add_section")
            
            # Step 2: Select user
            users = get_all_users()
            
            # Filter out users who are already in this course/section
            enrollments = get_all_enrollments()
            enrolled_user_ids = [
                e["userId"] for e in enrollments 
                if e["courseId"] == selected_course_id and e["sectionId"] == section_id
            ]
            
            available_users = [u for u in users if u["userId"] not in enrolled_user_ids]
            
            if available_users:
                user_options = {
                    f"{user['firstName']} {user['lastName']} ({user['universityEmail']})": user['userId'] 
                    for user in available_users
                }
                
                selected_user_display = st.selectbox(
                    "Select User",
                    options=list(user_options.keys()),
                    key="add_user"
                )
                
                selected_user_id = user_options[selected_user_display]
                
                # Step 3: Select role
                role_type = st.selectbox(
                    "Role",
                    options=["student", "teacher", "admin"],
                    key="add_role"
                )
                
                # Submit button
                if st.button("Add Enrollment", use_container_width=True):
                    # Prepare role data
                    role_data = {
                        "user_role": role_type,
                        "user_course": selected_course_id,
                        "user_section": section_id
                    }
                    
                    # Call API
                    success, message = add_user_role(selected_user_id, role_data)
                    
                    if success:
                        st.success(message)
                        logger.info(f"Added enrollment for user {selected_user_id} in course {selected_course_id}")
                        # Refresh the page
                        st.rerun()
                    else:
                        st.error(message)
                        st.info("For demonstration, showing what would be added:")
                        st.json(role_data)
            else:
                st.info("All users are already enrolled in this course section.")
        else:
            st.info("No courses available for the selected department.")
    
    with col2:
        st.subheader("Remove Enrollment")
        enrollments = get_all_enrollments()
        if enrollments:
            enrollment_options = {
                f"{e['firstName']} {e['lastName']} - {e['courseName']} (Section {e['sectionId']}) [{e['role']}]": (e["userId"], e["courseId"], e["sectionId"], e["role"])
                for e in enrollments
            }
            selected_enrollment = st.selectbox(
                "Select Enrollment to Remove",
                options=list(enrollment_options.keys()),
                key="remove_enrollment"
            )
            if selected_enrollment:
                user_id, course_id, section_id, role_type = enrollment_options[selected_enrollment]
                if st.button("Remove Enrollment", use_container_width=True):
                    role_data = {
                        "user_role": role_type,
                        "user_course": course_id,
                        "user_section": section_id
                    }
                    success, message = delete_user_role(user_id, role_data)
                    if success:
                        st.success(message)
                        logger.info(f"Removed enrollment: user {user_id} from course {course_id}, section {section_id}")
                        st.rerun()
                    else:
                        st.error(message)
        else:
            st.info("No enrollments available to remove.")

# Footer
st.markdown("---")