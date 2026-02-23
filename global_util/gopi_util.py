import os, re, json, dotenv
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import time

# Load Keys from .env file in global_util directory
env_path = os.path.join(os.path.dirname(__file__), '.env')
#print(f"Loading .env from: {env_path}")
dotenv.load_dotenv(env_path)

api_key = os.getenv("GOPI_OPENAI_API_KEY")
#print(f"API Key loaded: {api_key[:10] if api_key else 'None'}")
model_name = "gpt-3.5-turbo"

# Creates an LLM object and returns it
def get_llm():
    llm = ChatOpenAI(temperature=0.3, model_name=model_name, openai_api_key=api_key)
    return llm

# Creates an embedding object and returns it
def get_embedding():
    embedding = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=api_key)
    return embedding

# Creates a response from the LLM and returns it
def get_llm_response(prompt):
    messages = [{"role": "user", "content": prompt}]
    response = get_llm().invoke(messages)
    return response.content

# Creates a response from the LLM and returns it with retry
def get_llm_response_with_retry(prompt, max_retries=3):
    for i in range(max_retries):
        try:
            return get_llm_response(prompt)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)
    return None

# Creates or loads Chroma DB for documents
def create_or_load_chroma_db(docs, db_name="chroma_db", collection_name="default_collection"):
    """
    Creates a new Chroma DB or loads existing one from EdurekaExercises folder
    
    Args:
        docs: List of documents to store (for new DB creation)
        db_name: Name of the database directory
        collection_name: Name of the collection within the database
    
    Returns:
        Chroma vector store object
    """
    # Create Chroma DB in Edureka Exercises folder
    persist_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), db_name)
    
    # Check if Chroma DB already exists
    if os.path.exists(persist_dir):
        print(f"Loading existing Chroma DB from: {persist_dir}")
        vector_store = Chroma(
            persist_directory=persist_dir,
            embedding_function=get_embedding(),
            collection_name=collection_name
        )
    else:
        print(f"Creating new Chroma DB at: {persist_dir}")
        vector_store = Chroma.from_documents(
            docs, 
            embedding=get_embedding(), 
            collection_name=collection_name,
            persist_directory=persist_dir
        )
    
    return vector_store

from price_parser import Price
import re
# Extracts a numerical amount from a string using the price-parser library.
def extract_amount_from_text(input_string):
    """
    Extracts a numerical amount from a string using the price-parser library.
    Returns the amount as a Decimal or float.
    """
    price = Price.fromstring(input_string)
    if price.amount is not None:
        # Convert Decimal to float for simplicity if desired, 
        # otherwise use price.amount as a Decimal object
        return float(price.amount) 
    else:
        return None
