from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

# Creates a new blueprint object
users = Blueprint('users', __name__)

# Gets a specific user
@users.route('/<id>', methods=['GET'])
def search_user(id):
    cursor = db.get_db().cursor()
    cursor.execute('use course_companion')

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
    cursor.execute('use course_companion')

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


# Updates a users role
@users.route('/update/<id>/role', methods=['PUT'])
def update_user_role(id):

    request_data = request.get_json()

    cursor = db.get_db().cursor()
    cursor.execute('use course_companion')

    new_role = request_data.get('new_role')
    course_id = request_data.get('course_id')
    section_id = request_data.get('section_id')

    query = '''
        UPDATE user_course uc
        JOIN users u ON uc.userId = u.userId
        SET uc.role = %s
        WHERE u.userId = %s AND uc.courseId = %s AND uc.sectionId = %s
    '''
    
    cursor.execute(query, (new_role, id, course_id, section_id))

    db.get_db().commit()
    
    return "Role Updated"