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
        st.markdown(
            f'<p style="background-color:#F7F3F9; margin:2px; margin-inline: 3px; padding: 10px;">  👨 {msg}</p>',
            unsafe_allow_html=True)
    else:
        st.markdown(
            f'<p style="background-color:#f3f9f3; margin:2px; margin-inline: 3px; padding: 10px;">  ⚙️ {msg}</p>',
            unsafe_allow_html=True)


def chat_block(messages):
    history = messages[:-2]
    new = messages[-2:]
    # reverse the history
    history.reverse()
    new.reverse()
    for msg in new:
        print(msg[1])
        message_block(msg[1], msg[0] == 'user')

    st.divider()
    with st.expander('Show History'):
        for msg in history:
            message_block(msg[1], msg[0] == 'user')


def chat_block_nested(messages, i):
    history = messages[:-2]
    new = messages[-2:]
    # reverse the history
    history.reverse()
    new.reverse()
    for msg in new:
        print(msg[1])
        message_block(msg[1], msg[0] == 'user')

    st.divider()
    if st.checkbox('Show History', key='checkbox' + str(i)):
        for msg in history:
            message_block(msg[1], msg[0] == 'user')


def gen_tree(li, dic, n):
    for k, v in dic.items():
        li.append('    |' * n + '-' * 4 + k + '\n')
        gen_tree(li, v, n + 1)


def transform_structure(data):
    result = []
    i = 0
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
                    if '.' in key:
                        new_node = {'label': key, 'value': key + str(i)}
                        i += 1
                        temp.append(new_node)
                    else:
                        new_node = {'label': key, 'value': key + str(i), 'children': []}
                        i += 1
                        temp.append(new_node)
                        temp = new_node['children']
    return result


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


dics = ['chat_message', 'all_files']
strs = ['name', 'token', 'doc_tree', 'generate', 'had_generate', 'now_open_file']
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
if 'confirm_tree' not in st.session_state:
    st.session_state['confirm_tree'] = False

ROOT = "http://101.43.131.30:8080/structure/"
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

            st.session_state['chat_message'][str(len(st.session_state['chat_message']))] = \
                ('bot', reply)


        button = st.button('create', on_click=init_project)

elif not st.session_state['confirm_tree']:
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

            try:
                st.session_state['doc_tree'] = json.loads(reply.content)['structure']
            except:
                pass
            reply = json.loads(reply.content)['reply']
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


        def get_doc_tree():
            reply = requests.put(f"{ROOT}get", json={
                "token": st.session_state['token'],
            })

            reply = json.loads(reply.content)['structure']
            st.session_state['doc_tree'] = reply

        button = st.button('See File Structure', on_click=get_doc_tree, key='tree')
        return_select = tree_select(transform_structure(st.session_state['doc_tree']), disabled=True,
                                only_leaf_checkboxes=True)


        def confirm_tree():
            print('here')
            st.session_state['confirm_tree'] = True
            for i in st.session_state['doc_tree']:
                st.session_state['all_files'][i] = {}
                st.session_state['all_files'][i]['content'] = ''
                st.session_state['all_files'][i]['message'] = {}


        button2 = st.button('Confirm Tree', on_click=confirm_tree, key='confirm')
    # st.write(return_select)
elif st.session_state['generate'] == '':

    file_col, chat_col = st.columns(2)

    with file_col:
        file_tree = tree_select(transform_structure(st.session_state['doc_tree']), disabled=True,
                                only_leaf_checkboxes=True)


    def generate_file():
        st.session_state['generate'] = 'gen'


    button2 = st.button('Generate Zip', on_click=generate_file, key='gen')

    with chat_col:
        for i, path in enumerate(st.session_state['all_files']):
            with st.expander(path):
                def modify_file():
                    st.session_state['now_open_file'] = path


                button = st.button('modify file', on_click=modify_file, key=path)
                st.session_state['now_open_file'] = path
                # st.write(st.session_state['all_files'][i])
                st.write(st.session_state['doc_tree'][i])
                st.session_state['all_files'][path]['content'] = '1233323'
                st.write(st.session_state['all_files'][path]['content'])
                st.session_state['all_files'][path]['message'] = {
                    '1': ('user', 'hello'),
                    '2': ('bot', 'hi'),
                    '3': ('user', 'hello'),
                    '4': ('bot', 'hi'),
                    '5': ('user', 'hello'),
                    '6': ('bot', 'hi'),
                }
                chat_block_nested(list(st.session_state['all_files'][path]['message'].values()), i)

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
