from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import streamlit as st
import os 

class Bot:
    

    def chat(self):
    
        self.template = """Question: {question}

        Answer: I will do my best."""
        self.prompt = ChatPromptTemplate.from_template(self.template)
        self.model = OllamaLLM(model="llama2", temperature=0.2, max_tokens = 50)
        self.chain = self.prompt | self.model

    
        
        question = st.chat_input("Enter your question here")
        if question: 
            response = self.chain.invoke({"question": question})
            if isinstance(response, str):
                response_text = response  # If it's a string, assign it directly
            else:
                response_text = response.get('text', 'No response text available')
            


            st.session_state.messages.append({"role":"user", "content": question})
            st.session_state.messages.append({"role": "assistant", "content": response_text})

            st.write(response_text)