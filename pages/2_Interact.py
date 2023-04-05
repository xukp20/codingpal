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
        # search_page()
        option = st.selectbox(
            'What type do you want to search for',
            ('repo', 'doc', 'solution'))

        ROOT = "http://101.43.131.30:8080/search/" + option

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

        if option == "repo":
            col1, col2 = st.columns(2)

            with col1:
                keyword = st.text_input(
                    "Enter the keyword 👇",
                    '',
                )
                count = st.text_input(
                    "Enter the count you need👇",
                    '',
                )
                require = text_input = st.text_input(
                    "Enter your requirement 👇",
                    '',
                )

            with col2:
                language = st.selectbox(
                    'What language do you want to search for',
                    ('Python', 'Cpp', 'JavaScript', 'Rust', 'none'))
                sort = st.selectbox(
                    'How do you want to sort your search results',
                    ('stars', 'forks', 'updated'))

            if keyword != '' and count != '' and require != '':
                URL = f"{ROOT}?keyword={keyword}&language={language}&sort={sort}&count={count}&require={require}"
                r = requests.get(URL)
                st.markdown(
                    byte2str(r.content)
                )
            else:
                st.warning('Please enter the keyword/count/require')

        elif option == 'doc':
            col1, col2 = st.columns(2)

            with col1:
                keyword = st.text_input(
                    "Enter the key word 👇",
                    '',
                )

            with col2:
                language = st.selectbox(
                    'What language do you want to search for',
                    ('Python', 'Cpp', 'JavaScript', 'Rust', 'none'))

            if keyword != '':
                URL = f"{ROOT}?keyword={keyword}&language={language}"
                r = requests.get(URL)
                st.markdown(
                    byte2str(r.content)
                )
            else:
                st.warning('Please enter the keyword')
        elif option == 'solution':
            col1, col2 = st.columns(2)

            with col1:
                keyword = st.text_input(
                    "Enter the bug trace or any info you want to search for 👇",
                    '',
                )
                require = text_input = st.text_input(
                    "Enter your requirement 👇",
                    '',
                )

            with col2:
                website = st.selectbox(
                    'What website do you want to search for',
                    ('Google', 'Baidu', 'Bing'))

            if keyword != '':
                URL = f"{ROOT}?keyword={keyword}&website={website}&require={require}"
                print(URL)
                r = requests.put(URL)
                st.markdown(
                    byte2str(r.content)
                )
            else:
                st.warning('Please enter the keyword')

