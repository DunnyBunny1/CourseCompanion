from typing import List, Dict, Any, Tuple, Optional 
from flask import Blueprint, request, jsonify, make_response, current_app, Response
from backend.db_connection import db
from pymysql.cursors import DictCursor

analytics = Blueprint("analytics", __name__)

@analytics.route("/engagement", methods=["GET"])
def get_engagement_analytics():
    """
    Retrieves all available post tags
    """
    current_app.logger.info('GET /tags route')
    
    # Get a cursor for our shared DB connection
    cursor: DictCursor = db.get_db().cursor()

   
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