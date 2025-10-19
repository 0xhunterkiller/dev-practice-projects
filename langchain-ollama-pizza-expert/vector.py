"""
This script loads restaurant review data from a CSV file, generates embeddings for each review using the OllamaEmbeddings model, 
and initializes a Chroma vector store for efficient similarity search and retrieval. If the vector store database does not exist, 
it prepares Document objects from the CSV data, including review content and metadata such as rating and date.

Dependencies:
- langchain_ollama
- langchain_chroma
- langchain_core
- pandas
- os

Workflow:
1. Load review data from 'pizza.csv' into a pandas DataFrame.
2. Initialize the OllamaEmbeddings model for embedding generation.
3. Check if the Chroma vector store database exists; if not, prepare documents from the DataFrame.
4. Initialize the Chroma vector store with the specified collection name, persistence directory, and embedding function.
"""

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

# Load the CSV File
df = pd.read_csv("pizza.csv")

# Embedding Model
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

db_location = "./chroma_db"

add_documents = not os.path.exists(db_location)
if add_documents:
    documents = []
    ids = []

    for i, row in df.iterrows():
        document = Document(
            page_content=row["Title"] + " " + row["Review"],
            metadata = {"rating": row["Rating"], "date": row["Date"]},
            id = str(i)
        )
        ids.append(str(i))
        documents.append(document)

vector_store = Chroma(
    collection_name="restaurant_review",
    persist_directory=db_location,
    embedding_function=embeddings
)

if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)