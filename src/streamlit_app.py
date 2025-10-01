import streamlit as st
from streamlit_chat import message
from chatbot import RAGChatbot
from PIL import Image

favicon = Image.open("assets/favicon.ico")

st.set_page_config(
    page_title="Rust Documentation Chatbot",
    page_icon=favicon,
)


def on_input_change():
    user_input = st.session_state.user_input
    st.session_state.past.append(user_input)
    chatbot = st.session_state.get('chatbot')
    if not chatbot:
        chatbot = RAGChatbot()
        st.session_state['chatbot'] = chatbot
    with st.spinner("Searching Rust docs..."):
        bot_response = chatbot.generate_response(user_input)
    st.session_state.generated.append({'type': 'normal', 'data': bot_response})

def on_btn_click():
    del st.session_state.past[:]
    del st.session_state.generated[:]

st.session_state.setdefault('past', [])
st.session_state.setdefault('generated', [])

st.title("Rust Documentation Chatbot")

chat_placeholder = st.empty()

with chat_placeholder.container():
    for i in range(len(st.session_state['generated'])):
        message(st.session_state['past'][i], is_user=True, key=f"{i}_user")
        message(
            st.session_state['generated'][i]['data'],
            key=f"{i}",
            allow_html=True,
            is_table=st.session_state['generated'][i].get('type') == 'table'
        )
    st.button("Clear message", on_click=on_btn_click)

with st.container():
    st.text_input("", on_change=on_input_change, key="user_input", placeholder="Ask me anything about Rust programming...")
