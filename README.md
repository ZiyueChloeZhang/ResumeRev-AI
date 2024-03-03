# ResumeRev-AI
UBC CIC genAI Hackathon 2024

This sample application allows you to ask natural language questions of the resume PDF document you upload. It combines the text generation and analysis capabilities of an LLM with a vector search of the document content. The solution uses serverless services [Amazon Bedrock](https://aws.amazon.com/bedrock/) to access foundational models, and [Streamlit UI](https://streamlit.io/)

<p float="left">
  <img width="831" alt="Screen_Shot_2024-03-02_at_5 26 21_PM" src="https://github.com/ZiyueChloeZhang/ResumeRev-AI/assets/41217816/312ac4e0-45b9-4295-840e-a277be27cd9b">
</p>

> **Note**
> This architecture creates resources that have costs associated with them. Please see the [AWS Pricing](https://aws.amazon.com/pricing/) page for details and make sure to understand the costs before deploying this stack.

## Key features

- [Amazon Bedrock](https://aws.amazon.com/de/bedrock/) for serverless embedding and inference
- [LangChain](https://github.com/hwchase17/langchain) to orchestrate a Q&A LLM chain
- [FAISS](https://github.com/facebookresearch/faiss) vector store
- Frontend built in [Streamlit](https://streamlit.io/)

## How the application works

Serverless Resume PDF Suggestion architecture 
<img width="831" alt="Screen_Shot_2024-03-02_at_5 26 21_PM" src="https://github.com/ZiyueChloeZhang/ResumeRev-AI/assets/92232261/1d95867a-dba3-40af-86ab-0ce0f3398abe">

1. A user uploads a Resume PDF document into the platform
1. This upload performs a metadata extraction and document embedding process. The process converts the text in the document into vectors. The vectors are loaded into a vector index.
1. When a user chats with a Rseume PDF document and sends a prompt to the backend, a function retrieves the index and searches for information related to the prompt.
1. A LLM then uses the results of this vector search, previous messages in the conversation, and its general-purpose capabilities to formulate a response to the user.

## Deployment instructions

### Prerequisites

- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- [Python](https://www.python.org/) 3.11 or greater
