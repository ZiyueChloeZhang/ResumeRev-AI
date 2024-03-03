import os

import streamlit as st
import boto3
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.llms.bedrock import Bedrock
from langchain.embeddings import BedrockEmbeddings
from langchain.vectorstores import FAISS
import tempfile

query = """You will serve as an AI career coach, aiming to provide 
insightful responses to the questions asked. Your objective 
is to deliver helpful answers in character of AI career coach, 
assisting users with their inquiries and refining their resume 
details.

You should maintain a friendly customer service tone.

The resume information that users uploaded is listed between 
the <data> XML like tags. You should reference when answering 
the users questions {{user_input}}


Here are some important rules for the interaction:

Always stay in character, as AI career coach.
If you are unsure how to repond, say 'Sorry, I didn't understand that. 
Could you ask the question with more detailed information?''
If someone asks something irrelevant, say,  'Sorry, I only give resume 
related advice. Do you have a career question today I can help you with?'
Ensure responses are within 50 words by default. If users desire more 
information, increase the word count by 50 words with each request."""

st.title('ResumeRev')
st.subheader('The :blue[AI]-Powered Career Architect')

col1, col2 = st.columns(2, gap="large")
def initialize_chain(path_to_resume):
    if "chain" in st.session_state:
        del st.session_state["chain"]

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

    index_from_loader = index_creator.from_loaders([loader])
    index_from_loader.vectorstore.save_local("/tmp")
    faiss_index = FAISS.load_local("/tmp", embeddings)

    retriever = faiss_index.as_retriever()
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever
    )

    chain({
        "question": query,
        "chat_history": []
    })

    st.session_state['chain'] = chain

with col1:
    st.subheader('Resume', divider=True)
    resume = st.file_uploader("Choose a PDF file", type=['pdf'])
    if resume is not None:
        st.success(resume.name + ' Selected')
        if st.button('Submit', type="primary"):
            temp_dir = tempfile.mkdtemp()
            path = os.path.join(temp_dir, resume.name)
            with open(path, "wb") as f:
                f.write(resume.getvalue())
            initialize_chain(path)

with col2:
    st.subheader("AI Consultant", divider=True)

    # Initialize messages list in session state if not present
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Accept new user input and process it
    if 'chain' in st.session_state:
        prompt = st.chat_input("Ask me something about the resume")
        if prompt is not None:
            # Append user question to messages
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Display user question
            # with st.chat_message("user"):
            #     st.markdown(prompt)

            # Generate AI response using 'chain'
            result = st.session_state['chain']({
                "question": prompt,
                "chat_history": st.session_state.chat_history
            })
            ai_response = result["answer"]

            # Display AI response and append it to messages
            # with st.chat_message("assistant"):
            #     st.markdown(ai_response)

            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            st.session_state.chat_history.append((prompt, ai_response))
    else:
        st.write("Please upload a resume to start the consultation.")

    with st.container(height=400):
        # Display existing chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

