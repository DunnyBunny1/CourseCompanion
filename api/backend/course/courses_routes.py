########################################################
# Courses blueprint of endpoints
########################################################

from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
import json
from backend.db_connection import db

courses = Blueprint('courses', __name__)

#------------------------------------------------------------
# Get all courses
@courses.route('/all', methods=['GET'])
def get_all_courses():
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT courseId, courseName, courseDescription, sectionId, departmentId
        FROM course_companion.courses
    '''
    
    cursor.execute(the_query)
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
#------------------------------------------------------------
# Retrieve a specific course
@courses.route('/courses/<int:course_id>', methods=['GET'])
def retrieve_course_by_id(course_id):
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT courseId, courseName, courseDescription, sectionId, departmentId
        FROM course_companion.courses
        WHERE courseId = %s
    '''
    
    cursor.execute(the_query, (course_id,))
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

#------------------------------------------------------------
# Update an existing course
@courses.route('/courses', methods=['PUT'])
def update_course():
    current_app.logger.info('PUT /courses route')
    course_info = request.json
    course_id = course_info['courseId']
    course_name = course_info['courseName']
    course_desc = course_info['courseDescription']
    section_id = course_info['sectionId']
    dept_id = course_info['departmentId']

    the_query = '''
        UPDATE course_companion.courses
        SET courseName = %s, 
            courseDescription = %s,
            sectionId = %s,
            departmentId = %s
        WHERE courseId = %s;
    '''
    data = (course_name, course_desc, section_id, dept_id, course_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(the_query, data)
    db.get_db().commit()

    the_response = make_response(jsonify({"message": "Course updated successfully"}))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

#------------------------------------------------------------
# Delete a specific course
@courses.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course_by_id(course_id):
    current_app.logger.info(f'DELETE /courses/{course_id} route')
    cursor = db.get_db().cursor()
    the_query = '''
        DELETE FROM course_companion.courses
        WHERE courseId = %s
    '''
    
    r = cursor.execute(the_query, (course_id,))
    db.get_db().commit()
    
    the_response = make_response(jsonify({"message": "Course deleted successfully"}))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

#------------------------------------------------------------
# Create a new course
@courses.route('/courses/create', methods=['POST'])
def create_course():
    current_app.logger.info('POST /courses/create route')
    course_info = request.json
    course_id = course_info['courseId']
    course_name = course_info['courseName']
    course_desc = course_info['courseDescription']
    section_id = course_info['sectionId']
    dept_id = course_info['departmentId']
    
    the_query = '''
        INSERT INTO course_companion.courses
        (courseId,courseName, courseDescription, sectionId, departmentId)
        VALUES (%s,%s, %s, %s, %s)
    '''
    
    data = (course_id,course_name, course_desc, section_id, dept_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(the_query, data)
    db.get_db().commit()
    
    # Get the ID of the newly created course
    new_id = cursor.lastrowid
    
    the_response = make_response(jsonify({
        "message": "Course created successfully",
        "courseId": new_id
    }))
    the_response.status_code = 201
    the_response.mimetype = 'application/json'
    return the_response

#------------------------------------------------------------
# Search for courses based on specific criteria
@courses.route('/courses/search', methods=['GET'])
def search_courses():
    current_app.logger.info('GET /courses/search route')
    
    # Get search parameters from query string
    name_query = request.args.get('name', '')
    dept_id = request.args.get('departmentId', None)
    section_id = request.args.get('sectionId', None)
    
    # Start building the query
    the_query = '''
        SELECT courseId, courseName, courseDescription, sectionId, departmentId
        FROM course_companion.courses
        WHERE 1=1
    '''
    
    # Initialize parameters list
    params = []
    
    # Add filters based on provided parameters
    if name_query:
        the_query += ' AND courseName LIKE %s'
        params.append(f'%{name_query}%')
    
    if dept_id:
        the_query += ' AND departmentId = %s'
        params.append(dept_id)
    
    if section_id:
        the_query += ' AND sectionId = %s'
        params.append(section_id)
    
    # Add sorting
    the_query += ' ORDER BY courseName ASC'
    
    # Execute query
    cursor = db.get_db().cursor()
    cursor.execute(the_query, tuple(params))
    theData = cursor.fetchall()
    
    # Create response
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response