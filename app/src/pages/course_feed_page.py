from typing import Tuple, List, Dict, Optional, Any
from pprint import pformat
from datetime import datetime 
import logging
from matplotlib import pyplot as plt

import streamlit as st
from modules.nav import SideBarLinks
import requests

logger = logging.getLogger(__name__)

# Set this page as the active page
st.session_state["active_page"] = "course_feed_page"

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

# Write a welcome message to the user 
st.write("## Welcome to the Course Feeds page!")

def get_posts_from_active_class(
    class_data: Dict[str, Tuple[int, int]],
) -> List[Dict[str, Any]]:
    """
    Displays the posts, along w/ their comments, from the active class
    Streamlit will automatically refresh this each time a new choice is made in the dropdown,
    since this function depends on the active class, which depends on the dropdwon choice
    :param class_data: a dictionary mapping each course name to its (sectionId, courseId) pair
    """
    # Retrieve the active class based on the dropdown choice
    course_id, section_id = class_data[st.session_state["active_class_name"]]
    
    # Retrieve all the posts from the active class 
    # Sort the posts by createdAt in descending order
    response: List[Dict[str, Any]] = requests.get(
        url="http://api:4000/po/posts", 
        params={
            "courseId" : course_id, "sectionId" : section_id, "sortBy" : "createdAt"
        }
    ).json()
    
    
    # st.write(response)
    
    return response

    # response: List[Dict[str, Any]] = [
    #     {
    #         "title": "Welcome to AP Basketball",
    #         "postId": 1,
    #         "content": "Welcome to the class! In this course, we will be focusing on advanced basketball techniques and strategies. Looking forward to a great semester!",
    #         "authorId": 3,
    #         "courseId": 3001,
    #         "createdAt": "2025-01-15 09:00:00.000000",
    #         "sectionId": 1,
    #         "updatedAt": None,
    #         "isAnnouncement": 1,
    #     },
    #     {
    #         "title": "Practice Schedule",
    #         "postId": 2,
    #         "content": "Practice sessions will be held on Mondays and Wednesdays from 3 PM to 5 PM. Please bring appropriate gear.",
    #         "authorId": 3,
    #         "courseId": 3001,
    #         "createdAt": "2025-01-16 14:30:00.000000",
    #         "sectionId": 1,
    #         "updatedAt": None,
    #         "isAnnouncement": 1,
    #     },
    #     {
    #         "title": "Ball Handling Drills",
    #         "postId": 3,
    #         "content": "Today we learned some basic ball handling drills.",
    #         "authorId": 3,
    #         "courseId": 3001,
    #         "createdAt": "2025-01-20 16:45:00.000000",
    #         "sectionId": 1,
    #         "updatedAt": None,
    #         "isAnnouncement": 0,
    #     },
    # ]


    # for post in posts:
    #     st.write(pformat(post))


def get_class_data() -> Dict[str, Tuple[int, int]]:
    """
    Run a SQL query to retrieve all of the classes for the currently signed in user
    Returns a dictionary mapping each course name to its (sectionId, courseId) pair
    """
    # TODO: Refactor to use streamlit session state to track userid
    # TOOD: Refactor to use actual flask routes instead of sample data

    # Add the userID in the session state

    # Get the current user ID - this should from SQL
    user_id: int = 3

    # Get the current classes for this user as a list of (courseId, sectionId) pairs
    _ = """
    We need an endpoint that runs this query 
    SELECT courseId, sectionId
    FROM user_courses 
    WHERE userId = {user_id}
    """

    classes_ids: List[Tuple[int, int]] = [
        (2001, 1),
        (3001, 1),
        (4001, 1),
    ]

    # Once we have the class IDs as (course, section) pairs, extract the course name
    _ = """
    SELECT * FROM courses WHERE courseId = <> sectionId =<>
    """
    course_names: List[str] = ["Fundies of CS 1", "Linear Algebra", "AP Basketball"]

    return {
        course_name: class_id
        for course_name, class_id in zip(course_names, classes_ids)
    }

# def convert_date_to_human_readable_format(dt : str): 
    # return datetime.fromisoformat(dt).strftime('%B %d %Y')


def display_post(post: Dict[str, Any]):
    st.markdown(f"### {'📢 ' if post['isAnnouncement'] else '📝 '}{post['title']}")
    
    # Get the authorId of the poster 
    author_id = post["authorId"]
    # Get the name of the author - the response returned is a length-one list, so retrieve the 0th item
    author_info : Dict[str, Any] = requests.get(f"http://api:4000/u/{author_id}").json()[0]
        
    st.markdown(f"*Posted on {post['createdAt']} by {author_info['firstName']} {author_info.get('lastName', '')}*")
    st.write(post["content"])
    

    # If we are on the course feed page, then there could be other multiple posts
    # For the current post, add a button to denote which post we are on
    if st.session_state["active_page"] == "course_feed_page":
        # Add a button to redirect to the selected post page
        if st.button(f"View post", key=f"view_{post['postId']}"):
            st.session_state["selected_post"] = post
            st.switch_page("pages/selected_post_page.py")

        st.markdown("---")  # Add a separator between posts


class_data: Dict[str, Tuple[int, int]] = get_class_data()

def update_class_and_section():
    st.write("Updating class data")
    selected_class = st.session_state["active_class_name"]
    course_id, section_id = class_data[selected_class]
    st.session_state["active_course_id"] = course_id
    st.session_state["active_section_id"] = section_id

# st.write(pformat(class_data))

# Use the keys of our dictionary (the class names) as our dropdown options
class_options = class_data.keys()

# Create a dropdown menu - the response gets returned into the session state
# Streamlit will automatically refresh this (kind of like a pub/sub) after each choice
# The key="active_class_name" will autoamtically save the user choice 
# to active_class_name
st.selectbox(
    "Which class would you like to view the feed for?",
    class_options,
    key="active_class_name",
    on_change=update_class_and_section,
)



# # Set the active class info for future page s
# st.session_state["active_course_id"] = course_id
# st.session_state["active_section_id"] = section_id

st.write("You selected: ", st.session_state["active_class_name"], class_data[ st.session_state["active_class_name"]])


# Create 2 buttons: A new post button (on the left) and a search button the right 
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("New Post"):
        st.switch_page("pages/new_post_page.py")
with col3: 
    if st.button("Search posts"):
        st.switch_page("pages/search_posts_page.py")
    
# Add a separator b/w the search / new post buttons and the rest page 
st.markdown('---')

def add_ret_to_home_button(): 
    """
    Adds the `return to course feed home` button if we are within 
    the course feed subpages but not on the course feed home page 
    """
    if st.session_state["active_page"] == "course_feed_page":
        return 
    if st.button("Return to Course Feed Home page"):
        st.switch_page("pages/course_feed_page.py")


# Get the posts from the active class
# Streamlit will automatically refresh this each time a new choice is made in the dropdown,
# since this function depends on the active class, which depends on the dropdwon choice
class_posts: List[Dict[str, Any]] = get_posts_from_active_class(class_data)


# Display posts in a clean format
for post in class_posts:
    display_post(post)
