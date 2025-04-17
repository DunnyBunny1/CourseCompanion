from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db


# Creates a new blueprint object
users = Blueprint('users', __name__)


# Gets all users in the database
@users.route('/all', methods=['GET'])
def all_user():
    cursor = db.get_db().cursor()

    query = '''
        SELECT userId, firstName, lastName, bio, birthdate, universityEmail
        FROM users
    '''
    
    cursor.execute(query)
    return_data = cursor.fetchall()
    
    the_response = make_response(jsonify(return_data))
    the_response.status_code = 200
    return the_response


# Gets te name of a user given an id
@users.route('/users/<int:user_id>', methods=['GET'])
def specific_user(user_id: int):
    cursor = db.get_db().cursor()

    query = f'''
        SELECT firstName, lastName
        FROM users
        WHERE userId = {user_id}
    '''
    
    cursor.execute(query)
    return_data = cursor.fetchall()
    
    the_response = make_response(jsonify(return_data))
    the_response.status_code = 200
    return the_response

# Gets all users in the database
@users.route('/users/<int:course_id>/<int:section_id>/role/<string:role_id>', methods=['GET'])
def get_all_users_of_role(course_id, section_id, role_id):
    cursor = db.get_db().cursor()

    query = '''
        SELECT u.userId, u.firstName, u.lastName
        FROM users u 
        JOIN user_course uc ON u.userId = uc.userId
        WHERE uc.role = %s AND uc.courseId = %s AND uc.sectionId = %s
    '''
    
    params = (role_id, course_id, section_id)

    cursor.execute(query, params)
    return_data = cursor.fetchall()
    
    the_response = make_response(jsonify(return_data))
    the_response.status_code = 200
    return the_response





# Gets a specific user
@users.route('/<id>', methods=['GET'])
def search_user(id):
    cursor = db.get_db().cursor()

    query = '''
        SELECT userId, firstName, lastName, bio, birthdate, universityEmail
        FROM users
        WHERE userId = %s
    '''
    
    cursor.execute(query, (id,))
    
    return_data = cursor.fetchall()
    
    the_response = make_response(jsonify(return_data))
    the_response.status_code = 200
    return the_response


# Gets a users role
@users.route('/<id>/role', methods=['GET'])
def search_user_role(id):
    cursor = db.get_db().cursor()

    query = '''
        SELECT u.userId, firstName, lastName, uc.role, uc.courseId, uc.sectionId
        FROM users u
        JOIN user_course uc ON u.userId = uc.userId
        WHERE u.userId = %s
    '''
    
    cursor.execute(query, (id,))
    
    return_data = cursor.fetchall()
    
    the_response = make_response(jsonify(return_data))
    the_response.status_code = 200
    return the_response

# Add user with a certain role
@users.route('/<id>/create/role', methods=['POST'])
def create_role(id):
    request_data = request.get_json()
    
    cursor = db.get_db().cursor()

    u_role = request_data.get('user_role')
    u_course = request_data.get('user_course')
    u_section = request_data.get('user_section')
    is_active = request_data.get('isActive', 1)

    query = '''
        INSERT INTO user_course(userId, role, courseId, sectionId, isActive)
        VALUES (%s, %s, %s, %s, %s)
    '''
    
    cursor.execute(query, (id, u_role, u_course, u_section, is_active))
    
    db.get_db().commit()

    the_response = make_response(jsonify({"message": "User added successfully"}))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
 
# Remove user from a course
@users.route('/<id>/delete/role', methods=['DELETE'])
def delete_department(id):
    request_data = request.get_json()
    
    cursor = db.get_db().cursor()

    u_course = request_data.get('user_course')
    u_section = request_data.get('user_section')
    
    query = '''
        DELETE FROM user_course
        WHERE userId = %s AND courseId = %s AND sectionId = %s
    '''
    
    cursor.execute(query, (id, u_course, u_section)) 

    db.get_db().commit()

    the_response = make_response(jsonify({"message": "User in a course deleted successfully"}))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response