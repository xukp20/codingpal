import json
from streamlit_tree_select import tree_select
import streamlit as st
from streamlit_chat import message
import requests
import streamlit.components.v1 as components


option = st.selectbox(
    'Your purpose',
    ('Creating a new project', 'Continue editing the previous project'))


def gen_tree(li, dic, n):
    for k, v in dic.items():
        li.append('    |' * n + '-' * 4 + k + '\n')
        gen_tree(li, v, n + 1)


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


dics = ['chat_message']
strs = ['name', 'token', 'doc_tree']
for s in strs:
    if s not in st.session_state:
        st.session_state[s] = ''
for s in dics:
    if s not in st.session_state:
        st.session_state[s] = {}

if option == 'Creating a new project':

    ROOT = "http://101.43.131.30:8080/project/"

    if st.session_state['token'] == '':
        r = requests.get(ROOT + 'create')
        token = byte2str(r.content)[10:-2]
        st.session_state['token'] = token
        print(token)
    else:
        token = st.session_state['token']
    name = st.text_input('Your project name', '')
    st.session_state['name'] = name

    def init_project():
        reply = requests.put(f"{ROOT}init", json={
            "token": st.session_state['token'],
            "name": st.session_state['name'],
        })
        reply = json.loads(reply.content)['reply']
        has_scope = reply.find('{')
        if has_scope != -1:
            right_scope = reply.rfind("}")
            reply = reply[has_scope:right_scope + 1]
            try:
                reply = json.loads(reply)['reply']
            except:
                pass
        st.session_state['chat_message'][str(len(st.session_state['chat_message']))] = \
            ('bot', reply)
    button = st.button('create', on_click=init_project)

    chat_col, file_col = st.columns(2)

    with chat_col:

        st.title('Chat bot')
        if "temp" not in st.session_state:
            st.session_state["temp"] = ""


        def clear_text():
            st.session_state["temp"] = st.session_state["requires"]
            st.session_state["requires"] = ""


        require = st.text_input('Enter your requirements', key="requires", on_change=clear_text)

        if st.session_state["temp"] != '' and st.session_state["temp"] != "file structure":
            st.session_state['chat_message'][str(len(st.session_state['chat_message']))] = \
                ('user', st.session_state["temp"])

            reply = requests.put(f"{ROOT}continue", json={
                "token": st.session_state['token'],
                "require": st.session_state["temp"],
            })
            reply = json.loads(reply.content)['reply']
            has_scope = reply.find('{')
            if has_scope != -1:
                right_scope = reply.rfind("}")
                reply = reply[has_scope:right_scope + 1]
                try:
                    reply = json.loads(reply)['reply']
                except:
                    pass
            st.session_state['chat_message'][str(len(st.session_state['chat_message']))] = \
                ('bot', reply)
        st.session_state["temp"] = ""

        for key, value in st.session_state['chat_message'].items():
            if value[0] == 'user':
                message(value[1], is_user=True, key=key)
            else:
                message(value[1], key=key)
        # html = """
        # <div>
        #   %s
        # </div>
        # """
        #
        # for key, value in st.session_state['chat_message'].items():
        #     if value[0] == 'user':
        #         message_html = f"<p class='user-message'>{value[1]}</p>"
        #     else:
        #         message_html = f"<p class='bot-message'>{value[1]}</p>"
        #     html += message_html
        #
        # components.html(html, height=200, scrolling=True)

    with file_col:
        st.title('Document Tree')

        def gen_doc_tree(li):
            a = []
            for i in range(len(li)):
                docs = li[i].split('/')
                for j in range(len(docs)):
                    a.append('    |' * j + '-' * 4 + docs[j] + '\n')
            return a


        def transform_structure(data):
            result = []
            for item in data:
                keys = item.split('/')
                temp = result
                for key in keys:
                    if key != '':
                        found = False
                        for node in temp:
                            if node['label'] == key:
                                print(key)
                                temp = node['children']
                                found = True
                                break
                        if not found:
                            if key[-3:] == '.py':
                                new_node = {'label': key, 'value': key}
                                temp.append(new_node)
                            else:
                                new_node = {'label': key, 'value': key, 'children': []}
                                temp.append(new_node)
                                temp = new_node['children']
            print(result)
            return result


        def remove_empty_children(node):
            if 'children' in node:
                if len(node['children']) == 0:
                    node.pop('children')
                else:
                    for child in list(node['children']):
                        remove_empty_children(child)


        def get_doc_tree():
            reply = requests.put(f"{ROOT}continue", json={
                "token": st.session_state['token'],
                "require": "file structure",
            })
            reply = json.loads(reply.content)['reply']
            has_scope = reply.find('{')
            if has_scope != -1:
                right_scope = reply.rfind("}")
                reply = reply[has_scope:right_scope + 1]
                try:
                    reply = json.loads(reply)['structure']
                except:
                    pass
            st.session_state['doc_tree'] = reply

        button = st.button('get_tree', on_click=get_doc_tree)
        print(st.session_state['doc_tree'])
        return_select = tree_select(transform_structure(st.session_state['doc_tree']), only_leaf_checkboxes=True)
        st.write(return_select)
# else:
