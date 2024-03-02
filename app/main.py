import streamlit as st

st.title('ResumeRev')
st.subheader('The :blue[AI]-Powered Career Architect')


col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader('Job Posting', divider=True)
    txt = st.text_area(
        "Copy and paste a job posting here",
        "",
        )

    st.write(f'You wrote {len(txt)} characters.')

    st.subheader('Resume', divider=True)
    uploaded_files = st.file_uploader("Choose a PDF file", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        st.write("filename:", uploaded_file.name)
        st.write(bytes_data)

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