strs = ['editor_option', 'editor_caption_info', 'editor_code', 'editor_lang', 'editor_tips']
dicts = ['editor_params', 'editor_result']
bools = ['editor_got_result']
for s in strs:
    if s not in st.session_state:
        st.session_state[s] = ''
        if s == 'editor_lang':
            st.session_state[s] = 'python'
        if s == 'editor_tips':
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
        code = code_editor(st.session_state.editor_code)
        if code['text'] == '':
            st.warning('please press Ctrl + Enter to submit your code')
        elif not st.session_state.editor_got_result:
            st.caption('select tools for your code on the right')

        elif st.session_state.editor_got_result:
            st.warning('please press Ctrl + Enter to submit your code')
            option = st.session_state.editor_option
            if option == "translate":
                print_code(st.session_state.editor_result['code'], st.session_state.editor_result['lang'])
            elif option == "debug":
                st.write(st.session_state.editor_result['info'])
            elif option == "generate":
                print_code(st.session_state.editor_result['text'], code['lang'])
            elif option == "comment":
                print_code(st.session_state.editor_result['code'], code['lang'])
            elif option == "explain":
                st.write(st.session_state.editor_result['text'])
            elif option == 'code2pseudo':
                st.write(st.session_state.editor_result['text'])

        
    with info_col:
        option = st.selectbox("Tools",
            (
                "Completion", "Translate", "Debug", "ToPseudo", "Document", "Comment", "Logic"
            ),
            label_visibility='collapsed'
            )
        st.session_state.editor_caption_info = ''
        if option == "Completion":
            st.session_state.editor_got_result = False
            st.session_state.editor_option = "completion"
            st.session_state.editor_params = {
                "src": code["text"],
            }
            st.session_state.editor_got_result = False

        elif option == "Translate":
            st.session_state.got_result = False
            st.session_state.editor_option = "translate"
            src = st.selectbox("Source Language", LANGUAGES)
            tar = st.selectbox("Target Language", LANGUAGES)
            if src == tar:
                st.warning('The source language and the target language should not be the same')
            st.session_state.editor_params = {
                "code": code["text"],
                "src": src,
                "tar": tar,
            }
            st.session_state.editor_got_result = False


        elif option == "Debug":
            st.session_state.editor_option = "debug"
            st.session_state.editor_got_result = False

        elif option == "ToPseudo":
            st.session_state.editor_option = "code2pseudo"
            st.session_state.editor_got_result = False
            st.session_state.editor_params = {
                "code": code["text"],
            }

        elif option == "Document":
            st.session_state.editor_option = "generate"
            st.session_state.editor_got_result = False
            st.session_state.editor_params = {
                "code": code["text"],
            }
        
        elif option == "Comment":
            st.session_state.editor_option = "comment"
            st.session_state.editor_got_result = False
            st.session_state.editor_params = {
                "code": code["text"],
            }

        elif option == "Logic":
            st.session_state.editor_option = "explain"
            st.session_state.editor_got_result = False
            st.session_state.editor_params = {
                "code": code["text"],
            }

        cols = st.columns(6)
        with cols[5]:
            if st.button("Run", key=1):
                st.session_state.editor_got_result = True
                if st.session_state.editor_option == "completion":
                    res = requests.put(CODING_API + "completion", json=st.session_state.editor_params)
                    st.session_state.editor_code = byte2str(res.content)
                    st.session_state.editor_caption_info = 'Completion Done'
                    st.experimental_rerun()
                elif st.session_state.editor_option == "translate":
                    res = requests.put(CODING_API + "translate", json=st.session_state.editor_params)
                    st.session_state.editor_result['code'] = byte2str(res.content)
                    st.session_state.editor_result['lang'] = st.session_state.editor_params['tar']
                    st.session_state.editor_caption_info = 'Translate Done'
                    st.experimental_rerun()
                elif st.session_state.editor_option == "debug":
                    res = requests.put(CODING_API + "debug", json=st.session_state.editor_params)
                    st.session_state.editor_result['info'] = byte2str(res.content)
                    st.session_state.editor_caption_info = 'Debug Done'
                    st.experimental_rerun()
                elif st.session_state.editor_option == "code2pseudo":
                    res = requests.put(DOCUMENT_API + "code2pseudo", json=st.session_state.editor_params)
                    st.session_state.editor_result['text'] = byte2str(res.content)
                    st.session_state.editor_caption_info = 'ToPseudo Done'
                    st.experimental_rerun()
                elif st.session_state.editor_option == "generate":
                    res = requests.put(DOCUMENT_API + "generate", json=st.session_state.editor_params)
                    st.session_state.editor_result['text'] = byte2str(res.content)
                    st.session_state.editor_caption_info = 'Document Done'
                    st.experimental_rerun()
                elif st.session_state.editor_option == "comment":
                    res = requests.put(DOCUMENT_API + "comment", json=st.session_state.editor_params)
                    print(res.content)
                    st.session_state.editor_result['code'] = byte2str(res.content)
                    st.session_state.editor_caption_info = 'Comment Done'
                    st.experimental_rerun()
                elif st.session_state.editor_option == "explain":
                    res = requests.put(DOCUMENT_API + "explain", json=st.session_state.editor_params)
                    st.session_state.editor_result['text'] = byte2str(res.content)
                    st.session_state.editor_caption_info = 'Logic Done'
                    st.experimental_rerun()
        st.caption(st.session_state.editor_caption_info)
        # else:
        #     st.session_state.caption_info = 'choose the tool you need'
        #     st.session_state.code = code["text"]

            
