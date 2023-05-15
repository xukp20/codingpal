import streamlit as st
from st_pages import Page, show_pages, add_page_title
add_page_title("Home")

show_pages(
    [
        # Page("pages/1_TryOut.py", "Try Out"),
        Page('home.py', "Home", '🏠'),
        Page("pages/2_Interact.py", "Coding", '🧰'),
        Page("pages/chat.py", "Chat", '💬'),
    ]
)

