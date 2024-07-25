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

from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

from langchain_core.messages import HumanMessage

#Specification
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


#pinecone
#In this vector store, embeddings and docs are stored within a Pinecone index.
#During query time, the index uses Pinecone to query for the top k most similar nodes.


#from pinecone import Pinecone
#API_KEY = "3a98e064-8b05-4cc1-bc80-38c79bcfc694"
#pinecone = Pinecone(api_key=API_KEY)
#index_name = "trademarks"
#index = pinecone.Index(index_name)

# Module 1
# For extrating the query from the user or website
def query_extractor():
    query = ""
    return query

def query_handler2(query):
    identify_template2 = [
        ("system", 
        """
        Summarise all the descriptions of all the keys of input to be a paragraph.
        If the description of keys is not found or "Nil", output "Nil". 
        """),
        ("human", " INPUT: {input}")
    ]
    identify_prompt2 = ChatPromptTemplate.from_messages(identify_template2)

    #Summary 
    Summary_schema = ResponseSchema(name="Business Summary", description="Summarize all the business descriptions which have generated.")
    #Summary
    response_schemas2 = [Summary_schema] 
    output_parser2 = StructuredOutputParser.from_response_schemas(response_schemas2)
    chain2 = identify_prompt2 | bedrock | StrOutputParser()
    #prompt_result2 = chain2.invoke({"input": prompt_result})
    return chain2.invoke({"input": query})

def query_handler2(query):
    identify_template2 = [
        ("system", 
        """
        Summarise all the descriptions of all the keys of input to be a paragraph.
        If the description of keys is not found or "Nil", output "Nil". 
        """),
        ("human", " INPUT: {input}")
    ]
    identify_prompt2 = ChatPromptTemplate.from_messages(identify_template2)

    #Summary 
    Summary_schema = ResponseSchema(name="Business Summary", description="Summarize all the business descriptions which have generated.")
    #Summary
    response_schemas2 = [Summary_schema] 
    output_parser2 = StructuredOutputParser.from_response_schemas(response_schemas2)
    chain2 = identify_prompt2 | bedrock | StrOutputParser()
    #prompt_result2 = chain2.invoke({"input": prompt_result})
    return chain2.invoke({"input": query})

# Module 2
def query_handler(query):
    #the "conversation" key 
    #Formatting template   
    #identify_template = [("system", "Please generate a business description that capture the input text based on "),  ("User", " Query: {input}")]


        #For each key, if the Chinese component is not found, generate "Nil" instead of translating it from the Non-Chinese component.
        #For each key, if the Non-Chinese component is not found, generate "Nil" instead of translating it from the Chinese component.
    identify_template = [
        ("system", 
        """Please generate business descriptions to nine keys based on the input text.
        Output a dictionary with nine keys: 
        1. "Core product or service"; 
        2. "Target market";
        3. "Business goals";
        4. "Key benefits";
        5. "Unique selling proposition";
        6. "Brand Personality";
        7. "Brand Story";
        8. "Emotional Connection";
        9. "Trademark Name";
        In each key, separate the output into Chinese and Non-Chinese components if any. Each key should have the label "Chinese" and "Non-chinese" to distinguish chinese and non-chinese words.
        Use character-based identification: alphabetic characters (including numbers) indicate Non-Chinese, while non-alphabetic characters indicate Chinese. 
        If the description of key is not found, output "None". 
        Output in json string format.
        """),
        ("human", " INPUT: {input}")
    ]



    identify_prompt= ChatPromptTemplate.from_messages(identify_template)


    #The format of the output
    ####All the schemas

    #Basic information
    ProductService_schema = ResponseSchema(name="Core product or service", description="Identify the primary product or service offered by the business and summarize its nature and purpose. Be concise but informative")
    TargetMarket_schema = ResponseSchema(name="Target market", description="Identify the specific audience or customer segment that the business aims to serve and summarize their characteristics. In short, it is \"Mention who your products/services cater to.\"")
    BusinessGoals_schema = ResponseSchema(name="Business goals", description="Summarize the key objectives or goals that the business aims to achieve in the short or long term. Summarize your business’s purpose and goals.")
    Benefits_schema = ResponseSchema(name ="Key benefits", description = "Highlight the main benefits that customers can expect to receive from using the business's product or service and summarize them. In short, it is \"Describe the advantages customers gain by choosing your business.\"")    
    #Basic information
    
    #Brand information
    Uniquesellingproposition_schema = ResponseSchema(name="Unique selling proposition", description="Determine the key aspects or features that differentiate the business from its competitors and summarize them. In short, it is \"Highlight what sets you apart from competitors\". This could include factors such as quality, reliability, sustainability, innovation or others.")
    BrandPersonality_schema = ResponseSchema(name="Brand Personality", description="Summarize the personality traits that the brand embodies. Is it innovative, trustworthy, playful, sophisticated, or something else?")
    BrandStory_schema = ResponseSchema(name="Brand Story", description="Briefly summarize the narrative or story behind the brand. This could include its origins, mission, or any significant milestones.")
    EmotionalConnection_scheama = ResponseSchema(name="Emotional Connection", description="Describe the emotional connection that the brand aims to establish with its target audience. This could be through creating a sense of belonging, trust, or aspiration.")
    TrademarkName_scheama = ResponseSchema(name="Trademark Name", description="Identify the trademark name of the trademark application.")
    #Brand information


    
    #Combine all the schemas
    response_schemas = [ProductService_schema, TargetMarket_schema, BusinessGoals_schema, Benefits_schema, 
                        Uniquesellingproposition_schema, BrandPersonality_schema, BrandStory_schema, 
                        EmotionalConnection_scheama,TrademarkName_scheama]

    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    #output_parser
    

    ###########Check output format
    format_instruction = output_parser.get_format_instructions()
    #print(format_instruction)
    
    
    #Basic example: prompt + model + output parser
    chain = identify_prompt | bedrock | output_parser

    #print(chain)

    prompt_result = chain.invoke({"input": query}) # For key values
    prompt_result2 = query_handler2(prompt_result) #For summary
    #print(prompt_result)
    
    #print(chain.invoke({"input": query}))
    #return chain.invoke({"input": query})
    return prompt_result, prompt_result2
    #All accessible

    #return chain
    
    
    #message = []
    #return(message)
    #Let json parser = parsed_otuput = output_parser.parse(response.content) 
    #type(parsed_output) = dict
    # parsed_output["neme"]


