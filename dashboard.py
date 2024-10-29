import streamlit as st
from component.chat import Bot
from populate_database import main as populate_database_main
from feedback import display_feedback_form
from login import display_login


DATA_PATH = "data"

def initialize_session_state():
    """Initialize session state variable"""

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "chat" not in st.session_state:
        st.session_state.chat = Bot()

    if "data_uploaded" not in st.session_state:
        st.session_state.data_uploaded = False


def process_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        
        with open(f"data/{uploaded_file.name}" , "wb") as f:
            f.write(uploaded_file.getbuffer())

        populate_database_main()

        st.session_state.data_uploaded = True


def display_chat_messages():
    """Display chat messages from History"""

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])



def layout():
    """Define the layout of the stream App"""
    st.title ("ChatBot - App 🤖")
    st.write("##### An Intelligent, Document-Based Q&A Assistant for Internal Teams")
    
    # display login on side bar 
    display_login()   
    
    # Login button placeholder
    with st.sidebar:
        
        st.title("🗂️ Document Upload")
        uploaded_file = st.file_uploader("Upload data file")

        if uploaded_file and not st.session_state.data_uploaded:
            process_uploaded_file(uploaded_file)

    display_chat_messages()
    st.session_state.chat.chat()
    

    if st.session_state.messages:
        last_query = st.session_state.messages[-2]["content"]
        last_response = st.session_state.messages[-1]["content"]
        display_feedback_form(last_query , last_response)


if __name__ == "__main__":
    initialize_session_state()
    layout()