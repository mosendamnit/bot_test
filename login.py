import streamlit as st

def display_login():

    # Upload data file , you wish to query. 
    with st.sidebar:
        
        # login Section to be show on streamlit
        st.title("🔒 Login")
        st.write("Please enter your email and password to access the ChatBot")

    

        # input feilds for email and password
        email = st.text_input("Enter your email")
        password = st.text_input("Enter your password" , type = "password")

        if st.button("Login"):
            st.write("Login button clicked (backend logic will be add in future )")