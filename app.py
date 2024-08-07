# importing the  library

import streamlit as st 
from src.helper import get_pdf_text, get_text_chunks, get_vector_store, get_conversational_chain


def user_input(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chatHistory = response["chat_history"]
    for i , message in enumerate(st.session_state.chatHistory):
        if i%2 == 0:
            st.write("User : " , message.content)
        else:
            st.write("reply: ", message.content)

# This is  the main entry point for the Application
def main():
    st.set_page_config("Information Retreival")
    st.header("Information-Retreival-System")
    
    user_question = st.text_input("Ask a question from the PDF Files")
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chatHistory" not in st.session_state:
        st.session_state.chatHistory =  None
    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the submit & Process Button", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing...."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                vector_store = get_vector_store(text_chunks)
                st.session_state.conversation = get_conversational_chain(vector_store)
                st.success('Done')


if __name__ == "__main__":
    main()