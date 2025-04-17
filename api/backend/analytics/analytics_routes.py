from typing import List, Dict, Any, Tuple, Optional 
from flask import Blueprint, request, jsonify, make_response, current_app, Response
from backend.db_connection import db
from pymysql.cursors import DictCursor

analytics = Blueprint("analytics", __name__)

@analytics.route("/engagement", methods=["GET"])
def get_engagement_analytics():
    """
    Retrieves engagement analytics for each course, returning
    courses ranked by most engagement to least engagemnt
    """
    current_app.logger.info('GET /engagement route')
    
    # Get a cursor for our shared DB connection
    cursor: DictCursor = db.get_db().cursor()

    # Retrieve the total # of posts / comments, 
    # as well as the total # of unique posters / commenters
    # across each course. Sorts the courses by total 
    # engagement, as determined by the # of posts + # of
    # comments combined
    query: str = """
    SELECT c.courseId,
       c.sectionId,
       c.courseName,
       COUNT(DISTINCT p.postId)      AS total_posts,
       COUNT(DISTINCT com.commentId) AS total_comments,
       COUNT(DISTINCT p.authorId)    AS unique_posters,
       COUNT(DISTINCT com.authorId)  AS unique_commenters
    FROM courses c
            LEFT JOIN
        posts p ON c.courseId = p.courseId AND c.sectionId = p.sectionId
            LEFT JOIN
        comments com ON p.postId = com.postId
    GROUP BY c.courseId, c.sectionId, c.courseName
    ORDER BY total_posts + total_comments DESC
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

@analytics.route("/avg-enrollment", methods=["GET"])
def get_avg_enrollment():
    """
    Retrieves average enrollment per course section
    """
    current_app.logger.info('GET /analytics/avg-enrollment route')

    # Get a cursor for our shared DB connection
    cursor: DictCursor = db.get_db().cursor()

    # Create a query that reutrns the avg enrollemnt (the number of users in 
    # each class divided by the number of classes) 
    # Display classes as courseId-sectionId string pairs for readability 
    query: str = """
    SELECT 
        COUNT(userId) / COUNT(DISTINCT CONCAT(courseId, '-', sectionId)) AS avgEnrollmentPerSection
    FROM 
        user_course
    """

    # Execute our query and retrieve the data as a python dict
    cursor.execute(query)
    data = cursor.fetchall()

    # Create a 200 ok HTTP response w/ our jsonified data 
    response: Response = make_response(data)
    response.status_code = 200 
    response.mimetype = 'application/json'
    
    return response

@analytics.route("/role-distribution", methods=["GET"])
def get_role_distribution():
    """
    Retrieves the distro of user roles across the platform 
    """
    current_app.logger.info('GET /analytics/role-distribution route')
    
    # Get a cursor for our shared DB connection
    cursor: DictCursor = db.get_db().cursor()

    # Retrieve each role (Student, TA, etc.) and the number of users
    # of that role across all courses. If one user has the same role
    # in multiple courses, we will count them twice 
    query: str = """
    SELECT 
        role,
        COUNT(*) AS count
    FROM 
        user_course
    GROUP BY 
        role
    """

    # Execute our query
    cursor.execute(query)
    data = cursor.fetchall()

    # Create a 200 OK HTTP response w/ our jsonified data    
    response: Response = make_response(data)
    response.status_code = 200 
    response.mimetype = 'application/json'
    
    return response


@analytics.route("/active-hours", methods=["GET"])
def get_active_hours():
    """
    Retrieves the most active hours based on post and comment creation
    """
    current_app.logger.info('GET /analytics/active-hours route')
    
    # Get a cursor for our shared DB connection
    cursor: DictCursor = db.get_db().cursor()

    # Select all the unique created-at times across either post or comments,
    # then group each post/comment by the hour of the day they were made
    query: str = """
    SELECT 
        HOUR(createdAt) AS hour,
        COUNT(*) AS activity_count
    FROM 
        (
            SELECT createdAt FROM posts
            UNION ALL
            SELECT createdAt FROM comments
        ) AS activity
    GROUP BY 
        HOUR(createdAt)
    ORDER BY 
        activity_count DESC
    """

    cursor.execute(query)
    data = cursor.fetchall()

    response: Response = make_response(data)
    response.status_code = 200 
    response.mimetype = 'application/json'
    
    return response



@analytics.route("/avg-posts", methods=["GET"])
def get_avg_posts():
    """
    Retrieves avg number of posts per course section
    """
    current_app.logger.info('GET /analytics/avg-posts route')
    
    # Get a cursor for our shared DB connection
    cursor: DictCursor = db.get_db().cursor()

    
    # Create a query that reutrns the avg nu mber of posts in each class
    # Display classes as courseId-sectionId string pairs for readability 
    query: str = """
    SELECT 
        COUNT(postId) / COUNT(DISTINCT CONCAT(courseId, '-', sectionId)) AS avgPostsPerSection
    FROM 
        posts
    """
    
    # Execute our query
    cursor.execute(query)
    data = cursor.fetchall()

    # Return a 200 ok JSON response 
    response: Response = make_response(data)
    response.status_code = 200 
    response.mimetype = 'application/json'
    
    return response