import streamlit as st
from code_editor import code_editor
import requests
import json

CODING_API = f"http://101.43.131.30:8080/coding/"
SEARCH_API = f"http://101.43.131.30:8080/search/"
DOCUMENT_API = f"http://101.43.131.30:8080/document/"

LANGUAGES = ["Python", "Cpp", "JavaScript", "Rust"]
FUNCTIONS = ["generate", "completion", "translate", "pseudo2code", "debug"]

# tools
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

def print_code(code_str, lang):
            st.code(code_str, lang.lower())

        
def main_page():
    st.set_page_config(
        page_title='CodingPal',
        page_icon='🐍',
        layout='wide',
        initial_sidebar_state='expanded',
    )

    with st.sidebar:
        st.title('Main Page for CodingPal')

    editor_tab, text_tab, search_tab = st.tabs(
        ('Editor', 'Text', 'Search'))

    with editor_tab:
        editor_page()
    with text_tab:
        text_page()
    with search_tab:
        search_page()

strs = ['option', 'caption_info', 'code', 'lang', 'tips']
dicts = ['params', 'result']
bools = ['got_result']
for s in strs:
    if s not in st.session_state:
        st.session_state[s] = ''
        if s == 'lang':
            st.session_state[s] = 'python'
        if s == 'tips':
            st.session_state[s] = 'please press Ctrl + Enter to submit your code'
for b in bools:
    if b not in st.session_state:
        st.session_state[b] = False
for d in dicts:
    if d not in st.session_state:
        st.session_state[d] = {}

def editor_page():
    editor_col, info_col = st.columns(2)
    with editor_col:
        code = code_editor(st.session_state.code)
        if code['text'] == '':
            st.warning('please press Ctrl + Enter to submit your code')
        elif not st.session_state.got_result:
            st.caption('select tools for your code on the right')

        elif st.session_state.got_result:
            st.warning('please press Ctrl + Enter to submit your code')
            option = st.session_state.option
            if option == "translate":
                print_code(st.session_state.result['code'], st.session_state.result['lang'])
            elif option == "debug":
                st.write(st.session_state.result['info'])
            elif option == "generate":
                print_code(st.session_state.result['text'], code['lang'])
            elif option == "comment":
                print_code(st.session_state.result['code'], code['lang'])
            elif option == "explain":
                st.write(st.session_state.result['text'])
            elif option == 'code2pseudo':
                st.write(st.session_state.result['text'])
            st.session_state.got_result = False

        
    with info_col:
        option = st.selectbox("Tools",
            (
                "Completion", "Translate", "Debug", "ToPseudo", "Document", "Comment", "Logic"
            ),
            label_visibility='collapsed'
            )
        if option == "Completion":
            st.session_state.got_result = False
            st.session_state.option = "completion"
            st.session_state.params = {
                "src": code["text"],
            }

        elif option == "Translate":
            st.session_state.got_result = False
            st.session_state.option = "translate"
            src = st.selectbox("Source Language", LANGUAGES)
            tar = st.selectbox("Target Language", LANGUAGES)
            if src == tar:
                st.warning('The source language and the target language should not be the same')
            st.session_state.params = {
                "code": code["text"],
                "src": src,
                "tar": tar,
            }

        elif option == "Debug":
            st.session_state.option = "debug"
            st.session_state.got_result = False

        elif option == "ToPseudo":
            st.session_state.option = "code2pseudo"
            st.session_state.got_result = False
            st.session_state.params = {
                "code": code["text"],
            }

        elif option == "Document":
            st.session_state.option = "generate"
            st.session_state.got_result = False
            st.session_state.params = {
                "code": code["text"],
            }
        
        elif option == "Comment":
            st.session_state.option = "comment"
            st.session_state.got_result = False
            st.session_state.params = {
                "code": code["text"],
            }

        elif option == "Logic":
            st.session_state.option = "explain"
            st.session_state.got_result = False
            st.session_state.params = {
                "code": code["text"],
            }

        cols = st.columns(6)
        with cols[5]:
            if st.button("Run"):
                st.session_state.got_result = True
                if st.session_state.option == "completion":
                    res = requests.put(CODING_API + "completion", json=st.session_state.params)
                    st.session_state.code = byte2str(res.content)
                    st.session_state.caption_info = 'Completion Done'
                    st.experimental_rerun()
                elif st.session_state.option == "translate":
                    res = requests.put(CODING_API + "translate", json=st.session_state.params)
                    st.session_state.result['code'] = byte2str(res.content)
                    st.session_state.result['lang'] = st.session_state.params['tar']
                    st.session_state.caption_info = 'Translate Done'
                    st.experimental_rerun()
                elif st.session_state.option == "debug":
                    res = requests.put(CODING_API + "debug", json=st.session_state.params)
                    st.session_state.result['info'] = byte2str(res.content)
                    st.session_state.caption_info = 'Debug Done'
                    st.experimental_rerun()
                elif st.session_state.option == "code2pseudo":
                    res = requests.put(DOCUMENT_API + "code2pseudo", json=st.session_state.params)
                    st.session_state.result['text'] = byte2str(res.content)
                    st.session_state.caption_info = 'ToPseudo Done'
                    st.experimental_rerun()
                elif st.session_state.option == "generate":
                    res = requests.put(DOCUMENT_API + "generate", json=st.session_state.params)
                    st.session_state.result['text'] = byte2str(res.content)
                    st.session_state.caption_info = 'Document Done'
                    st.experimental_rerun()
                elif st.session_state.option == "comment":
                    res = requests.put(DOCUMENT_API + "comment", json=st.session_state.params)
                    print(res.content)
                    st.session_state.result['code'] = byte2str(res.content)
                    st.session_state.caption_info = 'Comment Done'
                    st.experimental_rerun()
                elif st.session_state.option == "explain":
                    res = requests.put(DOCUMENT_API + "explain", json=st.session_state.params)
                    st.session_state.result['text'] = byte2str(res.content)
                    st.session_state.caption_info = 'Logic Done'
                    st.experimental_rerun()
        st.caption(st.session_state.caption_info)
        # else:
        #     st.session_state.caption_info = 'choose the tool you need'
        #     st.session_state.code = code["text"]

            




            

def text_page():
    st.title('Text Page')

def search_page():
    st.title('Search Page')

main_page()