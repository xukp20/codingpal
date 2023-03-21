import requests
import streamlit as st

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
