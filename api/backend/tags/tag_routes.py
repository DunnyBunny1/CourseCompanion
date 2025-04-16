from typing import List, Dict, Any, Tuple, Optional 
import json
from flask import Blueprint, request, jsonify, make_response, current_app, Response
from backend.db_connection import db
from pymysql.cursors import DictCursor

tags = Blueprint("employees", __name__)


@tags.route("/tags", methods=["GET"])
def get_all_tags():
    """
    Retrieves all available post tags
    """
    current_app.logger.info('GET /tags route')
    
    # Get a cursor for our shared DB connection
    cursor: DictCursor = db.get_db().cursor()

    # Create a SQL query to retrieve all tag_names from
    # our table - these will be unique and not null thanks
    # to our DB constraints
    query: str = """
    SELECT * FROM tags  
    """

    # Execute our query
    cursor.execute(query)

    # Retrieve our data as a python dict
    data = cursor.fetchall()

    # Create HTTP response w/ our jsonified data
    response : Response = make_response(data)
    # Use a 200 OK response code w/ a JSON content type 
    response.status_code = 200 
    response.mimetype = 'application/json'
    
    return response 


@tags.route("/tags/<id>", methods=['GET'])
def get_tag_by_id(id : int): 
    """
    Retrieves the post tag with the given ID if one exists 
    """
    current_app.logger.info('GET /tags/<id> route')
    
    # Get a cursor for our shared DB connection
    cursor: DictCursor = db.get_db().cursor()

    # Create a SQL query to retrieve all tag_names from
    # our table - these will be unique and not null thanks
    # to our DB constraints
    query: str = f"""
    SELECT * FROM tags WHERE tagId = {id}  
    """

    # Execute our query
    cursor.execute(query)

    # Retrieve our data as a python dict
    data = cursor.fetchall()

    # Create HTTP response w/ our jsonified data
    response : Response = make_response(data)
    # Use a 200 OK response code w/ a JSON content type 
    response.status_code = 200 
    response.mimetype = 'application/json'
    
    return response 

@tags.route('/tags/create', methods=['POST'])
def create_new_tag():
    current_app.logger.info('POST /tags/create route')
    
    # Extract the post request body as a python dict
    tag_info : Dict[str, Any] = request.json

    # Extract the name from the tag info
    tag_name : str = tag_info["tag_name"]
    
    # Create a SQL query that creates a new tag 
    query = f"""
    INSERT INTO tags (tagName)
    VALUES ({tag_name})
    """
    
    # Get a cursor for our shared DB connection
    cursor: DictCursor = db.get_db().cursor()
    # Execute our operation and immediately commit to our DB 
    cursor.execute(query)
    db.get_db.commit()
    
    # Return response JSON + 201 status code to indicate successful creation     
    response = make_response(jsonify({"message": "Tag created successfully"}))
    response.status_code = 201 
    response.mimetype = 'application/json'
    return response


@tags.route("/tags/<id>", methods=['DELETE'])
def delete_tag_by_id(id : int): 
    current_app.logger.info('DELETE /tags/<id> route')
    
    # Create a SQL query that deletes the tag w/ the given ID
    query = f"""
    DELETE FROM tags WHERE tagId = {id}
    """
    
    # Get a cursor for our shared DB connection
    cursor: DictCursor = db.get_db().cursor()
    # Execute our operation and immediately commit to our DB 
    cursor.execute(query)
    db.get_db.commit()
    
    # Return response JSON + 200 status code to indicate successful deletion     
    response = make_response(jsonify({"message": "Tag deleted successfully"}))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

@tags.route("/tags/<id>", methods=['PUT'])
def update_tag_by_id(id : int): 
    current_app.logger.info('PUT /tags/<id> route')
    
    # Extract the post request body as a python dict
    tag_info : Dict[str, Any] = request.json

    # Extract the name from the tag info
    tag_name : str = tag_info["tag_name"]
    
    # Create a SQL query that deletes the tag w/ the given ID
    query = f"""
    UPDATE tags
    SET tagName = {tag_name}
    WHERE tagId = {id}
    """
    
    # Get a cursor for our shared DB connection
    cursor: DictCursor = db.get_db().cursor()
    # Execute our operation and immediately commit to our DB 
    cursor.execute(query)
    db.get_db.commit()
    
    # Return response JSON + 200 status code to indicate successful update     
    response = make_response(jsonify({"message": "Tag updated successfully"}))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

@tags.route("/tags/search", methods=["POST"])
def search_tags():
    current_app.logger.info('POST /tags/search route')
    
    # Extract the post request body as a python dict
    tag_info : Dict[str, Any] = request.json

    # Extract the name & id from the tag info 
    tag_name : str = tag_info["tag_name"]
    tag_id : str = tag_info["tag_id"]
    
    
    # Create a base SQL query to retrieve all tag_names from
    # our table. Based on the post request body, we will update
    # the WHERE cluase to match the search constraints 
    query: str = """
    SELECT * FROM tags WHERE 1=1  
    """
    
    if tag_name: 
        query += f" AND tagName = {tag_name} "
    if tag_id: 
        query += f" AND tagId = {tag_id} "

    
    # Get a cursor for our shared DB connection
    cursor: DictCursor = db.get_db().cursor()
    
    # Execute our query
    cursor.execute(query)

    # Retrieve our data as a python dict
    data = cursor.fetchall()

    # Create HTTP response w/ our jsonified data
    response : Response = make_response(data)
    # Use a 200 OK response code w/ a JSON content type 
    response.status_code = 200 
    response.mimetype = 'application/json'
    
    return response 