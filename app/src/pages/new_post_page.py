from typing import Tuple, List, Dict, Optional, Any
from pprint import pformat
from datetime import datetime 
import logging
from matplotlib import pyplot as plt

import streamlit as st
from modules.nav import SideBarLinks
import requests
from pages.course_feed_page import add_ret_to_home_button

logger = logging.getLogger(__name__)

# Set this page as the active page
st.session_state["active_page"] = "new_post_page"

# Display the appropriate sidebar links and buttons for the role of the logged in user
add_ret_to_home_button()
SideBarLinks()
