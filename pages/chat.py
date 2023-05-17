import json
from streamlit_tree_select import tree_select
import streamlit as st
from streamlit_chat import message
import requests
import io
HELP_LINK = 'https://codingpal-tutorial.streamlit.app/'
st.set_page_config(
        page_title='Chat',
        page_icon='💬',
        layout='wide',
        initial_sidebar_state='collapsed',
        menu_items={
            'About': '2023 Spring by Rookie Team.',
            'Get help': '{}'.format(HELP_LINK)
        }
    )

# tools
def message_block(msg, is_user):
            if is_user:                
                st.markdown(f'<p style="background-color:#F7F3F9; margin:2px; margin-inline: 3px; padding: 10px;">  👨 {msg}</p>', unsafe_allow_html=True)
            else:
                st.markdown(f'<p style="background-color:#f3f9f3; margin:2px; margin-inline: 3px; padding: 10px;">  ⚙️ {msg}</p>', unsafe_allow_html=True)

def chat_block(messages):
    history = messages[:-2]
    new = messages[-2:]
    # reverse the history
    history.reverse()
    new.reverse()
    for msg in new:
         message_block(msg[1], msg[0] == 'user')

    st.divider()
    with st.expander('Show History'):
        for msg in history:
            message_block(msg[1], msg[0] == 'user')

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
strs = ['name', 'token', 'doc_tree', 'generate', 'had_generate']
objs = ['file']
for s in strs:
    if s not in st.session_state:
        st.session_state[s] = ''
for s in objs:
    if s not in st.session_state:
        st.session_state[s] = None
for s in dics:
    if s not in st.session_state:
        st.session_state[s] = {}

ROOT = "http://101.43.131.30:8080/project/"
if st.session_state['token'] == '':
    option = st.selectbox(
        'Your purpose',
        ('Creating a new project', 'Continue editing the previous project'))

    if option == 'Creating a new project':

        name = st.text_input('Your project name', '')


        def init_project():
            if st.session_state['token'] == '':
                r = requests.get(ROOT + 'create')
                token = byte2str(r.content)[10:-2]
                st.session_state['token'] = token
                print(token)
            st.session_state['name'] = name

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

elif st.session_state['generate'] == '':
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

        chat_block(list(st.session_state['chat_message'].values()))

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
            return result


        def remove_empty_children(node):
            if 'children' in node:
                if len(node['children']) == 0:
                    node.pop('children')
                else:
                    for child in list(node['children']):
                        remove_empty_children(child)


        def get_doc_tree():
            reply = requests.put(f"{ROOT}structure", json={
                "token": st.session_state['token'],
            })
            reply = json.loads(reply.content)['reply']
            print(reply)
            has_scope = reply.find('{')
            if has_scope != -1:
                right_scope = reply.rfind("}")
                reply = reply[has_scope:right_scope + 1]
                try:
                    reply = json.loads(reply)['structure']
                except:
                    pass
            st.session_state['doc_tree'] = reply


        button = st.button('See File Structure', on_click=get_doc_tree, key='tree')
        return_select = tree_select(transform_structure(st.session_state['doc_tree']), disabled=True,
                                    only_leaf_checkboxes=True)


        def generate_file():
            st.session_state['generate'] = 'gen'


        button2 = st.button('Generate Zip', on_click=generate_file, key='gen')
        # st.write(return_select)
else:
    if st.session_state['had_generate'] == '':
        st.caption('Because the restriction of OpenAI API, this may take a while')
        with st.spinner('Generating···'):
            reply = requests.put(f"{ROOT}generate?token={st.session_state['token']}")
            if reply.status_code == 200:
                rep = requests.get(f"{ROOT}download?token={st.session_state['token']}")
                file = io.BytesIO(rep.content)
                st.session_state['file'] = file
        st.session_state['had_generate'] = 'gen'

    if st.session_state['file']:
        st.caption('Generate done')
        _, col2, _ = st.columns([1, 2, 1])
        with col2:
            st.markdown("### Your project is ready!")
            st.download_button(
                label="Download Zipfile",
                data=st.session_state['file'],
                file_name='project.zip',
                mime='application/octet-stream',
            )

            # return to continue edit if not satisfied
            st.caption('Not satisfied? Click the button below to continue edit')
            
            def reset():
                st.session_state['generate'] = ''
                st.session_state['had_generate'] = ''
                st.session_state['file'] = None
            button = st.button('Return', on_click=reset)



