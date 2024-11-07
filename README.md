# 🤖  Document-based Q&A Chatbot
- A versatile chatbot designed for document-based question answering. This bot can respond to user (Support & Sales teams) queries using information extracted from various document formats including PDF, CSV, Excel, and Word files. It is powered by embeddings , LLM model and similarity search for accurate, context-based responses.


##  ✨  Features

- Multi-format support: Supports PDF, Word and Excel files.
- Embedding-based retrieval: Uses embeddings to retrieve contextually relevant answers.
- Locally hosted LLM: Powered by a locally hosted language model (llama3.1) for generating responses, keeping data processing within your system and reducing dependency on external APIs.
- Feedback collection: Allows users to rate responses, aiding improvement.
- Easy-to-use UI: Built with Streamlit for an accessible web interface.


## ⚙️ Installation

- Clone the repository:
```bash
git clone <your-repo-url>
cd <repo-name>
```

- Set up a virtual environment (optional but recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
- Install dependencies: Use the requirements.txt file to install all necessary libraries:
```bash
pip install -r requirements.txt

```
- Install and set up the local LLM model (Llama 3.1):
## 🔗 Links
🌐 [Ollama CLI Download Page](https://ollama.com/download)

- Download the Llama 3.1 model using Ollama:
```bash
ollama pull llama3.1 
```
```bash
ollama run llama3.1:70b 
```
```bash
ollama run llama3.1:405b 
```

### Available Llama 3.1 Model Variants

Ollama offers different variants of the Llama 3.1 model, depending on your system’s memory and performance requirements. Choose the variant that best suits your setup:

| Model Variant | Parameter Size | Disk Space Required | Run Command               |
|---------------|----------------|---------------------|---------------------------|
| **Llama 3.1** | 8B             | 4.7 GB             | `ollama run llama3.1`     |
| **Llama 3.1** | 70B            | 40 GB              | `ollama run llama3.1:70b` |
| **Llama 3.1** | 405B           | 231 GB             | `ollama run llama3.1:405b` |

To run a specific model, use the corresponding command in your terminal.


## Requirements

Make sure you have the following installed:

BackEnd
- Python 3.8+
- Pandas: For handling CSV and Excel data.
- LangChain Modules:
    - langchain_core
    - langchain_ollama
    - langchain_chroma
    - langchain_text_splitters
- Openpyxl: To read and write Excel files.
- Python-docx: For reading .docx Word files.
- LLM Model (Llama 3.1):
    - Ollama CLI: Required to run llama3.1 locally.
    - Llama 3.1 Model: Downloaded via Ollama with:
```bash
ollama pull llama3.1
```

FrontEnd:
- Streamlit: For the web interface.
    

## Code Structure

- chat.py: Defines the chatbot interface.
- dashboard.py: Main UI for Streamlit, including file upload and chat display.
- document_utils.py: Utility functions for document chunking and ID generation.
- embedding_function.py: Embedding model definition.
- excel_format.py: Loads Excel files, splits sheets, and prepares data for embeddings.
- feedback.py: Collects feedback on responses.
- login.py: Basic login component (future enhancements).
- populate_database.py: Processes and stores documents in the Chroma database.
- query_data.py: Handles query processing and retrieves answers from stored data.
- run_dashboard.py: Starts the Streamlit app.
- word_format.py: Loads and processes Word files.



## Usage Instructions
- To launch the chatbot interface, use the following command to start the Streamlit app:
```bash
python run_dashboard.py
```
- This command will start a local server, and you should see a message like this:
```bash
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
Network URL: http://<your-ip>:8501
```
Open a browser and go to http://localhost:8501 to access the chatbot UI.

**Uploading Documents**

The chatbot can process and retrieve information from multiple document formats, including PDF, Word, Excel, and CSV. Here’s how to upload files:

- In the sidebar on the left, look for the "Document Upload" section.
- Click on "Upload data file" and select a file from your computer.
- Supported file types include:
    - PDF (.pdf)
    - Word (.docx)
    - Excel (.xlsx) 
Once uploaded, the documents will be processed and stored for querying.



**Asking Questions**

After uploading documents, you can start interacting with the chatbot:

- Type your question in the input box labeled "Enter your question here" at the bottom of the chat interface.
- Press Enter or click the send icon to submit your question.
- The chatbot will analyze the uploaded documents and respond based on the relevant information it finds.
*Example Questions*

- “Does my electric cable fit the Zpark charger?”
- “how does debiting work?”
- “Summarize the main points from the document about Zpark Duo M.”

**Providing Feedback**

- After receiving a response, you can rate its helpfulness. Here’s how:

    - Expand the Feedback Section: After each response, you’ll see an option to rate the response. Click on the "**Rate this response**" section to expand it.
- Choose a Rating: You can select either:
    - 👍 Thumbs Up if the response was helpful, or
    - 👎 Thumbs Down if the response was not helpful.
- Optional Comment: You can also add any specific comments or suggestions to improve the bot’s responses.
- Submit Feedback: Click "Submit Feedback" to save your rating. Feedback is stored in feedback_log.json and can be used to improve the chatbot’s accuracy.

```bash
        "timestamp": "2024-11-04T11:25:58.772530",
        "query": "does my electic cable fit the zpark charger ?",
        "response": "To answer your question, I need a bit more information. Unfortunately, it's not explicitly mentioned in the provided context what type of electric cables are compatible with the Zpark charger.\n\nHowever, if you're looking for guidance on this specific topic, I recommend checking the Zpark Portal or consulting the user manual for your specific charging station. They should have detailed information on cable compatibility and requirements.",
        "rating": [ "👎 :material/thumb_down:"],
        "comments": "Yes, the power outlet in a Zpark Duo complies with EU standard type 2."
```
