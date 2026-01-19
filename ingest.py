import os
import chromadb
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils import get_directories

# Configuration
CHROMA_PATH = "chroma_db"

def load_documents():
    """
    Load documents from the specified directories.
    """
    documents = []
    base_dirs = get_directories()
    
    for dir_name in base_dirs:
        path = os.path.join(os.getcwd(), dir_name)
        if not os.path.exists(path):
            print(f"Warning: Directory {path} does not exist.")
            continue
            
        print(f"Loading from {dir_name}...")
        # Start with a generic loader, can be specialized for PDF/Txt
        # Using DirectoryLoader with TextLoader for simplicity for now, or default
        # Assuming mixed content, let's try to handle common formats
        loader = DirectoryLoader(path, glob="**/*.txt", loader_cls=TextLoader)
        docs = loader.load()
        for doc in docs:
            doc.metadata["folder_name"] = dir_name
            doc.metadata["source_file"] = os.path.basename(doc.metadata.get("source", ""))
            documents.extend([doc])
            
        # Add PDF support if needed, assuming simple text for now based on description implies standard text mostly
        # But "Industry Reports" likely PDF. 
        loader_pdf = DirectoryLoader(path, glob="**/*.pdf", loader_cls=PyPDFLoader)
        try:
            pdf_docs = loader_pdf.load()
            for doc in pdf_docs:
                doc.metadata["folder_name"] = dir_name
                doc.metadata["source_file"] = os.path.basename(doc.metadata.get("source", ""))
            documents.extend(pdf_docs)
        except Exception as e:
            print(f"Error loading PDFs from {dir_name}: {e}")

    return documents

def split_documents(documents):
    """
    Split documents into chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

def add_to_chroma(chunks):
    """
    Add chunks to ChromaDB.
    """
    # Using a standard open embedding model suitable for local/cpu usage if needed, 
    # or we can use target specific ones. "all-MiniLM-L6-v2" is a safe bet.
    embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Initialize Chroma
    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_function
    )
    
    # Add chunks
    # Chroma handles IDs automatically if not provided, but we can prevent dupes if we want.
    # For this simple upskiller, we'll just add.
    
    print(f"Adding {len(chunks)} chunks to ChromaDB...")
    db.add_documents(chunks)
    print("Data ingestion complete.")

def main():
    documents = load_documents()
    if not documents:
        print("No documents found.")
        return
        
    chunks = split_documents(documents)
    add_to_chroma(chunks)

if __name__ == "__main__":
    main()
