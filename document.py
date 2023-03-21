import json

import requests
import streamlit as st
from code_editor import code_editor


def option_to_url(string):
    if string == 'Code to pseudo':
        return 'code2pseudo'
    elif string == 'Text to pseudo':
        return 'text2pseudo'
    elif string == 'Generate Document':
        return 'generate'
    elif string == 'Generate Comment':
        return 'comment'
    elif string == 'Explain':
        return 'explain'
    else:
        return 'explain_bug'


option = st.selectbox(
    'What type do you want to search for',
    ('Code to pseudo', 'Text to pseudo', 'Generate Document', 'Generate Comment', 'Explain', 'Explain Bug'))

ROOT = "http://101.43.131.30:8080/document/" + option_to_url(option)

if option == 'Code to pseudo':
    tips = st.text('If you are finished typing, press Ctrl+Enter')
    code_str = code_editor('welcome to use code to pseudo')
    if code_str['text'] != '':
        req = {'code': code_str['text']}
        r = requests.put(ROOT, req)
        content = str(r.content)
        content = content.replace("\\n", "\n").replace("\\0", "\0").replace("\\'", "\'").replace("\\\\", "\\"). \
            replace('\\"', '\"').replace('\\', '')
        st.markdown(
            content
        )
    else:
        st.warning('Please enter the code', icon="⚠️")
elif option == 'Text to pseudo':
    text = st.text_input(
        "Enter the text 👇",
        'welcome to use text to pseudo',
    )
    if text != 'welcome to use text to pseudo':
        URL = f"{ROOT}?text={text}"
        r = requests.put(URL)
        content = r.content
        try:
            content = content.decode("utf-8")[1:-1]
        except:
            content = content.decode("gbk")[1:-1]
        content = content.replace('\\n', '\n')
        st.markdown(
            content
        )
    else:
        st.warning('Please enter the text', icon="⚠️")
elif option == 'Generate Document':
    tips = st.text('If you are finished typing, press Ctrl+Enter')
    code_str = code_editor('welcome to use generate document')
    if code_str['text'] != '':
        req = {'code': json.dumps(code_str['text'])}
        print(req)
        r = requests.put(ROOT, req)
        content = str(r.content)
        content = content.replace("\\n", "\n").replace("\\0", "\0").replace("\\'", "\'").replace("\\\\", "\\"). \
            replace('\\"', '\"').replace('\\', '')
        st.markdown(
            content
        )
    else:
        st.warning('Please enter the code', icon="⚠️")
elif option == 'Generate Comment':
    tips = st.text('If you are finished typing, press Ctrl+Enter')
    code_str = code_editor('welcome to use generate comment')
    if code_str['text'] != '':
        req = {'code': code_str['text']}
        r = requests.put(ROOT, req)
        content = str(r.content)
        content = content.replace("\\n", "\n").replace("\\0", "\0").replace("\\'", "\'").replace("\\\\", "\\"). \
            replace('\\"', '\"').replace('\\', '')
        st.markdown(
            content
        )
    else:
        st.warning('Please enter the code', icon="⚠️")
elif option == 'Explain':
    tips = st.text('If you are finished typing, press Ctrl+Enter')
    code_str = code_editor('welcome to use explain')
    if code_str['text'] != '':
        req = {'code': code_str['text']}
        r = requests.put(ROOT, req)
        content = str(r.content)
        content = content.replace("\\n", "\n").replace("\\0", "\0").replace("\\'", "\'").replace("\\\\", "\\"). \
            replace('\\"', '\"').replace('\\', '')
        st.markdown(
            content
        )
    else:
        st.warning('Please enter the code', icon="⚠️")
else:
    text = st.text_input(
        "Enter the text 👇",
        'welcome to use explain bug',
    )
    if text != 'welcome to use explain bug':
        req = {'trace': text}
        r = requests.put(ROOT, req)
        content = str(r.content)
        content = content.replace("\\n", "\n").replace("\\0", "\0").replace("\\'", "\'").replace("\\\\", "\\"). \
            replace('\\"', '\"').replace('\\', '')
        st.markdown(
            content
        )
    else:
        st.warning('Please enter the code', icon="⚠️")
