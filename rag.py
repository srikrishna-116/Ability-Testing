# rag.py

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables. Please add it to .env file.")

# Global variables for lazy loading
db = None
llm = None

def _initialize_pdf():
    """Initialize PDF loader and vector database (lazy loading)."""
    global db, llm
    
    if db is not None:
        return  # Already initialized
    
    # Handle PDF path - supports both local and deployed environments
    pdf_paths = [
        Path("Testing Report project.pdf"),
        Path("./Testing Report project.pdf"),
    ]
    
    # Add environment variable path if set
    env_pdf_path = os.getenv("PDF_PATH")
    if env_pdf_path:
        pdf_paths.append(Path(env_pdf_path))
    
    pdf_path = None
    for path in pdf_paths:
        if path.is_file():
            pdf_path = path
            break
    
    if not pdf_path:
        raise FileNotFoundError(
            f"PDF file 'Testing Report project.pdf' not found. "
            f"Checked paths: {[str(p.resolve()) for p in pdf_paths]}. "
            f"Please place the PDF in the project root or set PDF_PATH in .env"
        )
    
    # Load project info PDF
    loader = PyPDFLoader(str(pdf_path))
    documents = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)
    
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    db = Chroma.from_documents(docs, embeddings)
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.1-8b-instant"
    )

# MAIN FUNCTION
def ask_question(query, chat_history=""):
    global db, llm
    
    # Initialize PDF on first call
    if db is None or llm is None:
        _initialize_pdf()
    
    results = db.similarity_search(query, k=3)
    context = "\n".join([doc.page_content for doc in results])

    prompt = f"""
You are an AI assistant for an Adaptive Testing System.

Answer ONLY about this system.
Explain clearly.

Chat History:
{chat_history}

Context:
{context}

Question: {query}
"""

    response = llm.invoke(prompt)
    return response.content