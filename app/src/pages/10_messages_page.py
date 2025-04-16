import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")

# Sidebar
SideBarLinks()

# Page configuration
st.markdown("<h2 style='margin-bottom: 0;'>📨 Messages Feed</h2>", unsafe_allow_html=True)

# === Top Buttons ===
with st.container():
    col1, col2, spacer = st.columns([2, 2, 6])
    with col1:
        st.button("New Message", use_container_width=True)
    with col2:
        st.button("Search Messages", use_container_width=True)



st.markdown("---")

# === Main Layout: Left = Chat List | Right = Chat Display ===
left_col, right_col = st.columns([2, 6])

# --- Left Panel: Message Feed ---
with left_col:
    st.subheader("Chats")

    chat_items = [
        ("Negative KL divergence values", "Today, 8:38 PM"),
        ("Coding Exam Q6", "Today, 6:30 PM"),
        ("Question 3 Coding Final", "Today, 6:20 PM"),
        ("Analyzing PCA", "Today, 5:44 PM"),
    ]
    for chat, time in chat_items:
        st.markdown(f"**{chat}**  \n<small>{time}</small>", unsafe_allow_html=True)
        st.markdown("---")

# --- Right Panel: Chat Window ---
with right_col:
    st.subheader("To: Max, Jeff, Vee, Ziming")
    
    # Chat window area
    with st.container():
        st.markdown("##### Ziming: `Hey, what's up guys`")
    
    # Message input
    st.text_input("Text Message", placeholder="Type a message and press Enter to send...")
