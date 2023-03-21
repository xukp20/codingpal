import requests
from code_editor import code_editor
import streamlit as st
import json

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
