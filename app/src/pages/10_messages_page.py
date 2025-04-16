import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

st.markdown("<h2 style='margin-bottom: 0;'>📨 Messages Feed</h2>", unsafe_allow_html=True)

with st.container():
    col1, col2, spacer = st.columns([2, 2, 6])
    with col1:
        if st.button("New Group Chat", use_container_width=True):
            st.switch_page('pages/11_new_group_chat_page.py')

    with col2:
        if st.button("Search Messages", use_container_width=True):
            st.switch_page('pages/12_filter_messages_page.py')

st.markdown("---")

if "selected_chat" not in st.session_state:
    st.session_state.selected_chat = "Study Group for Chemistry"

left_col, right_col = st.columns([2, 6])

with left_col:
    st.subheader("Chats")

    chat_items = [
        ("Study Group for Chemistry", "Today, 8:38 PM"),
        ("Databases Partner", "Today, 6:30 PM"),
        ("Fundies Partner", "Today, 6:20 PM"),
    ]

    for chat_title, timestamp in chat_items:
        label = f"{chat_title}\n{timestamp}"
        if st.button(label, use_container_width=True, key=chat_title):
            st.session_state.selected_chat = chat_title

with right_col:
    selected_chat = st.session_state.selected_chat
    st.subheader(selected_chat)
    st.markdown("**To: Max, Jeff, Vee, Ziming**")

    with st.container():
        st.markdown("##### Ziming: `Hey, what's up guys`")

    st.text_input("Text Message", placeholder="Type a message and press Enter to send...")
