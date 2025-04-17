import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout="wide")
SideBarLinks()

st.markdown("<h2>🔍 Search & Filter Messages</h2>", unsafe_allow_html=True)
st.markdown("---")


if st.button("Get All My Messages", use_container_width=True):
    messages = requests.get('http://api:4000/m/messages').json()
    try:
        st.dataframe(messages)
    except:
        st.write("Could not connect to database to get messages")




with st.form("Get Specific Message", clear_on_submit=True):
    group_name = st.text_input("Input ID number", placeholder="ID number")
    
    submitted = st.form_submit_button("Search", use_container_width=True)

    if group_name and submitted:
        get_my_messages = requests.get(f'http://api:4000/m/messages/{group_name}').json()
        try:
            st.dataframe(get_my_messages)
        except:
            st.write("Could not connect to database to get messages")
