import json
import streamlit as st
import requests
from code_editor import code_editor
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


def generate_markdown_tree(childs, indent_level):
    html = ''
    indent = "  " * indent_level
    for el in childs:
        html += f'''{indent}- {el["label"]}\n'''
        if el.get("children") and len(el["children"]) > 0:
            html += generate_markdown_tree(el["children"], indent_level + 1)
    return html


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
if 'doc_tree' not in st.session_state:
    st.session_state['doc_tree'] = []

ROOT = "http://101.43.131.30:8080/structure/"
ROOT1 = "http://101.43.131.30:8080/file/"
if st.session_state['token'] == '':
    st.title('Creating a new project 🛠️')

    name = st.text_input('Your project name', '')


    def init_project():
        if st.session_state['token'] == '':
            r = requests.get(ROOT + 'create')
            token = byte2str(r.content)[10:-2]
            st.session_state['token'] = token
        st.session_state['name'] = name
        with st.spinner('Please wait a moment···'):
            reply = requests.put(f"{ROOT}init", json={
                "token": st.session_state['token'],
                "name": st.session_state['name'],
            })
        reply = json.loads(reply.content)['reply']

        st.session_state['chat_message'][str(len(st.session_state['chat_message']))] = \
            ('bot', reply)


    button = st.button('create', on_click=init_project)


elif not st.session_state['confirm_tree']:
    progress_text = "Set your doc tree."
    st.progress(25, text=progress_text)

    st.write('\n \n \n \n \n')

    chat_col, file_col = st.columns([2, 1.2], gap='large')

    with chat_col:

        st.title('Chat :speech_balloon:', help='Type your requirements here to build the file structure tree')
        if "temp" not in st.session_state:
            st.session_state["temp"] = ""


        def clear_text():
            st.session_state["temp"] = st.session_state["requires"]
            st.session_state["requires"] = ""


        require = st.text_input('Enter your requirements', key="requires", on_change=clear_text,
                                label_visibility='collapsed')

        if st.session_state["temp"] != '' and st.session_state["temp"] != "file structure":
            st.session_state['chat_message'][str(len(st.session_state['chat_message']))] = \
                ('user', st.session_state["temp"])

            reply = requests.put(f"{ROOT}continue", json={
                "token": st.session_state['token'],
                "require": st.session_state["temp"],
            })

            try:
                st.session_state['doc_tree'] = []
                reply = json.loads(reply.content)['structure']
                for file in reply:
                    if file[-1] != '/':
                        st.session_state['doc_tree'].append(file)
            except:
                pass
            reply = json.loads(reply.content)['reply']
            st.session_state['chat_message'][str(len(st.session_state['chat_message']))] = \
                ('bot', reply)
        st.session_state["temp"] = ""

        chat_block(list(st.session_state['chat_message'].values()))

    with file_col:
        st.title('File Structure :evergreen_tree:')


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
            st.session_state['doc_tree'] = []
            for file in reply:
                if file[-1] != '/':
                    st.session_state['doc_tree'].append(file)


        def generate_tree(childs):
            html = ''
            for el in childs:
                html += f'''
                <ul>
                    <li>
                        {el["label"]}
                '''
                if el.get("children") and len(el["children"]) > 0:
                    html += generate_tree(el["children"])
                html += '</li>'
                html += '</ul>'
            return html


        button = st.button('Show File Structure', on_click=get_doc_tree, key='tree',
                           help='Press this button to view the file structure tree')

        # return_select = tree_select(transform_structure(st.session_state['doc_tree']), disabled=True,
        #                             only_leaf_checkboxes=True)
        st.markdown(generate_markdown_tree(transform_structure(st.session_state['doc_tree']), 0))

        def confirm_tree():
            st.session_state['confirm_tree'] = True
            for i in st.session_state['doc_tree']:
                st.session_state['all_files'][i] = {}
                st.session_state['all_files'][i]['content'] = ''
                st.session_state['all_files'][i]['message'] = {}
                st.session_state['all_files'][i]['had_init'] = False
                st.session_state['all_files'][i]['chat_msg'] = ''


        button2 = st.button('Confirm Tree', on_click=confirm_tree, key='confirm')
    # st.write(return_select)
