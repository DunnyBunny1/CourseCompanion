import streamlit as st 
from modules.nav import SideBarLinks

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()
st.write("Welcome to the messages feeds page")