from typing import Tuple, List, Dict, Optional, Any
from pprint import pformat
import logging
from datetime import datetime 

from matplotlib import pyplot as plt

import streamlit as st
from modules.nav import SideBarLinks
import requests
from pages.course_feed_page import display_post, add_ret_to_home_button


# Set this page as the active page 
st.session_state["active_page"] = "selected_post_page"

# Display the appropriate sidebar links and buttons for the role of the logged in user
add_ret_to_home_button()
SideBarLinks()



    

def display_comment(comment : Dict[str, Any]): 
    # TODO: Consider changing the comment icon based on the commenter's role 
        
    # Get the authorId of the commenter 
    author_id = comment["authorId"]
    # Get the name of the author - the response returned is a length-one list, so retrieve the 0th item
    author_info : Dict[str, Any] = requests.get(f"http://api:4000/u/{author_id}").json()[0]
        
    # Title the comment by saying "By <author first> <aiuthor last> "
    st.markdown(f"###### Comment by {author_info['firstName']} {author_info.get('lastName', '')}")
        
    st.markdown(f"*Posted on {(comment['createdAt'])}*")
    st.write(comment["content"])
    

    # We also want to display the replies of the comment, so retrieve those too
    # TODO: Figure out how to handle replies, since replioes laos store ptsrs to parents 
            
    st.write("\n")  # Add a separator between posts
    


def get_post_comments(): 
    """
    Retrieves comments for the selected post of this page 
    from our Flask API 
    """
    # Retrieve the comments for the current post 
    response = requests.get(
        'http://api:4000/cmt/comments/search',
        params={
            "postId" : st.session_state["selected_post"]['postId']
        }
    )
    
    return response.json()


# Get the comments for each post as a mapping of post Id's to a list of comment dictionaries 
# post_comments : List[List[Dict[str, Any]]] = get_comments_from_posts(class_posts)
# st.write(f"You are viewing post {st.session_state['selected_post']['postId']}")

# Display the active post 
display_post(st.session_state['selected_post'])

# Add a separator b/w the post and all of its comments
st.markdown("---")  

comments : List[Dict[str, Any]] = get_post_comments()

for comment in comments: 
    display_comment(comment)

