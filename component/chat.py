from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import streamlit as st
import os 

class Chat:
    
    def __init__(self):
        self.history = []


    def chat(self):
    
        self.template = """Question: {question}

        Answer: I will do my best."""
        self.prompt = ChatPromptTemplate.from_template(self.template)
        self.model = OllamaLLM(model="llama3.1")
        self.chain = self.prompt | self.model

    
        
        question = st.chat_input("Enter your question here")
        if question: 
            response = self.chain.invoke({"question": question})
            st.write(response)

# To run the app
if __name__ == "__main__":
    chat = Chat()
    

