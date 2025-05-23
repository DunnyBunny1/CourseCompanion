from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db


# Creates a new blueprint object
departments = Blueprint('departments', __name__)


# Gets all departments from the system
@departments.route('/all', methods=['GET'])
def get_departments():

    cursor = db.get_db().cursor()

    query = '''
        SELECT departmentId, departmentName, description
        FROM department;
    '''
    cursor.execute(query)
    
    return_data = cursor.fetchall()
    
    the_response = make_response(jsonify(return_data))
    the_response.status_code = 200
    return the_response


# Creates a new department
@departments.route('/create', methods=['POST'])
def create_departments():
    request_data = request.get_json()
    
    cursor = db.get_db().cursor()

    department_id = request_data.get('departmentId')
    description = request_data.get('description')
    department_name = request_data.get('departmentName')

    query = '''
        INSERT INTO department(departmentId, description, departmentName)
        VALUES (%s, %s, %s)
    '''
    
    cursor.execute(query, (department_id, description, department_name))
    
    db.get_db().commit()
    
    the_response = make_response(jsonify({"message": "Department added successfully"}))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# Gets a specific department
@departments.route('/search/<id>', methods=['GET'])
def search_department(id): 
    cursor = db.get_db().cursor()

    query = '''
        SELECT departmentId, departmentName, description
        FROM department
        WHERE departmentId = %s
    '''
    
    cursor.execute(query, (id,))
    
    return_data = cursor.fetchall()
    
    the_response = make_response(jsonify(return_data))
    the_response.status_code = 200
    return the_response


# Updates a specific department
@departments.route('/update/<id>', methods=['PUT'])
def update_department(id):
    request_data = request.get_json()
    
    cursor = db.get_db().cursor()
    
    department_name = request_data.get('departmentName')
    description = request_data.get('description')
    
    query = '''
        UPDATE department
        SET departmentName = %s,
            description = %s
        WHERE departmentId = %s
    '''
    
    cursor.execute(query, (department_name, description, id))

    db.get_db().commit()
    
    the_response = make_response(jsonify({"message": "Department updated successfully"}))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# Deletes a specific department
@departments.route('/delete/<id>', methods=['DELETE'])
def delete_department(id):
    
    cursor = db.get_db().cursor()
    
    query = '''
        DELETE FROM department
        WHERE departmentId = %s
    '''
    
    cursor.execute(query, (id,)) 

    db.get_db().commit()
    
    the_response = make_response(jsonify({"message": "Department deleted successfully"}))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response