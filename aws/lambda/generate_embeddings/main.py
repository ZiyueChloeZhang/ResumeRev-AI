import os
import json
import boto3
from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.llms.bedrock import Bedrock
from langchain.embeddings import BedrockEmbeddings
from langchain.vectorstores import FAISS

# # Assuming these environment variables are set
# DOCUMENT_TABLE = os.environ["DOCUMENT_TABLE"]
# BUCKET = os.environ["BUCKET"]

s3 = boto3.client("s3")
def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    resume_key = event['Records'][0]['s3']['object']['key']

    print(f"Processing file {resume_key} from bucket {bucket}")

    # Download the file from S3
    s3.download_file(bucket, resume_key)

    # Load the PDF
    loader = PyPDFLoader(resume_key)

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

    faiss_index = index_creator.from_loaders([loader])

    print(f"Faiss_index {faiss_index} ")


    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
        },
        "body": json.dumps(res["answer"]),
    }
