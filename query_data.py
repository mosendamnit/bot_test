import argparse
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from embedding_function import embedding_function

CHROMA_PATH = "chroma"
PROMPT_TEMPLATE = """
You are a specialized Zpark project chatbot, designed to assist users by providing clear, concise, and context-driven answers based solely on the provided information.
Your goal is to help users by addressing their questions directly and accurately, ensuring responses are easy to understand.

Guidelines:
- Summarize relevant context briefly before answering, if applicable.
- Structure your response in straightforward sentences or bullet points.
- Provide clear, to-the-point answers, avoiding unnecessary details.
- If more information is needed from the user, indicate this politely.

Context:
{context}

----

Answer the following question based on the above context:
{question}
"""

# function takes user query and send it to query function
def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text" , type=str , help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)

# 
def query_rag(query_text: str):
    
    #Prepare the DB
    embeddings = embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

    #Search the DB
    results = db.similarity_search_with_score(query_text , k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context= context_text , question = query_text)

    model = OllamaLLM(model="llama3.1" , temperature=0.5 , max_token= 150)
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return response_text

if __name__ == "__main__":
    main()
