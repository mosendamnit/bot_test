import streamlit as st
from component.chat import Bot
from populate_database import main as populate_database_main


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
    
    # Upload data file , you wish to query. 
    with st.sidebar:
        # login Section
        st.title("🔒 Login")
        st.write("Please enter your email and password to access the ChatBot")

        # input feilds for email and password
        email = st.text_input("Enter your email")
        password = st.text_input("Enter your password" , type = "password")
        
        # Login button placeholder
        if st.button("Login"):
            st.write("Login button clicked (backend logic will add tomorrow)")
        st.title("🗂️ Document Upload")
        uploaded_file = st.file_uploader("Upload data file")

        if uploaded_file and not st.session_state.data_uploaded:
            process_uploaded_file(uploaded_file)

    display_chat_messages()
    st.session_state.chat.chat()


if __name__ == "__main__":
    initialize_session_state()
    layout()