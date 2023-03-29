import streamlit as st
import requests
from code_editor import code_editor
import json

def try_out():
    st.title("Try Out")
    tab1, tab2, tab3 = st.tabs(["Coding", "Search", "Document"])
    with tab1:
        LANGUAGES = ["Python", "Cpp", "JavaScript", "Rust"]
        FUNCTIONS = ["generate", "completion", "translate", "pseudo2code", "debug"]

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

        function = st.selectbox("Function", FUNCTIONS)
        URL = f"http://101.43.131.30:8080/coding/{function}"

        if function == "generate":
            language = st.selectbox("Language", LANGUAGES)
            info = st.text_area("Information")
            if info != "":
                r = requests.get(f"{URL}?info={info}&language={language}")
                print_code(byte2str(r.content), language)
        elif function == "completion":
            input = code_editor("")
            if input["text"] != "":
                form = {
                    "src": input["text"],
                }
                r = requests.put(URL, json.dumps(form))
                print_code(byte2str(r.content), input["lang"])

        elif function == "translate":
            src = st.selectbox("Source Language", LANGUAGES)
            tar = st.selectbox("Target Language", LANGUAGES)
            input = code_editor("", lang=src.lower())
            if src == tar:
                st.error("Source and target languages are the same!")
            elif input["text"] != "":
                form = {
                    "code": input["text"],
                    "src": src,
                    "tar": tar,
                }
                r = requests.put(URL, json.dumps(form))
                print_code(byte2str(r.content), tar)

        elif function == "pseudo2code":
            tar = st.selectbox("Target Language", LANGUAGES)
            input = code_editor("")
            if input["text"] != "":
                form = {
                    "pseudo": input["text"],
                    "tar": tar,
                }
                r = requests.put(URL, json.dumps(form))
                print_code(byte2str(r.content), tar)
        else:
            input = code_editor("")
            if input["text"] != "":
                form = {
                    "code": input["text"],
                }
                r = requests.put(URL, json.dumps(form))
                print_code(byte2str(r.content), input["lang"])

    with tab2:
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
                    "Enter your count 👇",
                    '',
                )
                require = text_input = st.text_input(
                    "Enter your require 👇",
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
                st.warning('Please enter the keyword/count/require', icon="⚠️")

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
                st.warning('Please enter the keyword', icon="⚠️")
        elif option == 'solution':
            col1, col2 = st.columns(2)

            with col1:
                keyword = st.text_input(
                    "Enter the key word 👇",
                    '',
                )
                require = text_input = st.text_input(
                    "Enter your require 👇",
                    '',
                )

            with col2:
                website = st.selectbox(
                    'What language do you want to search for',
                    ('Google', 'Baidu', 'Bing'))

            if keyword != '':
                URL = f"{ROOT}?keyword={keyword}&website={website}&require={require}"
                print(URL)
                r = requests.put(URL)
                st.markdown(
                    byte2str(r.content)
                )
            else:
                st.warning('Please enter the keyword', icon="⚠️")
    with tab3:
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

try_out()