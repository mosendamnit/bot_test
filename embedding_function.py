from langchain_community.embeddings.ollama import OllamaEmbeddings


def embedding_function():
    embedding = OllamaEmbeddings(model="nomic-embed-text")

    return embedding