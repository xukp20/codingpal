import json

import requests
import streamlit as st
from code_editor import code_editor


def byte2str(bytes):
    string = str(bytes, encoding="utf8")
    if string[0] == '"':
        string = string[1:]
    if string[-1] == '"':
        string = string[:-1]
    string = string.replace("\\n", "\n").replace("\\0", "\0").replace(
        "\\'", "\'").replace("\\\\", "\\").replace('\\"',
                                                   '\"').replace("\\r", "\r")
    return string


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
    'What type of service do you want',
    ('Code to pseudo', 'Text to pseudo', 'Generate Document', 'Generate Comment', 'Explain', 'Explain Bug'))

ROOT = "http://101.43.131.30:8080/document/" + option_to_url(option)

if option == 'Code to pseudo':
    tips = st.text('If you are finished typing, press Ctrl+Enter')
    code_str = code_editor('welcome to use code to pseudo')
    if code_str['text'] != '':
        req = {'code': code_str['text']}
        r = requests.put(ROOT, json.dumps(req))
        st.code(
            byte2str(r.content)
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
        st.code(
            byte2str(content)
        )
    else:
        st.warning('Please enter the text', icon="⚠️")
elif option == 'Generate Document':
    tips = st.text('If you are finished typing, press Ctrl+Enter')
    code_str = code_editor('welcome to use generate document')
    if code_str['text'] != '':
        req = {"code": code_str['text']}
        r = requests.put(ROOT, json.dumps(req))
        st.markdown(
            byte2str(r.content)
        )
    else:
        st.warning('Please enter the code', icon="⚠️")
elif option == 'Generate Comment':
    tips = st.text('If you are finished typing, press Ctrl+Enter')
    code_str = code_editor('welcome to use generate comment')
    if code_str['text'] != '':
        req = {'code': code_str['text']}
        r = requests.put(ROOT, json.dumps(req))
        st.code(
            byte2str(r.content)
        )
    else:
        st.warning('Please enter the code', icon="⚠️")
elif option == 'Explain':
    tips = st.text('If you are finished typing, press Ctrl+Enter')
    code_str = code_editor('welcome to use explain')
    if code_str['text'] != '':
        req = {'code': code_str['text']}
        r = requests.put(ROOT, json.dumps(req))
        st.markdown(
            byte2str(r.content)
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
        r = requests.put(ROOT, json.dumps(req))
        st.markdown(
            byte2str(r.content)
        )
    else:
        st.warning('Please enter the code', icon="⚠️")
