import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

st.markdown("<h2>🔍 Search & Filter Messages</h2>", unsafe_allow_html=True)
st.markdown("---")

# Sample data for demonstration
messages_data = [
    {"chat": "Study Group for Chemistry", "sender": "Ziming", "message": "Hey, what's up guys"},
    {"chat": "Study Group for Chemistry", "sender": "Max", "message": "Let's review Chapter 3 today"},
    {"chat": "Databases Partner", "sender": "Jeff", "message": "Finished the ER diagram"},
    {"chat": "Fundies Partner", "sender": "Vee", "message": "Ready for the quiz?"},
    {"chat": "Databases Partner", "sender": "Alice", "message": "Add foreign key constraints too"},
    {"chat": "Study Group for Chemistry", "sender": "Vee", "message": "The worksheet was easy"},
]

# Sidebar filters
st.subheader("Filter Options")

chat_options = sorted(list(set(msg["chat"] for msg in messages_data)))
sender_options = sorted(list(set(msg["sender"] for msg in messages_data)))

selected_chat = st.selectbox("Select Chat", ["All"] + chat_options)
selected_sender = st.selectbox("Select Sender", ["All"] + sender_options)
keyword = st.text_input("Search Keyword")

# Filtering logic
def filter_messages():
    filtered = messages_data

    if selected_chat != "All":
        filtered = [msg for msg in filtered if msg["chat"] == selected_chat]

    if selected_sender != "All":
        filtered = [msg for msg in filtered if msg["sender"] == selected_sender]

    if keyword.strip():
        filtered = [msg for msg in filtered if keyword.lower() in msg["message"].lower()]

    return filtered

filtered_messages = filter_messages()

st.markdown("### 📬 Filtered Results")
if filtered_messages:
    for msg in filtered_messages:
        st.markdown(f"""
        **Chat:** {msg['chat']}  
        **Sender:** {msg['sender']}  
        **Message:** _{msg['message']}_  
        ---  
        """)
else:
    st.warning("No messages found matching your filters.")
