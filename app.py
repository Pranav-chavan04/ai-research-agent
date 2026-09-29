import streamlit as st
from main import app


st.set_page_config(
    page_title="Nexus",
    page_icon="◈",
    layout="wide"
)


st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stApp {
        background: #0b0d10;
        color: #e7e9ed;
    }

    [data-testid="stSidebar"] {
        background: #101216;
        border-right: 1px solid #20242b;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.5rem;
    }

    .brand {
        font-size: 20px;
        font-weight: 600;
        letter-spacing: -0.5px;
        margin-bottom: 24px;
    }

    .new-chat {
        background: #191c22;
        border: 1px solid #292e37;
        border-radius: 8px;
        padding: 10px 12px;
        margin-bottom: 20px;
        text-align: center;
        font-size: 14px;
    }

    .history-title {
        color: #777d87;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 10px;
    }

    .chat-title {
        color: #b7bbc3;
        font-size: 14px;
        padding: 9px 8px;
        border-radius: 7px;
        margin-bottom: 2px;
    }

    .chat-title:hover {
        background: #191c22;
    }

    .main-title {
        font-size: 32px;
        font-weight: 600;
        letter-spacing: -1px;
        margin-top: 18vh;
        text-align: center;
    }

    .subtitle {
        color: #777d87;
        text-align: center;
        margin-top: 8px;
        margin-bottom: 35px;
    }

    .message-container {
        max-width: 820px;
        margin: auto;
    }

    .user-message {
        background: #191c22;
        border: 1px solid #242932;
        border-radius: 12px;
        padding: 12px 16px;
        margin: 12px 0 20px auto;
        max-width: 75%;
    }

    .assistant-message {
        padding: 10px 0;
        margin: 10px 0 25px 0;
        line-height: 1.7;
    }

    .role {
        font-size: 12px;
        color: #737984;
        margin-bottom: 5px;
    }

    [data-testid="stChatInput"] {
        border-top: 1px solid #20242b;
        background: #0b0d10;
    }

    [data-testid="stChatInput"] textarea {
        background: #15181d;
        border: 1px solid #292e37;
        border-radius: 12px;
    }

    .empty-state {
        text-align: center;
        margin-top: 20vh;
    }

    .suggestion {
        display: inline-block;
        background: #13161b;
        border: 1px solid #242932;
        border-radius: 10px;
        padding: 12px 15px;
        margin: 5px;
        color: #aeb3bc;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)


if "messages" not in st.session_state:
    st.session_state.messages = []


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


with st.sidebar:

    st.markdown(
        '<div class="brand">◈ Nexus</div>',
        unsafe_allow_html=True
    )

    if st.button(
        "+  New conversation",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        '<div class="history-title">Conversations</div>',
        unsafe_allow_html=True
    )

    for title in st.session_state.chat_history:
        st.markdown(
            f'<div class="chat-title">{title}</div>',
            unsafe_allow_html=True
        )


if not st.session_state.messages:

    st.markdown(
        '<div class="empty-state">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-title">How can I help?</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Search the web, write code, or explore an idea.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="text-align:center;">
            <span class="suggestion">Research a topic</span>
            <span class="suggestion">Build a Python script</span>
            <span class="suggestion">Explain LangGraph</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class="message-container">
                <div class="user-message">
                    {message["content"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="message-container">
                <div class="assistant-message">
                    <div class="role">Nexus</div>
                    {message["content"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


user_input = st.chat_input(
    "Message Nexus..."
)


if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    if not st.session_state.chat_history:
        title = user_input[:35]

        st.session_state.chat_history.append(
            title
        )

    messages = [
        (
            message["role"],
            message["content"]
        )
        for message in st.session_state.messages
    ]

    with st.spinner("Thinking..."):

        result = app.invoke({
            "messages": messages
        })

        content = result["messages"][-1].content

        if isinstance(content, str):

            response = content

        else:

            response = "\n".join(
                block["text"]
                for block in content
                if isinstance(block, dict)
                and block.get("type") == "text"
                and "text" in block
            )

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.rerun()