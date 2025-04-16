##################################################
# Admin Departments & Courses Management Page
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
    page_title="Course Companion - Departments & Courses",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set up navigation
SideBarLinks()

# Helper functions for API calls
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
        st.error("Could not connect to the API. Using sample data instead.")
        # Return sample data as fallback
        return [
            {"departmentId": 1, "departmentName": "Mathematics", "description": "Department focused on mathematical theory and applications"},
            {"departmentId": 2, "departmentName": "Computer Science", "description": "Department focused on computation, programming, and algorithmic thinking"},
            {"departmentId": 3, "departmentName": "Spanish", "description": "Department focused on Spanish language and culture"},
            {"departmentId": 4, "departmentName": "Sports", "description": "Department focused on physical education and sports"}
        ]

def get_department(dept_id):
    try:
        # Try using api container name for Docker or localhost for local development
        try:
            response = requests.get(f'http://api:4000/dept/search/{dept_id}').json()
        except:
            response = requests.get(f'http://localhost:4000/dept/search/{dept_id}').json()
        
        if response and len(response) > 0:
            return response[0]  # API returns an array, get the first item
        return None
    except Exception as e:
        logger.error(f"API connection error: {str(e)}")
        return None

def create_department(dept_data):
    try:
        # Try using api container name for Docker or localhost for local development
        try:
            response = requests.post(
                'http://api:4000/dept/create', 
                json=dept_data,
                headers={"Content-Type": "application/json"}
            ).json()
        except:
            response = requests.post(
                'http://localhost:4000/dept/create', 
                json=dept_data,
                headers={"Content-Type": "application/json"}
            ).json()
        
        return True, response.get("message", "Department added successfully")
    except Exception as e:
        logger.error(f"API connection error: {str(e)}")
        return False, f"API connection error: {str(e)}"

def update_department(dept_id, dept_data):
    try:
        # Try using api container name for Docker or localhost for local development
        try:
            response = requests.put(
                f'http://api:4000/dept/update/{dept_id}', 
                json=dept_data,
                headers={"Content-Type": "application/json"}
            ).json()
        except:
            response = requests.put(
                f'http://localhost:4000/dept/update/{dept_id}', 
                json=dept_data,
                headers={"Content-Type": "application/json"}
            ).json()
        
        return True, response.get("message", "Department updated successfully")
    except Exception as e:
        logger.error(f"API connection error: {str(e)}")
        return False, f"API connection error: {str(e)}"

def delete_department(dept_id):
    try:
        # Try using api container name for Docker or localhost for local development
        try:
            response = requests.delete(f'http://api:4000/dept/delete/{dept_id}').json()
        except:
            response = requests.delete(f'http://localhost:4000/dept/delete/{dept_id}').json()
        
        return True, response.get("message", "Department deleted successfully")
    except Exception as e:
        logger.error(f"API connection error: {str(e)}")
        return False, f"API connection error: {str(e)}"

# Helper functions for courses (placeholder - implement when you have the API endpoints)
def get_all_courses():
    # Placeholder for course API - replace with actual API call
    return [
        {"courseId": 1, "courseName": "Introduction to Programming", "courseDescription": "Fundamentals of programming using Python", "departmentId": 1, "sectionId": 1},
        {"courseId": 2, "courseName": "Data Structures", "courseDescription": "Advanced data structures and algorithms", "departmentId": 1, "sectionId": 2},
        {"courseId": 3, "courseName": "Calculus I", "courseDescription": "Introduction to differential and integral calculus", "departmentId": 2, "sectionId": 1},
        {"courseId": 4, "courseName": "Physics I", "courseDescription": "Mechanics and thermodynamics", "departmentId": 3, "sectionId": 1},
        {"courseId": 5, "courseName": "Engineering Fundamentals", "courseDescription": "Basic principles of engineering design", "departmentId": 4, "sectionId": 1}
    ]

def get_department_name(dept_id, departments_data):
    for dept in departments_data:
        if dept["departmentId"] == dept_id:
            return dept["departmentName"]
    return "Unknown Department"

# Page header
st.title("Department & Course Management")
st.markdown("### Course Companion Admin System")
st.markdown("---")

# Back button
if st.button("← Back to Admin Home"):
    st.switch_page("pages/20_admin_page.py")

# Main content
tab1, tab2 = st.tabs(["Departments", "Courses"])

