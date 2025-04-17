from typing import List 
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
import json
from backend.db_connection import db

messages = Blueprint("messages", __name__)


@messages.route("/messages", methods=["GET"])
def get_all_messages():
    cursor = db.get_db().cursor()
    query: str = """
    SELECT * FROM messages
    """
    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200 
    response.mimetype = 'application/json'
    return response




@messages.route('/messages/<int:user_id>', methods=['GET'])
def get_my_messages(user_id: int):
    cursor = db.get_db().cursor()
    query: str = f"""
        SELECT m.messageId,
        m.content,
        m.createdAt,
        m.authorId,
        GROUP_CONCAT(DISTINCT um.recipientId) AS recipientIds
        FROM messages m
            LEFT JOIN
        user_messages um ON m.messageId = um.messageId
        WHERE m.authorId = {user_id}   
        OR um.recipientId = {user_id} 
        GROUP BY m.messageId
    """
    cursor.execute(query)
    data = cursor.fetchall()
    the_response = make_response(jsonify(data))
    the_response.status_code = 200 
    the_response.mimetype = 'application/json'
    return the_response 



@messages.route('/messages/conversations/<int:user_id>', methods=['GET'])
def get_conversations_for_user(user_id):
    cursor = db.get_db().cursor()

    query = """
        SELECT GROUP_CONCAT(DISTINCT u.firstName ORDER BY u.firstName) AS participants, 
        m.authorId
        FROM user_messages um
        JOIN messages m ON um.messageId = m.messageId
        JOIN users u ON um2.recipientId = u.userId
        WHERE um.recipientId = %s
    """

    cursor.execute(query, (user_id,))
    data = cursor.fetchall()
    the_response = make_response(jsonify(data))
    the_response.status_code = 200 
    the_response.mimetype = 'application/json'
    return the_response 



@messages.route('/messages/people/<int:user_id>', methods=['GET'])
def get_message_people(user_id: int):
    cursor = db.get_db().cursor()
    query = """
        SELECT DISTINCT m.authorId
        FROM messages m
        LEFT JOIN user_messages um ON m.messageId = um.messageId
        WHERE um.recipientId = %s
    """
    cursor.execute(query, (user_id))
    data = cursor.fetchall()
    the_response = make_response(jsonify(data))
    the_response.status_code = 200 
    the_response.mimetype = 'application/json'
    return the_response 










@messages.route('/messages/<int:message_id>', methods=['PUT'])
def update_messages(message_id : int):
    current_app.logger.info('PUT /messages/<int:message_id> route')
    message_data = request.json

    m_content = message_data('content')

    query = f'''
        UPDATE messages 
        SET content = {m_content}
        where messagesId = {message_id}
    '''

    cursor = db.get_db().cursor()
    r = cursor.execute(query)
    db.get_db().commit()

    the_response = make_response(jsonify({"message": "Message was successfully updated"}))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


@messages.route('/messages/<int:message_id>', methods=['DELETE'])
def delete_message(message_id : int):
    current_app.logger.info(f'DELETE /messages/<int:message_id> route')
    cursor = db.get_db().cursor()

    query = f'DELETE FROM posts WHERE postId = {message_id}'
    cursor.execute(query)
    db.get_db().commit()

    the_response = make_response(jsonify({"message": "Message was successfully deleted"}))
    the_response.status_code = 200 
    the_response.mimetype = 'application/json'
    return the_response



@messages.route('/messages/<int:author_id>/<int:user_id>', methods=['GET'])
def get_peoples_messages(author_id: int, user_id: int):
    cursor = db.get_db().cursor()
    query: str = f"""
        SELECT m.content,
        m.createdAt,
        u.firstName, 
        u.lastName,
        GROUP_CONCAT(DISTINCT um.recipientId) AS recipientIds
        FROM messages m
            LEFT JOIN
        user_messages um ON m.messageId = um.messageId
        JOIN users u ON m.authorID = u.userId
        WHERE m.authorId = {user_id}   
        OR um.recipientId = {user_id} 
        AND m.authorId = {author_id}
        GROUP BY m.messageId
    """
    cursor.execute(query)
    data = cursor.fetchall()
    the_response = make_response(jsonify(data))
    the_response.status_code = 200 
    the_response.mimetype = 'application/json'
    return the_response 


