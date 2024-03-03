import os

import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError
import uuid

from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.llms.bedrock import Bedrock
from langchain.embeddings import BedrockEmbeddings
from langchain.vectorstores import FAISS
import tempfile

st.title('ResumeRev')
st.subheader('The :blue[AI]-Powered Career Architect')

col1, col2 = st.columns(2, gap="large")


def embed_and_response(path_to_resume):
    print('ho')
    # Load the PDF
    loader = PyPDFLoader(path_to_resume)

    # Initialize Bedrock client
    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime",
        region_name="us-west-2",
    )

    embeddings, llm = BedrockEmbeddings(
        model_id="amazon.titan-embed-text-v1",
        client=bedrock_runtime,
        region_name="us-west-2",
    ), Bedrock(
        model_id="anthropic.claude-v2", client=bedrock_runtime, region_name="us-west-2"
    )

    # Create index from the PDF
    index_creator = VectorstoreIndexCreator(
        vectorstore_cls=FAISS,
        embedding=embeddings,
    )

    current_dir = os.getcwd()
    print(current_dir)

    index_from_loader = index_creator.from_loaders([loader])
    index_from_loader.vectorstore.save_local("/tmp")

    faiss_index = FAISS.load_local("/tmp", embeddings)

    print(f"Faiss_index {faiss_index} ")

    retriever = faiss_index.as_retriever()

    chat_history = []
    query = "This is my resume. Give me some advice."

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever
    )

    result = chain({"question": query, "chat_history": chat_history})
    chat_history.append((query, result["answer"]))

    print(chat_history)

with col1:
    st.subheader('Job Posting', divider=True)
    job_posting = st.text_area(
        "Copy and paste a job posting here",
        "",
        )

    st.subheader('Resume', divider=True)
    resume = st.file_uploader("Choose a PDF file", type=['pdf'])
    if resume is not None:
        st.success(resume.name + ' Selected')
        if st.button('Start Tailoring', type="primary"):
            with st.spinner('Uploading...'):
                print('helllooooo')
                temp_dir = tempfile.mkdtemp()
                path = os.path.join(temp_dir, resume.name)
                with open(path, "wb") as f:
                    f.write(resume.getvalue())
                print(path)
                embed_and_response(path)



with col2:
    st.subheader('Your tailored Resume', divider=True)
    # with open("flower.png", "rb") as file:
    #     btn = st.download_button(
    #         label="Download image",
    #         data=file,
    #         file_name="flower.png",
    #         mime="image/png"
    #     )
    text_contents = '''This is some text'''
    st.download_button('Download Resume', text_contents)

    # Chatbot
    st.subheader("AI Consultant", divider=True)
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})