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

def get_my_messages(id: int):
    cursor = db.get_db().cursor()
    query: str = f"""
    SELECT m.content
    FROM user_messages um
    JOIN messages m ON um.messageID = m.messageID
    WHERE um.recipientID = {id} 
    """
    cursor.execute(query)
    data = cursor.fetchall()
    the_response = make_response(data)
    the_response.status_code = 200 
    the_response.mimetype = 'application/json'
    
    return the_response 


def send_message():
    message_data = request.json
    current_app.logger.info(message_data)
    cursor = db.get_db().cursor()

    m_messageId = message_data('messageId')
    m_createdAt = message_data('createdAt')
    m_updatedAt = message_data('updatedAt')
    m_content = message_data('content')
    m_authorID = message_data('authorId')
    um_messageId = m_messageId
    um_recipientId = message_data('recipientId')

    query = """
        INSERT INTO messages (createdAt, updatedAt, content, authorId)
        VALUES (%s,%s,%s,%s)
        INSERT INTO user_messages (messageId, recipientId)
        VALUES (%s,%s)
    """

    values1 = (m_createdAt, m_updatedAt, m_content, m_authorID)
    values2 = (um_messageId, um_recipientId)
    
    current_app.logger.info(query, values1)
    current_app.logger.info(query, values2)    

    cursor.execute(query)
    db.get_db().commit()

    the_response = make_response(jsonify({"message": "Message was successfully sent"}))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

def update_message(message_id : int):
    current_app.logger.info('PUT /messages/<int:message_id> route')
    message_data = request.json
    m_messageID = message_data('messageId')
    m_createdAt = message_data('createdAt')
    m_updatedAt = message_data('updatedAt')
    m_content = message_data('content')
    m_authorID = message_data('authorId')

    query = '''
        UPDATE messages 
        SET messagesId = %s
            createdAt = %s
            updatedAt = %s
            content = %s
            authorId = %s
        where messagesId = %s
    '''

    value = (m_messageID, m_createdAt, m_updatedAt, m_content, m_authorID)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, value)
    db.get_db().commit()

    the_response = make_response(jsonify({"message": "Message was successfully updated"}))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


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

