import streamlit as st

st.set_page_config(
    page_title='CodingPal Tutorial',
    page_icon='❔',
    layout="wide",
)

VIDEO_PATH = 'help/videos/'
st.markdown('This page should contains the instructions and examples to use CodingPal')
st.markdown("Under construction...")

with st.expander("Some examples made with CodingPal"):
    tab1, tab2 = st.tabs(['Blog Website', 'Image Classification'])
    with tab1:
        st.write('Blog Website built with CodingPal: use streamlit framework, show posts from the markdown files in the posts folder')
        col1, col2, col3 = st.columns(3)
        with col1:
            with open(VIDEO_PATH + 'blog_gen.mp4', 'rb') as f:
                video_bytes = f.read()
                st.video(video_bytes)
        with col2:
            with open(VIDEO_PATH + 'blog_edit.mp4', 'rb') as f:
                video_bytes = f.read()
                st.video(video_bytes)
        with col3:
            with open(VIDEO_PATH + 'blog_show.mp4', 'rb') as f:
                video_bytes = f.read()
                st.video(video_bytes)

    with tab2:
        st.write('Image Classification based on huggingface API, not finished yet as the API is not working...')
        col1, col2 = st.columns(2)
        with col1:
            with open(VIDEO_PATH + 'class_gen1.mp4', 'rb') as f:
                video_bytes = f.read()
                st.video(video_bytes)
        with col2:
            with open(VIDEO_PATH + 'class_show.mp4', 'rb') as f:
                video_bytes = f.read()
                st.video(video_bytes)

