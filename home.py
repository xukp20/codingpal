import streamlit as st
HELP_LINK = 'https://codingpal-tutorial.streamlit.app/'

st.set_page_config(
        page_title='CodingPal',
        page_icon='🏠',
        initial_sidebar_state='expanded',
        menu_items={
            'About': '2023 Spring by Rookie Team.',
            'Get help': '{}'.format(HELP_LINK)
        }
    )

lang = st.radio("Language", ('English', '中文'), horizontal=True, label_visibility='collapsed')



if lang == 'English':
    st.title("Welcome to CodingPal")
    st.markdown("""
    **CodingPal is a programming tool that helps you write code, fix bugs or even generate a project from scratch.**
    
    ### 👀 Introduction
    The main idea of CodingPal is to use ChatGPT to assist coding.
    In order to provide the bot with more information, we take advantage of online webpages and APIs like:
    - Github search API for repos
    - Bing for searching solutions of bugs
    - Official documentations of programming languages as an addition to the bot's knowledge base
    
    Also, inspired by the idea of building a project with ChatGPT, we constructed the 'Chat' page in which you can explain your idea to the bot and it will generate a project for you.

    ### ❔ How to use
    **👈 Select a page from the sidebar to use CodingPal!**
    
    #### Coding
    This page is for some basic coding tasks that can be categorized into three types:
    - from your code: 
        - Completion, Translation
        - Debug, Generate Document, Comment and explain Logic of the code
    - from text:
        - Generate code from text or pseudocode
        - To comprehensively explain the bug trace from a compiler or interpreter
    - Internet:
        - Search for repos on Github
        - Keywords in official documentations
        - Search for solutions of bugs on Bing
    
    The first two categories are implemented simply on the ability of ChatGPT, while the last one is implemented by using the APIs mentioned above, with ChatGPT to process the search results.
    Usage of this page is simple, and each section is provided with a brief help message.

    #### Chat
    This page is for generating a project from your idea. The bot will ask you some questions about your idea and generate a project for you. The project will be a simple one, but it can be a good start for you to develop your idea.
    As this website is light-weighted, you don't need to login to use this page. However, we will not keep your project, so please remember to download it before you leave the page.
    
    To generate a project:
    - Choose a name for your project
    - Start chatting with the bot
    - Generate the project and download it

    If you need more specific help with examples, see [here]({}), or click the memu button on the right top of any page to choose 'Get help'

    ### ✨ About
    Developed by Rookie team 2023.
    """.format(HELP_LINK))
else:
    st.title("欢迎来到 CodingPal")
    st.markdown("""
    **CodingPal 是一个编程工具，可以帮助你编写代码，修复错误，甚至从头开始生成项目。**

    ### 👀 介绍
    CodingPal 的主要思想是使用 ChatGPT 来辅助编码。
    为了为机器人提供更多信息，我们利用了在线网页和 API，例如：
    - Github 搜索 API 用于搜索仓库
    - Bing 用于搜索错误的解决方案
    - 编程语言的官方文档作为机器人知识库的补充

    此外，受到 ChatGPT 构建项目的想法的启发，我们构建了“聊天”页面，您可以在其中向机器人解释您的想法，它将为您生成一个项目。

    ### ❔ 如何使用
    **👈 从侧边栏选择页面以使用 CodingPal！**

    #### 写代码
    此页面用于一些基本的编码任务，可以分为三类：
    - 来自您的代码：
        - 补全，翻译
        - 调试，生成文档，注释和解释代码的逻辑
    - 来自文本：
        - 从文本或伪代码生成代码
        - 从编译器或解释器的错误跟踪中全面解释错误
    - 网络：
        - 在 Github 上搜索仓库
        - 官方文档中的关键字
        - 在 Bing 上搜索错误的解决方案
    
    前两类是简单地使用 ChatGPT 的能力实现的，而最后一类是通过使用上面提到的 API 实现的，并使用ChatGPT处理搜索结果。
    此页面的使用非常简单，每个部分都提供了简短的帮助信息。

    #### 聊天
    此页面用于从您的想法生成项目。机器人将向您询问有关您的想法的一些问题，并为您生成一个项目。该项目将是一个简单的项目，但它可以成为您开发想法的良好起点。
    由于此网站是轻量级的，因此您无需登录即可使用此页面。但是，我们不会保留您的项目，请在离开页面之前记得下载它。

    生成项目：
    - 为您的项目选择一个名称
    - 与机器人聊天
    - 生成项目并下载

    如果您需要更多具体的帮助示例，请参见[这里]({})，或者点击任一页面右上角菜单中的Get help选项。

    ### ✨ 关于
    Rookie 2023 团队开发。

    另外，中文文档由ChatGPT生成🤣。
    """.format(HELP_LINK))