strs = ['text_option', 'text_caption_info', 'text_code', 'text_lang', 'text_tips', 'text_text']
dicts = ['text_params', 'text_result']
bools = ['text_got_result']
for s in strs:
    if s not in st.session_state:
        st.session_state[s] = ''
        if s == 'text_lang':
            st.session_state[s] = 'python'
        if s == 'text_tips':
            st.session_state[s] = 'please press Ctrl + Enter to submit your code'
for b in bools:
    if b not in st.session_state:
        st.session_state[b] = False
for d in dicts:
    if d not in st.session_state:
        st.session_state[d] = {}



            

def text_page():
    text_col, result_col = st.columns(2)
    with text_col:
        option = st.selectbox("Tools",
            ('Generate', 'Pseudo To Code', 'Text To Pseudo', 'Explain Bug'),
        )
        st.session_state.text_text = st.text_area("Text", '')
        st.session_state.text_caption_info = ''
        if option == 'Generate':
            st.session_state.text_option = 'generate'
            language = st.selectbox("Language", LANGUAGES)
            st.session_state.text_params = {
                'info': st.session_state.text_text,
                'language': language,
            }
            # st.session_state.text_got_result = False

        elif option == 'Pseudo To Code':
            st.session_state.text_option = 'pseudo2code'
            language = st.selectbox("Language", LANGUAGES)
            st.session_state.text_params = {
                "pseudo": st.session_state.text_text,
                "tar": language,
            }
            # st.session_state.text_got_result = False

        elif option == 'Text To Pseudo':
            st.session_state.text_option = 'text2pseudo'
            st.session_state.text_params = {
                "text": st.session_state.text_text,
            }
            # st.session_state.text_got_result = False

        elif option == 'Explain Bug':
            st.session_state.text_option = 'explain_bug'
            st.session_state.text_params = {
                "trace": st.session_state.text_text,
            }
            # st.session_state.text_got_result = False


        if st.button("Run", key=2):
            st.session_state.text_got_result = True
            if st.session_state.text_option == 'generate':
                res = requests.get(CODING_API + "generate?info=" + st.session_state.text_params['info'] + "&language=" + st.session_state.text_params['language'])
                st.session_state.text_result['code'] = byte2str(res.content)
                st.session_state.text_caption_info = 'Generate Done'
                st.experimental_rerun()
            elif st.session_state.text_option == 'pseudo2code':
                res = requests.put(CODING_API + "pseudo2code", json=st.session_state.text_params)
                st.session_state.text_result['code'] = byte2str(res.content)
                st.session_state.text_caption_info = 'Pseudo To Code Done'
                st.experimental_rerun()
            elif st.session_state.text_option == 'text2pseudo':
                res = requests.put(DOCUMENT_API + "text2pseudo?text=" + st.session_state.text_params['text'])
                st.session_state.text_result['text'] = byte2str(res.content)
                st.session_state.text_caption_info = 'Text To Pseudo Done'
                st.experimental_rerun()
            elif st.session_state.text_option == 'explain_bug':
                res = requests.put(DOCUMENT_API + "explain_bug", json=st.session_state.text_params)
                st.session_state.text_result['text'] = byte2str(res.content)
                st.session_state.text_caption_info = 'Explain Bug Done'
                st.experimental_rerun()
        st.caption(st.session_state.text_caption_info)
    
    with result_col:
        if st.session_state.text_got_result:
            if st.session_state.text_option == 'generate':
                print_code(st.session_state.text_result['code'], st.session_state.text_params['language'])
            elif st.session_state.text_option == 'pseudo2code':
                print_code(st.session_state.text_result['code'], st.session_state.text_params['tar'])
            elif st.session_state.text_option == 'text2pseudo':
                st.markdown(st.session_state.text_result['text'])
            elif st.session_state.text_option == 'explain_bug':
                st.markdown(st.session_state.text_result['text'])
        st.session_state.text_got_result = False

def search_page():
    st.title("Search")


main_page()