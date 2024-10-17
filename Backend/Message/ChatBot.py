
from langchain_core.prompts import MessagesPlaceholder

from langchain_community.chat_models import BedrockChat


import logging
from botocore.exceptions import NoCredentialsError
from langchain_aws import ChatBedrock
import boto3, os

from langchain.chains.llm import LLMChain
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser


from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Bedrock

import json

from langchain.chains.summarize import load_summarize_chain
from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain
#from langchain_text_splitters import CharacterTextSplitter # type: ignore

from langchain.chains.combine_documents.stuff import StuffDocumentsChain
#from langchain_text_splitters import CharacterTextSplitter # type: ignore

from langchain_community.llms import Bedrock



from langchain_core.messages import HumanMessage

#Specification
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

# Access credentials safely
aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_DEFAULT_REGION')

session = boto3.Session(profile_name='poctester1')
bedrock_runtime = boto3.client(
    service_name="bedrock",
    region_name="us-east-1",
)


model_id = "anthropic.claude-3-haiku-20240307-v1:0"
model_kwargs =  {
    "temperature": 0.1,
}
#Specification
session = boto3.Session()
bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
)

# model_id = "amazon.titan-text-express-v1"
model_id = "anthropic.claude-3-haiku-20240307-v1:0"

model_kwargs =  {
    "temperature": 0.1,
    #"top_p": 1.0,
    #"top_k": 40,
    #"num_beams":4,
    #"max_new_tokens":128,
}

bedrock = BedrockChat(
    client=bedrock_runtime,
    model_id=model_id,
    model_kwargs=model_kwargs,
)


def ChatBot(question,history):
    

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant."),
            MessagesPlaceholder("history"),
            ("human", "{question}")
        ]
    )
    #prompt.invoke(
    #{
    #    "history": [("human", "what's 5 + 2"), ("ai", "5 + 2 is 7")],
    #    "question": "now multiply that by 4"
    #}
    #)
    #identify_template2 = [
    #    ("system", 
    #    """
    #    Summarise all the descriptions of all the keys of input to be a paragraph.
    #    If the description of keys is not found or "Nil", output "Nil". 
    #    """),
    #    ("human", " INPUT: {input}")
    #]
    history_speaker = "ai"
    history_message = "hi, who i am."
    history_session1 = (history_speaker, history_message)

    history_speaker = "human"
    history_message = "hi, who you are."
    history_session2 = (history_speaker, history_message)
    
    data_session = [history_session1,history_session2]

    print(data_session)
    #print(history_session)
    #identify_prompt2 = ChatPromptTemplate.from_messages(identify_template2)
    data = [
    ("human", "what's 5 + 2 and let it is a variable 'a'."),
    ("ai", "5 + 2 is 7 and 'a' is 7."),
    ("human", "what's 9 + 11 and let it is a variable 'b'"),
    ("ai", "9 + 11 is 20 and 'b' is 20.")
    ]
    question = question
    #Summary 
    #Summary_schema = ResponseSchema(name="Business Summary", description="Summarize all the business descriptions which have generated.")
    #Summary
    #response_schemas2 = [Summary_schema]
    #output_parser2 = StructuredOutputParser.from_response_schemas(response_schemas2)
    chain2 = prompt | bedrock | StrOutputParser()
    #prompt_result2 = chain2.invoke({"input": prompt_result})
    return chain2.invoke({
        "history": history,
        "question": question
    })




