import streamlit as st
from component.chat import Bot


def initialize_session_state():
    """Initialize session state variable"""

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "chat" not in st.session_state:
        st.session_state.chat = Bot()

def display_chat_messages():
    """Display chat messages from History"""

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])



def layout():
    """Define the layout of the stream App"""
    st.title ("ChatBot- App")
    st.write("This is an testing Bot")


    display_chat_messages()
    st.session_state.chat.chat()


if __name__ == "__main__":
    initialize_session_state()
    layout()