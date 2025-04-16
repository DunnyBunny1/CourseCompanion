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

 # Gets all users in the data base
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
    
    # Check if the API is receiving the isActive field in the request
    print(f"Received data: {request_data}")
    
    # Try to get table schema to confirm isActive field
    try:
        cursor.execute("SHOW COLUMNS FROM user_course")
        columns = cursor.fetchall()
        column_names = [col[0] for col in columns]
        print(f"Table columns: {column_names}")
        
        # Check if isActive field exists
        if 'isActive' in column_names:
            # Field exists, include it in the query
            is_active = request_data.get('isActive', 1)  # Default to 1 if not provided
            
            query = '''
                INSERT INTO user_course(userId, role, courseId, sectionId, isActive)
                VALUES (%s, %s, %s, %s, %s)
            '''
            
            cursor.execute(query, (id, u_role, u_course, u_section, is_active))
        else:
            # Field doesn't exist, use original query
            query = '''
                INSERT INTO user_course(userId, role, courseId, sectionId)
                VALUES (%s, %s, %s, %s)
            '''
            
            cursor.execute(query, (id, u_role, u_course, u_section))
    except Exception as e:
        # If SHOW COLUMNS fails, try with isActive anyway since the error suggests it exists
        print(f"Error checking schema: {str(e)}")
        
        try:
            is_active = request_data.get('isActive', 1)
            
            query = '''
                INSERT INTO user_course(userId, role, courseId, sectionId, isActive)
                VALUES (%s, %s, %s, %s, %s)
            '''
            
            cursor.execute(query, (id, u_role, u_course, u_section, is_active))
        except Exception as e2:
            print(f"Error inserting with isActive: {str(e2)}")
            
            # Try without isActive as last resort
            try:
                query = '''
                    INSERT INTO user_course(userId, role, courseId, sectionId)
                    VALUES (%s, %s, %s, %s)
                '''
                
                cursor.execute(query, (id, u_role, u_course, u_section))
            except Exception as e3:
                print(f"Error inserting without isActive: {str(e3)}")
                raise e3  # Re-raise the last exception
    
    db.get_db().commit()

    the_response = make_response(jsonify({"message": "User role added successfully"}))
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