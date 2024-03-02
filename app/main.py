import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError
import uuid

st.title('ResumeRev')
st.subheader('The :blue[AI]-Powered Career Architect')

col1, col2 = st.columns(2, gap="large")


def upload_job_posting_and_resume_to_s3(job_posting, resume):
    # Initialize a boto3 client
    s3 = boto3.client('s3')
    bucket_name = 'resume-team-2'

    # Define the S3 key names for the job posting and resume
    session_id = str(uuid.uuid4())

    job_posting_key = f'{session_id}/job_posting.txt'
    resume_key = f'{session_id}/{resume.name}'

    try:
        # Upload the job posting
        # Convert the job posting string to bytes and upload it as a text file
        s3.put_object(Body=job_posting.encode(), Bucket=bucket_name, Key=job_posting_key)

        # Upload the resume
        # Use the 'UploadedFile' object's 'getbuffer()' method to read the file content
        s3.upload_fileobj(resume, bucket_name, resume_key)

        print(f"Job posting and resume uploaded successfully to bucket '{bucket_name}'")
    except NoCredentialsError:
        print("Error: AWS credentials not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


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
                upload_job_posting_and_resume_to_s3(job_posting, resume)


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