import streamlit as st

def message_block(msg, is_user):
            if is_user:                
                st.markdown(f'<p style="background-color:#F7F3F9; margin:2px; margin-inline: 3px; height: 50px; line-height: 30px; padding: 10px;">  👨 {msg}</p>', unsafe_allow_html=True)
            else:
                st.markdown(f'<p style="background-color:#f3f9f3; margin:2px; margin-inline: 3px; height: 50px; line-height: 30px; padding: 10px;">  ⚙️ {msg}</p>', unsafe_allow_html=True)

def chat_block(messages):
    history = messages[:-2]
    new = messages[-2:]
    # reverse the history
    history.reverse()
    new.reverse()
    for msg in new:
         message_block(msg[1], msg[0] == 'user')

    with st.expander('Show History'):
        for msg in history:
            message_block(msg[1], msg[0] == 'user')