# Departments Tab
with tab1:
    st.header("Department Management")
    
    # Fetch departments
    departments_data = get_all_departments()
    
    # Add new department
    with st.expander("Add New Department"):
        with st.form("add_department_form"):
            # Auto-generate the next department ID
            next_dept_id = 1
            if departments_data:
                next_dept_id = max(dept["departmentId"] for dept in departments_data) + 1
            
            dept_id = st.number_input("Department ID", min_value=1, value=next_dept_id)
            dept_name = st.text_input("Department Name", key="new_dept_name")
            dept_desc = st.text_area("Description", key="new_dept_desc")
            
            submit_button = st.form_submit_button("Add Department")
            if submit_button:
                if dept_name:
                    # Create department data
                    dept_data = {
                        "departmentId": int(dept_id),
                        "departmentName": dept_name,
                        "description": dept_desc
                    }
                    
                    # Send to API
                    success, message = create_department(dept_data)
                    
                    if success:
                        st.success(message)
                        logger.info(f"Added new department: {dept_name}")
                        # Refresh the page to show the new department
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Department name is required!")
    
    # Edit departments
    with st.expander("Edit Departments"):
        if departments_data:
            department_options = {dept["departmentName"]: dept["departmentId"] for dept in departments_data}
            selected_dept_name = st.selectbox(
                "Select Department to Edit",
                options=list(department_options.keys())
            )
            
            selected_dept_id = department_options[selected_dept_name]
            
            # Get current department info
            dept_info = next((dept for dept in departments_data if dept["departmentId"] == selected_dept_id), None)
            
            if dept_info:
                with st.form("edit_department_form"):
                    dept_name = st.text_input("Department Name", value=dept_info["departmentName"])
                    dept_desc = st.text_area("Description", value=dept_info["description"])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        update_button = st.form_submit_button("Update Department")
                    with col2:
                        delete_button = st.form_submit_button("Delete Department", type="secondary")
                    
                    if update_button:
                        # Create updated department data
                        updated_data = {
                            "departmentName": dept_name,
                            "description": dept_desc
                        }
                        
                        # Send to API
                        success, message = update_department(selected_dept_id, updated_data)
                        
                        if success:
                            st.success(message)
                            logger.info(f"Updated department: {dept_name}")
                            # Refresh the page to show the updated department
                            st.rerun()
                        else:
                            st.error(message)
                    
                    if delete_button:
                        # Check if courses exist for this department
                        courses_data = get_all_courses()
                        if any(course["departmentId"] == selected_dept_id for course in courses_data):
                            st.error("Cannot delete department with associated courses!")
                            logger.warning(f"Attempted to delete department {dept_name} with associated courses")
                        else:
                            # Send to API
                            success, message = delete_department(selected_dept_id)
                            
                            if success:
                                st.success(message)
                                logger.info(f"Deleted department: {dept_name}")
                                # Refresh the page to show the deleted department
                                st.rerun()
                            else:
                                st.error(message)
        else:
            st.info("No departments found.")
    
    # Display departments table
    st.subheader("Current Departments")
    if departments_data:
        dept_df = pd.DataFrame(departments_data)
        st.dataframe(dept_df, use_container_width=True)
    else:
        st.info("No departments found.")

# Courses Tab (placeholder - implement when you have the API endpoints)
with tab2:
    st.header("Course Management")
    
    # Fetch departments for the dropdown
    departments_data = get_all_departments()
    
    # Department filter dropdown
    department_options = {dept["departmentName"]: dept["departmentId"] for dept in departments_data}
    department_options["All Departments"] = "All"
    
    selected_dept_name = st.selectbox(
        "Filter by Department",
        options=list(department_options.keys())
    )
    
    department_filter = department_options[selected_dept_name]
    
    # Fetch courses
    courses_data = get_all_courses()
    
    # Add new course (placeholder)
    with st.expander("Add New Course"):
        st.write("Course creation functionality will be implemented when the API is available.")
        
        # Sample form for future implementation
        with st.form("add_course_form"):
            course_name = st.text_input("Course Name", key="new_course_name")
            course_desc = st.text_area("Course Description", key="new_course_desc")
            
            dept_options = {dept["departmentName"]: dept["departmentId"] for dept in departments_data}
            selected_dept = st.selectbox(
                "Department",
                options=list(dept_options.keys())
            )
            
            section_id = st.number_input("Section ID", min_value=1, value=1)
            
            submit_button = st.form_submit_button("Add Course")
            if submit_button:
                st.info("Course addition API not yet implemented")
    
    # Edit courses (placeholder)
    with st.expander("Edit Courses"):
        st.write("Course editing functionality will be implemented when the API is available.")
    
    # Display courses table
    st.subheader("Current Courses")
    
    # Filter courses by selected department if not "All"
    if department_filter != "All":
        filtered_courses = [course for course in courses_data if course["departmentId"] == department_filter]
    else:
        filtered_courses = courses_data
    
    if filtered_courses:
        # Create a DataFrame with department names
        courses_df = pd.DataFrame(filtered_courses)
        courses_df["department"] = courses_df["departmentId"].apply(
            lambda x: get_department_name(x, departments_data)
        )
        
        # Display the DataFrame
        st.dataframe(courses_df[["courseId", "courseName", "courseDescription", "department", "sectionId"]], 
                   use_container_width=True)
    else:
        st.info("No courses found for the selected department.")

# Footer
st.markdown("---")