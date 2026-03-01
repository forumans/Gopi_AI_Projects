'''
RAG Demo with hardcoded data inside the program itself as Document objects
Used FAISS vector store from Meta to store those documents
Used OPEN AI LLM and Embeddings for Similarity Search
'''

import os, sys
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS #Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from global_util.gopi_util import get_llm, get_embedding

'''
This RAG demo is to show how to use LangChain to create a RAG system

Steps:
1. Load environment variables
2. Create OpenAI LLM
3. Create OpenAI embeddings
4. Create sample documents
5. Create FAISS vector store from sample documents
6. Create RAG chain
7. Answer user questions
'''

llm = get_llm()

# Create OpenAI embeddings - Embeddings are used to convert text to vectors for semantic search
def create_openai_embeddings_model():
    #embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=my_openai_api_key)
    embeddings = get_embedding()
    return embeddings


# Create sample documents to load in to FAISS vector store
def create_sample_documents():
    documents = [
        Document(page_content="Python is a high-level programming language.", metadata={"topic": "programming"}),
        Document(page_content="Machine learning is a subset of artificial intelligence.", metadata={"topic": "ml"}),
        Document(page_content="Deep learning uses neural networks with multiple layers.", metadata={"topic": "ai"}),
    ]

    return documents


# Create FAISS vector store
def create_vector_store():
 
    documents = create_sample_documents()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=10) # because our documents are small defined as strings
    splits = text_splitter.split_documents(documents)

    #print(f"Splits: {len(splits)}" + "\n") # print number of splits

    # Create vector store
    vector_store = FAISS.from_documents(splits, create_openai_embeddings_model()) # invoke local function to create openai embeddings model
    retriever = vector_store.as_retriever(search_kwargs={"k": 5}) # retrieve top 5 documents only
    print("Vector store created successfully!")

    return retriever


# RAG chain function to answer the user questions
def rag_chain(retriever, llm, user_query):
    prompt_template = """
    Answer the question based only on the following context:

    Context:
    {context}

    Question: {question}

    Answer:
    """

    prompt = ChatPromptTemplate.from_template(prompt_template)

    # Implicit function to retrieve only the "page_content" part from each document 
    # Retriever returns 5 relevant Document objects (search_kwargs={"k": 5}) and sends it to this function  
    # This function extracts only the page_content from each Document (ignoring metadata)
    # Joins the "page_content" parts into a single string with 2 new lines between them
    def extract_only_page_content_part_from_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs) 

    rag_chain = ( 
        {"context": retriever | extract_only_page_content_part_from_docs, "question": RunnablePassthrough()} 
        | prompt
        | llm
        | StrOutputParser()
    )

    result = rag_chain.invoke(user_query)
    print(result)



# Menu function to interact with the user
def show_menu():
    retriever = create_vector_store() # Create a FAISS vector store one time
    
    while True:
        print("\n================================================")    
        print("1. Ask a question")
        print("2. Exit")
        choice = input("Choose an option (1-2): ")
        
        if choice == "1":
            user_query = input("Enter your question about AI, DL, ML, or Python: ")
            rag_chain(retriever, llm, user_query) # invoke the RAG chain
        elif choice == "2":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please choose a number from 1 to 2.")




if __name__ == "__main__":
    show_menu()

    
    
