import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout="wide")
SideBarLinks()

st.markdown("<h2>➕ Send A New Message</h2>", unsafe_allow_html=True)
st.markdown("---")

temp_user_id = 2

classes = []
class_ids = []
section_ids = []

get_classes = requests.get(f'http://api:4000/crs/courses/of_student/{temp_user_id}').json()

for course in get_classes:
    cId = course['courseId']
    cName = course['courseName']
    sId = course['sectionId']
    
    classes.append(cName)
    class_ids.append(cId)
    section_ids.append(sId)

if 'selected_class_course_id' not in st.session_state:
    st.session_state.selected_class_course_id = None
    st.session_state.selected_class_section_id = None
    st.session_state.selected_class_name = None

with st.form("select_class_form", clear_on_submit=False):
    selected_class_name = st.selectbox("Choose a Class", options=classes)
    submit_class = st.form_submit_button("Submit Class")

    if submit_class:
        num_posn = classes.index(selected_class_name)
        st.session_state.selected_class_course_id = class_ids[num_posn]
        st.session_state.selected_class_section_id = section_ids[num_posn]
        st.session_state.selected_class_name = selected_class_name

if st.session_state.selected_class_course_id is not None:

    get_recipients = requests.get(
        f'http://api:4000/u/users/{st.session_state.selected_class_course_id}/{st.session_state.selected_class_section_id}/role/student'
    ).json()

    recipients = []
    recipients_ids_map = {}

    for user in get_recipients:
        if user['userId'] != temp_user_id:
            fullname = user['firstName'] + " " + user['lastName']
            recipients.append(fullname)
            recipients_ids_map[fullname] = user['userId']

    with st.form("send_message_form", clear_on_submit=False):
        people = st.multiselect("Choose Recipients", options=recipients)
        message_text = st.text_input("Input a new message...")

        submit_message = st.form_submit_button("Send New Message", use_container_width=True)

        if submit_message:
            st.write("Message Sent and Saved")
            st.write("Sent Message: " + message_text)