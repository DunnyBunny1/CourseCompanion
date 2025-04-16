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
            response = requests.get('http://api:4000/dept/all').json()
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
        response = requests.get(f'http://api:4000/dept/search/{dept_id}').json()

        if response and len(response) > 0:
            return response[0]  # API returns an array, get the first item
        return None
    except Exception as e:
        logger.error(f"API connection error: {str(e)}")
        return None

def create_department(dept_data):
    try:
        # Try using api container name for Docker or localhost for local development
        response = requests.post(
                'http://api:4000/dept/create', 
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
        response = requests.put(
                f'http://api:4000/dept/update/{dept_id}', 
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
        response = requests.delete(f'http://api:4000/dept/delete/{dept_id}').json()
        
        return True, response.get("message", "Department deleted successfully")
    except Exception as e:
        logger.error(f"API connection error: {str(e)}")
        return False, f"API connection error: {str(e)}"

def get_department_name(dept_id, departments_data):
    for dept in departments_data:
        if dept["departmentId"] == dept_id:
            return dept["departmentName"]
    return "Unknown Department"

# Updated helper functions for courses API calls
def get_all_courses():
    try:
        # Try using api container name for Docker or localhost for local development
        response = requests.get('http://api:4000/crs/all').json()
        return response
        
    except Exception as e:
        logger.error(f"API connection error: {str(e)}")
        st.error("Could not connect to the API. Using sample data instead.")
        # Return sample data as fallback
        return [
            {"courseId": 1001, "courseName": "Intro to Spanish", "courseDescription": "Introduction to Spanish language for beginners", "departmentId": 3, "sectionId": 1},
            {"courseId": 1001, "courseName": "Intro to Spanish", "courseDescription": "Introduction to Spanish language for beginners", "departmentId": 3, "sectionId": 2},
            {"courseId": 2001, "courseName": "Fundies of CS 1", "courseDescription": "Fundamentals of Computer Science 1 - Introduction to programming concepts", "departmentId": 2, "sectionId": 1},
            {"courseId": 3001, "courseName": "Linear Algebra", "courseDescription": "Study of linear equations, matrices, vector spaces, and linear transformations", "departmentId": 1, "sectionId": 1},
            {"courseId": 4001, "courseName": "AP Basketball", "courseDescription": "How to dunk like LeGoat and splash 3 pointers like Steph", "departmentId": 4, "sectionId": 1}
        ]

def get_course(course_id):
    try:
        # Try using api container name for Docker or localhost for local development
        response = requests.get(f'http://api:4000/crs/courses/{course_id}').json()
        
        if response and len(response) > 0:
            return response[0]  # API returns an array, get the first item
        return None
    except Exception as e:
        logger.error(f"API connection error: {str(e)}")
        return None

def get_courses_by_department(dept_id):
    try:
        # Try using api container name for Docker or localhost for local development
        response = requests.get(f'http://api:4000/crs/department/{dept_id}').json()
        return response
        
    except Exception as e:
        logger.error(f"API connection error: {str(e)}")
        return []

def create_course(course_data):
    try:
        # Try using api container name for Docker or localhost for local development
        response = requests.post(
                'http://api:4000/crs/courses/create', 
                json=course_data,
                headers={"Content-Type": "application/json"}
            ).json()
       
        return True, response.get("message", "Course added successfully"), response.get("courseId")
    except Exception as e:
        logger.error(f"API connection error: {str(e)}")
        return False, f"API connection error: {str(e)}", None

def update_course(course_data):
    try:
        # Try using api container name for Docker or localhost for local development
        response = requests.put(
                f'http://api:4000/crs/courses', 
                json=course_data,
                headers={"Content-Type": "application/json"}
            ).json()
       
        return True, response.get("message", "Course updated successfully")
    except Exception as e:
        logger.error(f"API connection error: {str(e)}")
        return False, f"API connection error: {str(e)}"

def delete_course(course_id):
    try:
        # Try using api container name for Docker or localhost for local development
        response = requests.delete(f'http://api:4000/crs/courses{course_id}').json()
        
        return True, response.get("message", "Course deleted successfully")
    except Exception as e:
        logger.error(f"API connection error: {str(e)}")
        return False, f"API connection error: {str(e)}"

def search_courses(name_query="", dept_id=None, section_id=None):
    try:
        # Build query parameters
        params = {}
        if name_query:
            params["name"] = name_query
        if dept_id and dept_id != "All":
            params["departmentId"] = dept_id
        if section_id:
            params["sectionId"] = section_id
            
        # Try using api container name for Docker or localhost for local development
        try:
            response = requests.get('http://api:4000/crs/search', params=params).json()
            return response
        except:
            response = requests.get('http://localhost:4000/crs/search', params=params).json()
            return response
    except Exception as e:
        logger.error(f"API connection error: {str(e)}")
        return []

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

# Courses Tab
with tab2:
    st.header("Course Management")
    
    # Fetch all courses and departments data
    courses_data = get_all_courses()
    departments_data = get_all_departments()
    
    # --- Add New Course ---
    with st.expander("Add New Course"):
      with st.form("add_course_form"):
        # Department selector
        dept_map = {d["departmentName"]: d["departmentId"] for d in departments_data}
        selected_dept_name = st.selectbox("Department", list(dept_map.keys()))
        sel_dept_id = dept_map[selected_dept_name]

        # Compute next course ID as default
        dept_courses = [c for c in courses_data if c["departmentId"] == sel_dept_id]
        suggested_course_id = (
            max(c["courseId"] for c in dept_courses) + 1
            if dept_courses
            else sel_dept_id * 1000 + 1
        )

        # Now let the user override it
        course_id = st.number_input(
            "Course ID",
            min_value=1,
            value=suggested_course_id,
            step=1
        )

        # Other fields
        course_name = st.text_input("Course Name")
        course_desc = st.text_area("Course Description")
        section_id = st.number_input("Section ID", min_value=1, value=1)

        submit = st.form_submit_button("Add Course")
        if submit:
            if not course_name:
                st.error("Course name is required!")
            else:
                payload = {
                    "courseId": course_id,                # use the user‑entered ID
                    "courseName": course_name,
                    "courseDescription": course_desc,
                    "departmentId": sel_dept_id,
                    "sectionId": section_id
                }
                success, message, new_id = create_course(payload)
                if success:
                    created_id = new_id or course_id
                    st.success(f"{message} (ID: {created_id})")
                    logger.info(f"Added new course: {course_name} ({created_id})")
                    st.rerun()
                else:
                    st.error(message)

    
    # Edit courses
    with st.expander("Edit Courses"):
        if courses_data:
            course_options = {f"{course['courseName']} (ID: {course['courseId']}, Section: {course['sectionId']})": course["courseId"] for course in courses_data}
            selected_course_name = st.selectbox(
                "Select Course to Edit",
                options=list(course_options.keys())
            )
            
            selected_course_id = course_options[selected_course_name]
            
            # Find courses with matching ID
            matching_courses = [c for c in courses_data if c["courseId"] == selected_course_id]
            
            if matching_courses:
                # If multiple sections exist, let user select which section to edit
                if len(matching_courses) > 1:
                    section_options = {f"Section {c['sectionId']}": c['sectionId'] for c in matching_courses}
                    selected_section_name = st.selectbox(
                        "Select Section",
                        options=list(section_options.keys())
                    )
                    selected_section_id = section_options[selected_section_name]
                    course_info = next((c for c in matching_courses if c["sectionId"] == selected_section_id), None)
                else:
                    course_info = matching_courses[0]
                
                if course_info:
                    with st.form("edit_course_form"):
                        course_name = st.text_input("Course Name", value=course_info["courseName"])
                        course_desc = st.text_area("Course Description", value=course_info["courseDescription"])
                        
                        # Department dropdown for editing
                        dept_options = {dept["departmentName"]: dept["departmentId"] for dept in departments_data}
                        current_dept_name = next((dept["departmentName"] for dept in departments_data 
                                                if dept["departmentId"] == course_info["departmentId"]), 
                                                list(dept_options.keys())[0])
                        
                        selected_dept = st.selectbox(
                            "Department",
                            options=list(dept_options.keys()),
                            index=list(dept_options.keys()).index(current_dept_name) if current_dept_name in dept_options.keys() else 0
                        )
                        
                        section_id = st.number_input("Section ID", min_value=1, value=course_info["sectionId"])
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            update_button = st.form_submit_button("Update Course")
                        with col2:
                            delete_button = st.form_submit_button("Delete Course", type="secondary")
                        
                        if update_button:
                            # Create updated course data
                            updated_data = {
                                "courseId": course_info["courseId"],
                                "courseName": course_name,
                                "courseDescription": course_desc,
                                "departmentId": dept_options[selected_dept],
                                "sectionId": int(section_id)
                            }
                            
                            # Send to API
                            success, message = update_course(updated_data)
                            
                            if success:
                                st.success(message)
                                logger.info(f"Updated course: {course_name}")
                                # Refresh the page to show the updated course
                                st.rerun()
                            else:
                                st.error(message)
                        
                        if delete_button:
                            # Confirm deletion
                            if st.checkbox("Confirm deletion - this cannot be undone"):
                                # Send to API
                                success, message = delete_course(selected_course_id)
                                
                                if success:
                                    st.success(message)
                                    logger.info(f"Deleted course: {course_name}")
                                    # Refresh the page to show the deleted course
                                    st.rerun()
                                else:
                                    st.error(message)
        else:
            st.info("No courses found.")
    
    # Filter and search functionality
    with st.expander("Search and Filter Courses"):
        col1, col2, col3 = st.columns(3)
        with col1:
            # Department filter dropdown
            department_options = {dept["departmentName"]: dept["departmentId"] for dept in departments_data}
            department_options["All Departments"] = "All"
            
            selected_dept_name = st.selectbox(
                "Filter by Department",
                options=list(department_options.keys())
            )
            department_filter = department_options[selected_dept_name]
        
        with col2:
            search_name = st.text_input("Search by Course Name")
        
        with col3:
            search_section = st.number_input("Filter by Section ID", min_value=0, value=0)
            if search_section == 0:
                search_section = None
                
        if st.button("Search"):
            filtered_courses = search_courses(
                name_query=search_name,
                dept_id=department_filter if department_filter != "All" else None,
                section_id=search_section
            )
            st.session_state.filtered_courses = filtered_courses
        
        # Button to clear search and show all courses
        if hasattr(st.session_state, 'filtered_courses'):
            if st.button("Clear Search"):
                del st.session_state.filtered_courses
                st.rerun()
    
    # Display courses table
    st.subheader("Current Courses")
    
    # Get courses for display (either from session state or fetch new)
    display_courses = st.session_state.filtered_courses if hasattr(st.session_state, 'filtered_courses') else courses_data
    
    if display_courses:
        # Create a DataFrame with department names
        courses_df = pd.DataFrame(display_courses)
        courses_df["department"] = courses_df["departmentId"].apply(
            lambda x: get_department_name(x, departments_data)
        )
        
        # Display the DataFrame
        st.dataframe(courses_df[["courseId", "courseName", "courseDescription", "department", "sectionId"]], 
                   use_container_width=True)
    else:
        st.info("No courses found for the selected criteria.")
# Footer
st.markdown("---")