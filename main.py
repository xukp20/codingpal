import streamlit as st
from st_pages import Page, show_pages, add_page_title

KEY = 'Rookie'
if 'invite_key' not in st.session_state:
    st.session_state['invite_key'] = ''

if st.session_state['invite_key'] == '':
    # set title to be Login
    st.set_page_config(
        page_title='Login',
        page_icon='🔑'
    )
    st.text_input('Please input invite key', key='invite_key')
elif st.session_state['invite_key'] != KEY:
    st.set_page_config(
        page_title='Login',
        page_icon='🔑'
    )
    st.error('Wrong invite key')
    st.text_input('Try again or contact Rookie Team for invite key', key='invite_key')
else:
    st.title("Welcome to CodingPal")
    st.markdown("Choose a page from the sidebar to use CodingPal!")
    st.caption("By Rookie Team @ 2023")
    st.balloons()
    show_pages(
        [
            # Page("pages/1_TryOut.py", "Try Out"),
            Page('home.py', "Home", '🏠'),
            Page("multipages/2_Interact.py", "Coding", '🧰'),
            Page("multipages/chat.py", "Chat", '💬'),
        ]
    )
    # switch to home page
    # st.experimental_rerun()

