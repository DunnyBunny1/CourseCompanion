import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

st.markdown("<h2>➕ Create New Group Chat</h2>", unsafe_allow_html=True)
st.markdown("---")

with st.form("create_group_chat_form", clear_on_submit=True):
    group_name = st.text_input("Group Name", placeholder="Study Group for Chemistry...")
    
    all_users = ["Max", "Jeff", "Vee", "Ziming", "Alice", "Bob"]
    selected_recipients = st.multiselect("Add Recipients", options=all_users)

    initial_message = st.text_area("Initial Message", placeholder="Say something to get the conversation started...")

    submitted = st.form_submit_button("Create Group Chat", use_container_width=True)

if submitted:
    if not group_name.strip():
        st.error("Please enter a group name.")
    elif not selected_recipients:
        st.error("Please select at least one recipient.")
    elif not initial_message.strip():
        st.error("Please write an initial message.")
    else:
        st.success(f"✅ Group '{group_name}' created with {', '.join(selected_recipients)}!")
        st.info(f"Initial message: {initial_message}")
