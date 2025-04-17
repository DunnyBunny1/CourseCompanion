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
    response = make_response(data)
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
    the_response = make_response(data)
    the_response.status_code = 200 
    the_response.mimetype = 'application/json'
    return the_response 


@messages.route('/messages/<int:recipients_id>', methods=['POST'])
def send_message(recipients_id : List[int]):
    message_data = request.json
    current_app.logger.info(message_data)
    cursor = db.get_db().cursor()
    m_messageId = message_data('messageId')
    m_createdAt = message_data('createdAt')
    m_updatedAt = message_data('updatedAt')
    m_content = message_data('content')
    m_authorID = message_data('authorId')
    um_recipientId = recipients_id
    query = """
            INSERT INTO messages (createdAt, updatedAt, content, authorId)
            VALUES (%s,%s,%s,%s)"""
    for recipientId in um_recipientId:
        query += f"""
            INSERT INTO user_messages (messageId, recipientId)
            VALUES ({m_messageId},{recipientId})
        """
    values1 = (m_createdAt, m_updatedAt, m_content, m_authorID)

    current_app.logger.info(query, values1)

    cursor.execute(query)
    db.get_db().commit()

    the_response = make_response(jsonify({"message": "Message was successfully sent"}))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@messages.route('/messages/<int:message_id>', methods=['PUT'])
def update_message(message_id : int):
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

