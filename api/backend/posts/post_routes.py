from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
import json
from backend.db_connection import db

posts = Blueprint('posts', __name__)

# GET /posts - Retrieve all posts with optional filtering parameters [Henry-3] [Jane-2]
@posts.route('/posts', methods=['GET'])
def get_all_posts():
    current_app.logger.info('GET /posts')

    post_id = request.args.get('postId')
    title = request.args.get('title')
    content = request.args.get('content')
    created_at = request.args.get('createdAt')
    updated_at = request.args.get('updatedAt')
    is_announcement = request.args.get('isAnnouncement')
    author_id = request.args.get('authorId')
    course_id = request.args.get('courseId')
    section_id = request.args.get('sectionId')
    sort_by = request.args.get('sortBy', 'createdAt')

    cursor = db.get_db().cursor()

    # Build the base query
    query = '''
        SELECT postId, title, content, createdAt, updatedAt, isAnnouncement, authorId, courseId, sectionId
        FROM posts
    '''

    filters = []
    values = []

    if post_id:
        filters.append("postId = %s")
        values.append(post_id)
    if title:
        filters.append("title LIKE %s")
        values.append(f"%{title}%")
    if content:
        filters.append("content LIKE %s")
        values.append(f"%{content}%")
    if created_at:
        filters.append("DATE(createdAt) = %s")
        values.append(created_at)
    if updated_at:
        filters.append("DATE(updatedAt) = %s")
        values.append(updated_at)
    if is_announcement is not None:
        filters.append("isAnnouncement = %s")
        values.append(is_announcement)
    if author_id:
        filters.append("authorId = %s")
        values.append(author_id)
    if course_id:
        filters.append("courseId = %s")
        values.append(course_id)
    if section_id:
        filters.append("sectionId = %s")
        values.append(section_id)

    if filters:
        query += " WHERE " + " AND ".join(filters)

    allowed_sort_fields = ['postId', 'createdAt', 'updatedAt', 'title']
    if sort_by not in allowed_sort_fields:
        sort_by = 'createdAt'

    query += f" ORDER BY {sort_by} DESC"

    cursor.execute(query, values)
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response





# GET /posts/{id} - Retrieve a specific post by ID [Henry-3]
@posts.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    current_app.logger.info('GET /posts/<int:post_id> route')
    cursor = db.get_db().cursor()
    query = f'''
        SELECT postId, title, content, createdAt, updatedAt, isAnnouncement, authorId, courseId, sectionId
        FROM posts
        WHERE postId = {post_id}
    '''

    cursor.execute(query)
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response





# PUT /posts/{id} - Update an existing post [Henry-6] [Jane-5]
@posts.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    current_app.logger.info('PUT /posts/<int:post_id> route')
    post_data = request.json
    post_id = post_data['postId']
    title = post_data['title']
    content = post_data['content']
    updatedAt = post_data['updatedAt']
    isAnnouncement = post_data['isAnnouncement']
    courseId = post_data['courseId']
    sectionId = post_data['sectionId']

    query = '''
        UPDATE posts 
        SET title = %s, 
            content = %s,
            updatedAt = %s, 
            isAnnouncement = %s, 
            courseId = %s, 
            sectionId = %s, 
        where postId = %s
    '''

    data = (title, content, updatedAt, isAnnouncement, courseId, sectionId, post_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    
    the_response = make_response(jsonify({"message": f"Post {post_id} updated successfully"}))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response





# DELETE /posts/{id} - Delete a specific post [Henry-6] [Jane-5] [Jacobson-5]
@posts.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    current_app.logger.info(f'DELETE /posts/<int:post_id> route')
    cursor = db.get_db().cursor()

    delete_query = f'DELETE FROM posts WHERE postId = {post_id}'
    cursor.execute(delete_query)
    db.get_db().commit()

    the_response = make_response(jsonify({"message": f"Post {post_id} deleted successfully"}))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response





# POST /posts/create - Create a new post [Henry-1] [Henry-2] [Jacobson-4]
@posts.route('/posts/create', methods=['POST'])
def create_post():
    post_data = request.json
    current_app.logger.info(post_data)
    
    post_id = post_data['postId']
    title = post_data['title']
    content = post_data['content']
    createdAt = post_data['createdAt']
    updatedAt = post_data['updatedAt']
    isAnnouncement = post_data['isAnnouncement']
    authorId = post_data['authorId']
    courseId = post_data['courseId']
    sectionId = post_data['sectionId']
    
    query = '''
        INSERT INTO posts (title, content, createdAt, updatedAt, isAnnouncement, authorId, courseId, sectionId)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''

    values = (title, content, createdAt, updatedAt, isAnnouncement, authorId, courseId, sectionId)

    current_app.logger.info(query, values)
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    the_response = make_response(jsonify({"message": f"Post {post_id} created successfully"}))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
