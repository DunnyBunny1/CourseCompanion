########################################################
# Comments blueprint of endpoints
########################################################

from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
import json
from backend.db_connection import db

comments = Blueprint('comments', __name__)

#------------------------------------------------------------
# Retrieve a specific comment
@comments.route('/comments/<int:comment_id>', methods=['GET'])
def retrieve_comments_by_id(comment_id):
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT commentId, content, createdAt, updatedAt, authorId, parentCommentId, postId
        FROM course_companion.comments
        WHERE commentId = %s
    '''
    
    cursor.execute(the_query, (comment_id,))
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

#------------------------------------------------------------
# Update an existing comment
@comments.route('/comments', methods=['PUT'])
def update_comment():
    current_app.logger.info('PUT /comments route')
    cmt_info = request.json
    cmt_id = cmt_info['commentId']
    content = cmt_info['content']
    c_at = cmt_info['createdAt']
    u_at = cmt_info['updatedAt']
    a_id = cmt_info['authorId']
    p_cid = cmt_info.get('parentCommentId', None) # Optional parent comment ID

    the_query = '''
        UPDATE course_companion.comments
        SET commentId = %s, 
            content = %s,
            createdAt = %s,
            updatedAt = NOW(),
            authorId = %s,
            parentCommentId = %s,
        where commentId = %s;
    '''
    data = (cmt_id, content, c_at, u_at, a_id, p_cid)
    cursor = db.get_db().cursor()
    r = cursor.execute(the_query, data)
    db.get_db().commit()

    the_response = make_response(jsonify({"message": "Comment updated successfully"}))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

#------------------------------------------------------------
# Delete a specific comment
@comments.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comments_by_id(comment_id):
    current_app.logger.info(f'DELETE /comments/{comment_id} route')
    cursor = db.get_db().cursor()
    the_query = '''
        DELETE FROM course_companion.comments
        WHERE commentId = %s
    '''
    
    r = cursor.execute(the_query, (comment_id,))
    db.get_db().commit()
    
    the_response = make_response(jsonify({"message": "Comment deleted successfully"}))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

#------------------------------------------------------------
# Create a new comment on a post
@comments.route('/comments/create', methods=['POST'])
def create_comment():
    current_app.logger.info('POST /comments/create route')
    cmt_info = request.json
    content = cmt_info['content']
    a_id = cmt_info['authorId']
    post_id = cmt_info['postId']
    p_cid = cmt_info.get('parentCommentId', None)  # Optional parent comment ID
    
    the_query = '''
        INSERT INTO course_companion.comments
        (content, createdAt, updatedAt, authorId, parentCommentId, postId)
        VALUES (%s, NOW(), NOW(), %s, %s, %s)
    '''
    
    data = (content, a_id, p_cid, post_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(the_query, data)
    db.get_db().commit()
    
    # TODO: Consider improving debugging by adding comment IDs 
    the_response = make_response(jsonify({"message": "Comment created successfully with id number"}))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

#------------------------------------------------------------
# Search for comments based on specific criteria
@comments.route('/comments/search', methods=['GET'])
def search_comments():
    current_app.logger.info('GET /comments/search route')
    
    # Get search parameters from query string
    content_query = request.args.get('content', '')
    author_id = request.args.get('authorId', None)
    post_id = request.args.get('postId', None)
    date_from = request.args.get('dateFrom', None)
    date_to = request.args.get('dateTo', None)
    
    # Start building the query
    the_query = '''
        SELECT commentId, content, createdAt, updatedAt, authorId, parentCommentId, postId
        FROM course_companion.comments
        WHERE 1=1
    '''
    
    # Initialize parameters list
    params = []
    
    # Add filters based on provided parameters
    if content_query:
        the_query += ' AND content LIKE %s'
        params.append(f'%{content_query}%')
    
    if author_id:
        the_query += ' AND authorId = %s'
        params.append(author_id)
    
    if post_id:
        the_query += ' AND postId = %s'
        params.append(post_id)
    
    if date_from:
        the_query += ' AND createdAt >= %s'
        params.append(date_from)
    
    if date_to:
        the_query += ' AND createdAt <= %s'
        params.append(date_to)
    
    # Add sorting
    the_query += ' ORDER BY createdAt DESC'
    
    # Execute query
    cursor = db.get_db().cursor()
    cursor.execute(the_query, tuple(params))
    theData = cursor.fetchall()
    
    # Create response
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response