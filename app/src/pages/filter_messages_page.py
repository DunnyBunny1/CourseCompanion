import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout="wide")
SideBarLinks()

st.markdown("<h2>🔍 Search & Filter Messages</h2>", unsafe_allow_html=True)
st.markdown("---")

tempid = 1

if st.button("Get All My Messages", use_container_width=True):
    messages = requests.get(f'http://api:4000/m/messages/{tempid}').json()
    content_list = []
    time_list = []
    
    for message in messages:
        content_list.append(message['content'])
        time_list.append(message['createdAt'])
    try:
        for i in range(len(content_list)):
            st.write("**" + content_list[i] + "**")
            st.write(time_list[i])
    except:
        st.write("Could not connect to database to get messages")


with st.form("Get Specific Message", clear_on_submit=False):
    message_selected = requests.get(f'http://api:4000/m/messages/people/{tempid}').json()
    
    authors = []
    author_id_key = {}

    for m in message_selected:
        author_id = m['authorId']

        author_info = requests.get(f'http://api:4000/u/users/{author_id}').json()


        first_name = author_info[0]['firstName']
        last_name = author_info[0]['lastName']

        full_name = f"{first_name} {last_name}"
        authors.append(full_name)
        author_id_key.update({full_name: author_id})

    message_list = []

    message_select = st.selectbox("Find Your Messages", options=authors)

    submitted = st.form_submit_button("Search", use_container_width=True)
    if submitted:
        get_my_messages = requests.get(f'http://api:4000/m/messages/{author_id_key[message_select]}/{tempid}').json()
        try:
            content_list = []
            time_list = []
            name_list = []
            for message in get_my_messages:
                content_list.append(message['content'])
                time_list.append(message['createdAt'])
                name_list.append(message['firstName'] + " " + message['lastName'])
            
            try:
                for i in range(len(content_list)):
                    st.write("**FROM: " + name_list[i] + " : " + content_list[i] + "**")
                    st.write(time_list[i])
            except:
                st.write("Could not connect to database to get messages")
        except:
            st.write("Could not connect to database to get messages")
