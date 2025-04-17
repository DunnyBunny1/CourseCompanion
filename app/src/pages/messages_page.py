import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

st.markdown("<h2 style='margin-bottom: 0;'>📨 Messages Feed</h2>", unsafe_allow_html=True)

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

with left_col:
    st.subheader("Chats")

    chat_num = 0

    recipients = [
        ("**To: Max, Jeff, Donovan**", 1),
        ("**To: Max, Jeff, Vee**", 2),
        ("**To: Max, Ziming**", 3),
    ]

    messages = [
        (),
        ("Max: Yo, my initals spell out AI", "Jeff: Yo what???", "Donovan: No way man"),
        ("Jeff: What happened to Vee?", "Max: I happened", "Vee: No, I'm still here :)"),
        ("Ziming: Yo what's up", "Max: Huh")
    ]

    for (recipient, num_chat) in recipients:
        label = f"{recipient}"
        if st.button(label, use_container_width=True, key=recipient):
            st.session_state.selected_chat = recipient
            chat_num = num_chat

with right_col:
    selected_chat = st.session_state.selected_chat
    st.subheader(selected_chat)

    for message in messages[chat_num]:
        st.markdown(message)



