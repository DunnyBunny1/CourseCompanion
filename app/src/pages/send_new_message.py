import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout="wide")
SideBarLinks()

st.markdown("<h2>➕ Send A New Message</h2>", unsafe_allow_html=True)
st.markdown("---")

with st.form("create_group_chat_form", clear_on_submit=True):
    get_users = requests.get('http://api:4000/u/users/<int:course_id>/<int:section_id>/role/<string:role_id>').json()

    classes = st.multiselect("Choose a Class")

    selected_recipients = st.multiselect("Add Recipients", options=get_users)

    initial_message = st.text_area("Send Message", placeholder="Say something to get the conversation started...")

    submitted = st.form_submit_button("Send New Message", use_container_width=True)




# # Gets a users role
# @users.route('/<id>/role', methods=['GET'])
# def search_user_role(id):
#     cursor = db.get_db().cursor()

#     query = '''
#         SELECT u.userId, firstName, lastName, uc.role, uc.courseId, uc.sectionId
#         FROM users u
#         JOIN user_course uc ON u.userId = uc.userId
#         WHERE u.userId = %s
#     '''
    
#     cursor.execute(query, (id,))
    
#     return_data = cursor.fetchall()
    
#     the_response = make_response(jsonify(return_data))
#     the_response.status_code = 200
#     return the_response
