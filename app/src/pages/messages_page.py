import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout="wide")
SideBarLinks()

st.markdown("<h2 style='margin-bottom: 0;'>📨 Messages Feed</h2>", unsafe_allow_html=True)

tempid = 1

with st.container():
    col1, col2, spacer = st.columns([2, 2, 6])
    with col1:
        if st.button("Send New Message", use_container_width=True):
            st.switch_page('pages/send_new_message.py')

    with col2:
        if st.button("Search Messages", use_container_width=True):
            st.switch_page('pages/filter_messages_page.py')

st.markdown("---")

if "selected_chat" not in st.session_state:
    st.session_state.selected_chat = "None"

left_col, right_col = st.columns([2, 6])

chat_num = 0
messages = []
chats = requests.get(f'http://api:4000/m/messages/{tempid}').json()

with left_col:
    st.subheader("Chats")


    list = []

    for chat in chats:
        if str(chat["authorId"]) not in list:
            x = chat["authorId"]
            author_name = requests.get(f"http://api:4000/u/users/{x}").json()
            first_name = author_name[0]['firstName']
            st.button(label=first_name)  
            list.append(str(chat["authorId"]))


    # chats = requests.get(f'http://api:4000/m/messages/{tempid}').json()
    # current_user = requests.get(f'http://api:4000/u/users/{tempid}').json()
    # current_first_name = current_user[0]['firstName']

    # recipients = []

    # for chat in chats:
    #     id = chat['authorId']
    #     json_name = requests.get(f"http://api:4000/u/users/{id}").json()
    #     first_name = json_name[0]['firstName']
    #     recipients.append(first_name)

    # if tempid in recipients:
    #     recipients.removeAll(current_first_name)
    #     chat.removeAll(tempid)

    # buttons = []
    # recipients_string = "TO: "

    # for i in range(len(chat)):
    #     recipients_string += recipients[i] + ", "
    #     button = st.button(recipients_string)
    #     buttons.append(button)
    #     if button:
    #         st.session_state.selected_chat = recipients[i]
    #         chat_num = chats[i]['author_id']
        

with right_col:

    messages = [
        "Hey, what's up!",
        "Yo",
        "When is the test?",
        "You good to hang out tomorrow",
        "Sorry, I'm busy"
    ]

    for m in messages:
        st.write(m)


