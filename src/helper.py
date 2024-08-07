# Importing the necessary libraries

import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import GooglePalmEmbeddings
from langchain_google_genai import GoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain 
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv


# Loading the environment variables

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY

# This helper function extracts the text from the pdf document
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# This helper function splits th etext extracted from the pdf document into chunks
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    chunks = text_splitter.split_text(text)
    return chunks

# This helper function creates the vector store by performing the embedding over the text chunks
def get_vector_store(text_chunks):
    embeddings = GooglePalmEmbeddings()
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    return vector_store


# This helper function gets the final conversational chain for Q&A pipeline
def get_conversational_chain(vector_store):
    llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=GOOGLE_API_KEY, temperature=0.1)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=vector_store.as_retriever(), memory=memory)
    return conversation_chain