elif st.session_state['generate'] == '':
    progress_text = "Get file content."
    st.progress(50, text=progress_text)

    st.write('\n \n \n \n \n')

    file_col, chat_col = st.columns(2)

    with file_col:
        st.title('File Structure :evergreen_tree:')
        st.markdown(generate_markdown_tree(transform_structure(st.session_state['doc_tree']), 0))

        col1, col2 = st.columns(2)

        with col1:
            def return_confirm_tree():
                st.session_state['confirm_tree'] = False
                st.session_state['all_files'] = {}

            button1 = st.button('Back', on_click=return_confirm_tree, key='return_confirm_tree')

        with col2:
            def generate_file():
                st.session_state['generate'] = 'gen'


            button2 = st.button('Next step', on_click=generate_file, key='gen_file')

    with chat_col:
        for i, path in enumerate(st.session_state['all_files']):
            with st.expander(path):
                col1, col2 = st.columns(2)

                def init_file(path):
                    print(path)
                    reply = requests.put(f"{ROOT1}init", json={
                        "token": st.session_state['token'],
                        "path": path,
                    })

                    st.session_state['all_files'][path]['message'][
                        str(len(st.session_state['all_files'][path]['message']))] = (
                        'bot', json.loads(reply.content)['reply'])
                    st.session_state['all_files'][path]['had_init'] = True


                with col1:
                    button1 = st.button('init file', on_click=init_file, args=[path], key=path + 'init',
                                        help='Press this button to generate the current file')

                st.session_state['now_open_file'] = path
                if st.session_state['all_files'][path]['had_init']:
                    def clear_text(path):
                        st.session_state['all_files'][path]['chat_msg'] = st.session_state["requires" + path]
                        st.session_state["requires" + path] = ""


                    if st.session_state['all_files'][path]['content'] != '':
                        st.code(st.session_state['all_files'][path]['content'])

                    require = st.text_input('Enter your requirements', key='requires' + path, on_change=clear_text,
                                            args=[path])

                    if st.session_state['all_files'][path]['chat_msg'] != '':
                        st.session_state['all_files'][path]['message'][
                            str(len(st.session_state['all_files'][path]['message']))] = \
                            ('user', st.session_state['all_files'][path]['chat_msg'])
                        st.caption('Because the restriction of OpenAI API, this may take a while')
                        with st.spinner('Please wait a moment···'):
                            reply = requests.put(f"{ROOT1}continue", json={
                                "token": st.session_state['token'],
                                "path": path,
                                "require": st.session_state['all_files'][path]['chat_msg'],
                            })

                        try:
                            st.session_state['all_files'][path]['content'] = json.loads(reply.content)['content']
                        except:
                            pass
                        reply = json.loads(reply.content)['reply']
                        st.session_state['all_files'][path]['message'][
                            str(len(st.session_state['all_files'][path]['message']))] = \
                            ('bot', reply)
                        st.session_state['all_files'][path]['chat_msg'] = ''

                        st.experimental_rerun()

                # st.session_state['all_files'][path]['message'] = {
                #     '1': ('user', 'hello'),
                #     '2': ('bot', 'hi'),
                #     '3': ('user', 'hello'),
                #     '4': ('bot', 'hi'),
                #     '5': ('user', 'hello'),
                #     '6': ('bot', 'hi'),
                # }
                chat_block_nested(list(st.session_state['all_files'][path]['message'].values()), i)

else:
    # if st.session_state['had_generate'] == '':
    #     st.caption('Because the restriction of OpenAI API, this may take a while')
    #     with st.spinner('Generating···'):
    #         reply = requests.put(f"{ROOT}generate?token={st.session_state['token']}")
    #         if reply.status_code == 200:
    #             rep = requests.get(f"{ROOT}download?token={st.session_state['token']}")
    #             file = io.BytesIO(rep.content)
    #             st.session_state['file'] = file
    #     st.session_state['had_generate'] = 'gen'
    #
    # if st.session_state['file']:
    #     st.caption('Generate done')
    #     _, col2, _ = st.columns([1, 2, 1])
    #     with col2:
    #         st.markdown("### Your project is ready!")
    #         st.download_button(
    #             label="Download Zipfile",
    #             data=st.session_state['file'],
    #             file_name='project.zip',
    #             mime='application/octet-stream',
    #         )
    #
    #     # return to continue edit if not satisfied
    #     st.caption('Not satisfied? Click the button below to continue edit')
    #
    if 'progress_per' not in st.session_state or st.session_state['progress_per'] is None:
        st.session_state['progress_per'] = 75
    progress_text = "Edit by yourself" if st.session_state['progress_per'] == 75 else "Download Right Now!"
    st.progress(st.session_state['progress_per'], text=progress_text)

    st.write('\n \n \n \n \n')
    col1, col, col2 = st.columns([1.5, 13, 2])

    def reset():
        st.session_state['generate'] = ''
        st.session_state['had_generate'] = ''
        st.session_state['file'] = None
        st.session_state['progress_per'] = None

    with col1:
        button = st.button('Return', on_click=reset)

    # generate file after clicking
    def generate_file():
        import os
        import zipfile
        DIR_BASE = 'data'
        token = st.session_state['token']
        if not os.path.exists(os.path.join(DIR_BASE, st.session_state['token'])):
            os.makedirs(os.path.join(DIR_BASE, st.session_state['token']))
        with zipfile.ZipFile(os.path.join(DIR_BASE, token + ".zip"), "w") as zipf:
            # files are in st.session_state['all_files']
            for path in st.session_state['all_files']:
                zipf.writestr(path, st.session_state['all_files'][path]['content'])
        zipf.close()
        st.session_state['file'] = io.BytesIO(open(os.path.join(DIR_BASE, token + ".zip"), 'rb').read())
        st.session_state['progress_per'] = 100

    def delete_file():
        import os
        import zipfile
        DIR_BASE = 'data'
        token = st.session_state['token']
        if os.path.exists(os.path.join(DIR_BASE, token)):
            os.removedirs(os.path.join(DIR_BASE, token))
        if os.path.exists(os.path.join(DIR_BASE, token + ".zip")):
            os.remove(os.path.join(DIR_BASE, token + ".zip"))
        st.session_state['file'] = None
        st.session_state['progress_per'] = 75

    with col2:
        if st.session_state['file']:
            download_button = st.download_button(
                    label="Download Zipfile",
                    data=st.session_state['file'] if st.session_state['file'] else None,
                    file_name='project.zip',
                    mime='application/octet-stream',
                    on_click=delete_file
                )
        else:
            generate_button = st.button('Generate project', on_click=generate_file)

    for i, path in enumerate(st.session_state['all_files']):
        with st.expander(path):
            code = code_editor(st.session_state['all_files'][path]['content'], key='code_editor' + path)
            if code['text'] == '':
                st.warning('please press Ctrl + Enter to submit your code')
            else:
                st.session_state['all_files'][path]['content'] = code['text']