# ===============Create functions required to process resumes=================

import os, sys
import dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Loaders & Splitters
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Vector store
from langchain_chroma import Chroma

# Add project root to Python path to find global_util
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from global_util.gopi_util import get_llm, get_embedding


# Models
# Embeddings: OpenAI Text Embedding
#openai_embedding = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=api_key)
openai_embedding = get_embedding()

# LLM
#llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=api_key, temperature=0.3)
#llm = ChatOpenAI(temperature=0.3, model="gpt-4o-mini", openai_api_key=api_key)
llm = get_llm()


# Functions
# Load resumes in different formats
def load_resumes(file_paths):
    documents = []
    for file_path in file_paths:
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith('.docx'):
            loader = Docx2txtLoader(file_path)
        elif file_path.endswith('.txt'):
            loader = TextLoader(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")
        
        # Loader.load() function parses PDF/DOCX/Text files by extracting text content and metadata on a page-by-page basis. 
        # It then converts each page into a distinct Document object containing the text content and metadata (like page numbers and file names), 
        # Making it ideal for RAG systems requiring precise citations. 
        documents.extend(loader.load())

    return documents


# Extract candidate details from resume
def extract_candidate_details(docs):
    """Extract name, email, location from resume text"""
    full_text = ""
    for doc in docs:
        full_text += doc.page_content + "\n\n"
    
    # Simple regex patterns for extraction
    import re
    
    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, full_text)
    
    # Phone pattern (basic)
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    phones = re.findall(phone_pattern, full_text)
    
    # Location pattern (basic - look for city, state, country)
    location_keywords = ['located in', 'based in', 'lives in', 'address:', 'location:']
    locations = []
    for keyword in location_keywords:
        pattern = f'{keyword}([^.\n]+)'
        matches = re.findall(pattern, full_text, re.IGNORECASE)
        locations.extend(matches)
    
    # Name extraction - look for common patterns
    # This is a simplified approach - you might want to use NLP libraries for better accuracy
    name_pattern = r'^([A-Z][a-z]+\s+[A-Z][a-z]+)'
    names = []
    lines = full_text.split('\n')
    for line in lines[:10]:  # Check first 10 lines for name
        match = re.match(name_pattern, line.strip())
        if match:
            names.append(match.group(1))
    
    return {
        'name': names[0] if names else 'Unknown',
        'email': emails[0] if emails else 'Unknown',
        'phone': phones[0] if phones else 'Unknown',
        'location': locations[0] if locations else 'Unknown',
        'emails': emails,
        'phones': phones,
        'locations': locations
    }


# Analyze the resume using Gemini
def analyze_resume(docs, job_desc):
    # Combine all resume content for single analysis
    full_resume_text = ""
    for doc in docs:
        full_resume_text += doc.page_content + "\n\n"
    
    prompt = f"""
    Compare the resume with the job description and provide the following information:
    1. Match percentage
    2. Skills match
    3. Experience match
    4. Education match
    5. Strengths & Weaknesses
    6. Overall assessment
    
    Job Description:
    {job_desc}
    
    Resume:
    {full_resume_text}
    """
    response = llm.invoke(prompt)

    # Check if the response has a content attribute (common in LangChain)
    if hasattr(response, 'content'):
        content = response.content if isinstance(response.content, str) else str(response.content)
    else:
        content = str(response)

    return content


# Store text chunks into ChromaDB (embeddings now use OpenAI)
def store_in_chromadb(docs, persist_directory="chroma_db"):
    # Extract candidate details
    candidate_details = extract_candidate_details(docs)
    
    # Split documents into chunks for storage
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    
    texts = [chunk.page_content for chunk in chunks]
    
    # Create metadata with candidate details for each chunk
    metadatas = []
    for i, chunk in enumerate(chunks):
        metadata = {
            "source": f"resume_chunk_{i}",
            "name": candidate_details['name'],
            "email": candidate_details['email'],
            "phone": candidate_details['phone'],
            "location": candidate_details['location'],
            "chunk_index": i,
            "total_chunks": len(chunks)
        }
        metadatas.append(metadata)

    chromadb = Chroma.from_texts(texts=texts, embedding=openai_embedding, metadatas=metadatas, persist_directory=persist_directory)
    # Note: persist() is deprecated in Chroma 0.4+, docs are automatically persisted
    return chromadb, candidate_details


# Use basic similarity search to fetch relevant chunks
def run_self_query(query, persist_directory="chroma_db"):
    vectorstore = Chroma(persist_directory=persist_directory, embedding_function=openai_embedding)
    
    # Use similarity search instead of SelfQueryRetriever
    results = vectorstore.similarity_search(query, k=5)
    
    return results