#Module 3
def output_checker(query):
    count = 0 # the times you check the model response
    for i in range(5):
        count2 = 0 # count how many "Nil" you have found
        #print(count)
        prompt_result, prompt_result2=query_handler(query)
        for idx, item in enumerate(prompt_result):
            #print(f"****The item is {item}.****\n{prompt_result[item]}")
            if prompt_result[item]['Chinese'] == "None" and prompt_result[item]['Non-chinese'] == "None":
                count2 = count2 + 1
                #print(count2)
            if count2 > 7: # more than 7 "Nil" of the properties
                count = count + 1
                break
    if count == 5: # If 5 test cases are all more than 7 "Nil".
        return 
    else:
        return prompt_result, prompt_result2



#if __name__ == "__main__":
def Business_Analysis(query_input):    

    query = """I am seeking a trademark for our innovative software platform that revolutionizes project management and 
            collaboration. Our target market includes small to medium-sized businesses in the technology and creative industries 
            seeking efficient project management solutions. Our primary goal is to become the industry leader in project 
            management software by providing intuitive tools that streamline workflows and boost productivity.
            The key benefits of our software platform are real-time collaboration, task tracking, and seamless communication, 
            allowing teams to work more efficiently, meet deadlines, and deliver high-quality results.
            What sets us apart is our unique selling proposition of offering customizable project templates, advanced analytics, 
            and integrations with popular productivity tools, giving users unparalleled flexibility and insights.
            Our brand personality is characterized by being innovative, reliable, and user-centric. We strive to empower teams and foster a collaborative work culture. 
            Our brand story began with a team of experienced project managers who recognized the need for a 
            comprehensive solution to overcome common project management challenges. 
            Our passion for efficiency and productivity led us to develop our groundbreaking software.
            Through our software platform, we aim to create an emotional
            connection with our customers, providing them with a sense of confidence and control over their
            projects. Our software fosters a feeling of empowerment and promotes seamless teamwork.
            """
    query2 = "hello world"

    query3 = """"我是一家新兴的企业，计划向贵局申请商标注册。特此向贵局提出以下查询，以确保申请的准确性和完整性。

            首先，我公司名为“优美家居设计有限公司”，我们专注于提供高品质的室内设计服务。我希望注册的商标名称是“优美家居设计”。

            商标的设计主要由一个简洁而现代的标志组成，与我们的业务定位相符。我们的商标将与室内设计服务相关联。

            我们的目标受众是追求高品质和独特设计的个人和家庭。我们的竞争优势在于提供个性化的设计方案和卓越的客户服务。

            我们所在的行业是室内设计和装饰，我们的商标将在全国范围内使用。
    
            在商标注册过程中，我们进行了广泛的市场调研，没有发现与我们商标相似的其他商标。

            我们计划在未来拓展国际市场，因此我们希望申请国际商标保护，以确保我们的商标在全球范围内得到保护。

            此前，我们已经开始使用商标，并在多个项目中成功应用。我们希望通过商标注册来巩固我们的品牌地位。

            感谢贵局的耐心阅读，并期待贵局的支持和指导。"""

    query4 = """I am writing to submit a trademark application and would like to raise a few queries to ensure its accuracy and completeness. 我希望向贵局提交商标申请，并提出以下查询。

            My company is called "美好生活有限公司" and we specialize in providing innovative and eco-friendly products for the home. 我的公司名为“美好生活有限公司”，我们专注于为家庭提供创新和环保的产品。

            The trademark I would like to register is "EcoLiving" and it will be associated with our line of eco-friendly home products. 我希望注册的商标名称是“EcoLiving”，它将与我们的环保家居产品系列相关联。

            Our target audience is environmentally conscious consumers who are looking for high-quality and sustainable products for their homes. 我们的目标受众是环保意识强的消费者，他们寻求高品质和可持续的家居产品。

            Our competitive advantage lies in our commitment to using eco-friendly materials and our focus on design and functionality. 我们的竞争优势在于致力于使用环保材料，并注重设计和功能。

            We operate in the home goods industry and plan to use our trademark throughout the country. 我们在家居用品行业运营，并计划在全国范围内使用商标。

            Prior to submitting this application, we conducted a thorough search and did not find any other trademarks that are similar to ours. 在提交申请之前，我们进行了全面的搜索，没有发现与我们商标相似的其他商标。

            We plan to expand internationally in the future and would like to apply for international trademark protection. 我们计划在未来扩大国际市场，并希望申请国际商标保护。

            Thank you for your attention to this matter. Please let me know if you require any additional information. 谢谢贵局的关注，如有需要，请告知我需要提供哪些额外信息。"""
    
    query5 = "LUNG FUNG COSMETIC 龍豐藥粧"

    query6 = """I am writing to submit a trademark application and would like to raise a few queries to ensure its accuracy and completeness. 我希望向贵局提交商标申请，并提出以下查询。

            we specialize in providing innovative and eco-friendly products for the home. 我们专注于为家庭提供创新和环保的产品。

            it will be associated with our line of eco-friendly home products. 它将与我们的环保家居产品系列相关联。

            Our target audience is environmentally conscious consumers who are looking for high-quality and sustainable products for their homes. 我们的目标受众是环保意识强的消费者，他们寻求高品质和可持续的家居产品。

            Our competitive advantage lies in our commitment to using eco-friendly materials and our focus on design and functionality. 我们的竞争优势在于致力于使用环保材料，并注重设计和功能。

            We operate in the home goods industry and plan to use our trademark throughout the country. 我们在家居用品行业运营，并计划在全国范围内使用商标。

            Prior to submitting this application, we conducted a thorough search and did not find any other trademarks that are similar to ours. 在提交申请之前，我们进行了全面的搜索，没有发现与我们商标相似的其他商标。

            We plan to expand internationally in the future and would like to apply for international trademark protection. 我们计划在未来扩大国际市场，并希望申请国际商标保护。

            Thank you for your attention to this matter. Please let me know if you require any additional information. 谢谢贵局的关注，如有需要，请告知我需要提供哪些额外信息。"""


    count = 0
    #prompt_result, prompt_result2=query_handler(query4)
    while(1):
        try:
            prompt_result, prompt_result2 = output_checker(query_input)
            #if prompt_result["Trademark Name"]['Chinese'] == "Nil" and prompt_result["Trademark Name"]['Non-chinese'] == "Nil":
            #    print("Please provide the trademark name.")
            #    continue
            #print(prompt_result)
            #print(prompt_result2)
            break
        except:
            print("Please provide more information.")


            
            #When the output is "Nil" (non-return type)
            #print("Please provide more information.")
            count = count + 1
            if count == 5:
                prompt_result = "error"
                prompt_result2 = "error"
                break
    return prompt_result, prompt_result2
    #print(prompt_result)
    #print(prompt_result["Core product or service"])
    #print(len(prompt_result))