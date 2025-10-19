from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.tools import tool
from langchain_community.document_loaders import DirectoryLoader
import os

# Embedding Model - uses local Ollama Model
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

DATA_DIRECTORY = "./five-rings"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
LENGTH_FUNCTION = len

db_location = "./chromadb" 

# Verify that the data directory exists
if not os.path.exists(DATA_DIRECTORY):
    print(f"{DATA_DIRECTORY} path does not exist")
    exit()

if not os.path.exists(db_location):
    # Load the documents from the data directory
    try:
        loader = DirectoryLoader(
            DATA_DIRECTORY, 
            glob="**/*.md", 
            use_multithreading=True,
            
        )
        docs = loader.load()
        print(f"Found {len(docs)} Markdown Documents", end="\n\n")
        
        # Split the text in the directory using recursive text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            separators=[
                "\n\n",
                "\n",
                " ",
                ".",
                ",",
                "\u200b",
                "\uff0c",
                "\u3001",
                "\uff0e",
                "\u3002",
                "",
            ], # This helps to make sure that we dont have any half-words or things like that
            chunk_size = CHUNK_SIZE,
            chunk_overlap = CHUNK_OVERLAP,
            length_function = LENGTH_FUNCTION
        )


        documents_split = text_splitter.split_documents(docs)
    except Exception as e:
        print(f"error laoding documents {e}")
        raise

    try:
        vector_store = Chroma.from_documents(
            documents=documents_split,
            embedding=embeddings,
            persist_directory=db_location,
            collection_name="five_rings"
        )
    except Exception as e:
        print(f"error creating chroma db {e}")
        raise
else:
    try:
        vector_store = Chroma(
            embedding_function=embeddings,
            persist_directory=db_location,
            collection_name="five_rings"
        )
    except Exception as e:
        print(f"error while loading chroma db {e}")
        raise 

retriever = vector_store.as_retriever(
    search_type = "similarity",
    search_kwargs = {"k": 5} # K is the amount of chunks to return
)

@tool
def retriever_tool(query: str) -> str:
    """
    This tool searches and returns the information from the five-rings directory,
    which contains information about the life and 5 rings of Miyamoto Musashi.
    """
    docs = retriever.invoke(query)
    if not docs:
        return "I found no relevant information in the five rings directory"
    
    results = []
    for i, doc in enumerate(docs):
        results.append(f"Document {i+1}:\n {doc.page_content}")
    return "\n\n".join(results)

if __name__ == "__main__":
    query  = input("What is your query about the 5 rings? ")
    while True:
        if query.strip().lower() == "q":
            print("Goodbye.")
            break
        response = retriever_tool.invoke(query)    
        print("Results: ")
        print(query)
        print("=="*20)
        print(response)
        print("===="*20, end="\n\n")
        query  = input("What is your query about the 5 rings? ")