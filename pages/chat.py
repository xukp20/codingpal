import streamlit as st
from streamlit_chat import message
from streamlit_tree_select import tree_select

chat_col, file_col = st.columns(2)


def gen_tree(li, dic, n):
    for k, v in dic.items():
        li.append('    |' * n + '-' * 4 + k + '\n')
        gen_tree(li, v, n+1)


with chat_col:
    st.title('Chat bot')
    strs = ['chat_message']
    for s in strs:
        if s not in st.session_state:
            st.session_state[s] = {}

    st.session_state['chat_message']['1'] = ('bot', 'What can I do for you')
    st.session_state['chat_message']['2'] = ('user', 'I want to generate a Vue-based frontend')

    require = st.text_input('Enter your requirements', '')
    if require != '':
        st.session_state['chat_message'][str(len(st.session_state['chat_message']) + 1)] = \
            ('user', require)

    for key, value in st.session_state['chat_message'].items():
        if value[0] == 'user':
            message(value[1], is_user=True, key=key)
        else:
            message(value[1], key=key)

    st.session_state['chat_message']['3'] = ('bot', 'ok')

with file_col:
    st.title('Document Tree')
    st.text('This is an example')
    dic_doc = {
        'f1': {'f2': {}, 'f3': {}},
        'f4': {'f5': {'f6': {}}}
    }
    doc_tree = ''
    level = 0
    l = []
    gen_tree(l, dic_doc, level)
    for i in l:
        doc_tree += i
    st.text(doc_tree)

    # nodes = [
    #     {
    #         'label': 'F1',
    #         'value': 'f1',
    #         'children': [
    #             {
    #                 'label': 'F2',
    #                 'value': 'f2'
    #             },
    #             {
    #                 'label': 'F3',
    #                 'value': 'f3'
    #             }
    #         ]
    #     },
    #     {
    #         'label': 'F4',
    #         'value': 'f4',
    #         'children': [
    #             {
    #                 'label': 'F5',
    #                 'value': 'f5',
    #                 'children': [
    #                     {
    #                         'label': 'F6',
    #                         'value': 'f6'
    #                     }
    #                 ]
    #             }
    #         ]
    #     }
    # ]
    # return_select = tree_select(nodes, only_leaf_checkboxes=True, no_cascade=True)
    # st.write(return_select)

