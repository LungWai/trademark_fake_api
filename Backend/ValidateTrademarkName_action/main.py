
from fastapi.responses import FileResponse

from typing import Union

from fastapi import FastAPI, Path
from typing import Optional
from langchain_core.prompts import MessagesPlaceholder
"""
def test():
    app = FastAPI() # create fastapi object, attributes

    #Amazon Simple Storage Service (Amazon S3) 
    #is an object storage service that offers industry-leading scalability, data availability, security, and performance.
    # You can use Amazon S3 to store and retrieve any amount of data at any time, from anywhere. 




    #Create end point, end of a communication channel

    #***DynamoDB
    #Once you enable DynamoDB Streams for your database,
    #it keeps records of changes such as puts, updates & deletes.
    #Whenever an item is modified in the table,
    #a new record has appeared in the DynamoDB Stream.
    #AWS Lambda polls the stream and executes your function which can be used for custom requirements.

    #***hanlder
    #Similarly, Netflix also uses AWS Lambda to update its offshore databases whenever new files are uploaded. This way, all their databases are kept updated.




    #amazon.com/delete-user # endpoint = delete-user 
    #GET - GET AN INFORMATION - GET OR RETURN DATA OR INFORMATION THAT ALREADY EXIST
    #POST - CREATE SOMETHING NEW OR ADD SOMETHING
    #PUT - UPDATE
    #DELETE - DELETE SOMETHING
    # ***URL/docs: check html response 
    # Server = back to a page
    # google.com/get-student = the basic URL to get a student
    # google.com/get-student/1 = get the specific object
    #get, lt, ge(greater than)

    #***Query part***
    # A query is used to pass a value into a URL
    # google.com/results?search=Python
    # results = variable name, query variable = search = Python, search = key


    #In our case, 127.0....../get-student/1
    students = {
        1: {
            "name": "john",
            "age": 17,
            "class": "year 12"
        }
    }


    #***Path parameter
    @app.get("/") #OUR OWN HOMEPAGE
    def index():
        return {"name": "First Data"}

    @app.get("/get-student/{student_id}") # (Dynamic)Variable: student_id
    def get_student(student_id: int = Path(description = "The ID of the student you want to view", gt=0, lt=3)): # If the person doesn't input anything, is just
        # going to leave it blank = an empty data.
        return students[student_id] #students[1], students[2]......

    #***Query parameter
    #get the stuudent data by the name
    # e.g. app.get("\get-by-name?name=jonh")
    @app.get("/get-by-name") 
    def get_student(name : Optional[str] = None):#, test : int):
        for student_id in students:
            if students[student_id]["name"] == name:
                return students[student_id]
            return {"Data": "Not found"}

    #@app.get("/items/{item_id}")
    #def read_item(item_id: int, q: Union[str, None] = None):
    #    return {"item_id": item_id, "q": q}

    import uvicorn



    #Define an entry point
    if __name__ == "__main__":
        uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)


    #
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware

    app = FastAPI()

    #Firewall rules
    origins = [
        "http://localhost.tiangolo.com",
        "https://localhost.tiangolo.com",
        "http://localhost",
        "http://localhost:8080",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
"""
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

# Access credentials safely
aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_DEFAULT_REGION')


from langchain_core.messages import HumanMessage


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

response_enabled = "False"
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
def HistoryExample(question,history):
    

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
def start_point(query_input):    

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



#########################
from typing import Union, List, Any, Literal
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.middleware.cors import CORSMiddleware
######## query model ##########


"""
New added ActionMessageResult
"""
#class Progress(BaseModel):
#  progress: str
#  content: str


#class ProgressMessageRequest(BaseModel):
#    actions: List[Progress]

#class GenerateProgress(ProgressMessageRequest):
#    type: Literal["GenerateProgress"] #specify that the value of the attribute `type` can only be the string `"GenerateProgress"`
#    content: str

#class Block1Content(BaseModel):
#    response = ""


"""
New added ActionMessageResult
"""

class Action(BaseModel):
  type: str
  content: str

class ActionMessageRequest(BaseModel):
    actions: List[Action]



class GenerateSpecification(ActionMessageRequest):
    type: Literal["GenerateSpecification"]
    content: str


class TrademarkNameValidationRequest(BaseModel):
   name: str
   classes: List[int]


class ValidateTrademarkName(ActionMessageRequest):
    type: Literal["ValidateTrademarkName"]
    content: List[TrademarkNameValidationRequest]


class BusinessNatureAnalysis(ActionMessageRequest):
    type: Literal["BusinessNatureAnalysis"]
    content: str

class Message(BaseModel):
    speaker: str
    message: str
    created_at: int
    id: str
    suggestion: List[str] = []

class ActionAndMessageRequest(BaseModel):
    actions: List[Action]
    messages: List[Message]

class MessageRequest(BaseModel):
    messages: List[Message]

#*****************************************
class Specification_block(BaseModel):
    class_index: int
    specification: str
#*****************************************



#*****************************************
class Specification(BaseModel):
    class_name: int
    specification: str
#*****************************************
class FillPDFFormRequest(BaseModel):
    applicant_name_1: str
    applicant_flat_address_1: str
    applicant_street_address_1: str
    applicant_state_address_1: str
    applicant_type_1: str
    incorporation_country_1: str
    incorporation_state_1: str
    correspondence_name_2: str
    correspondence_flat_address_2: str
    correspondence_street_address_2: str
    correspondence_telephone_2: str
    correspondence_fax_2: str
    correspondence_reference_2: str
    agent_name_3: str
    agent_flat_address_3: str
    agent_street_address_3: str
    agent_country_address_3: str
    agent_telephone_3: str
    agent_fax_3: str
    agent_reference_3: str
    language_5: str
    translation_letters_5: str
    translation_transliteration1_5: str
    translation_transliteration2_5: str
    checkBox_color_6: str
    color_6: str
    checkBox_shape_6: str
    shape_6: str
    checkBox_sound_6: str
    checkBox_smell_6: str
    checkBox_others_6: str
    others_6: str
    convention_date_8: str
    convention_countries_8: str
    convention_applications_8: str
    convention_details_8: str
    checkbox_certification_9: str
    checkbox_collective_9: str
    checkbox_defensive_9: str
    disclaimer_10: str
    confirmation_signatory_11: str
    confirmation_capacity_11: str
    confirmation_date_11: str

class FillPDFForm(ActionMessageRequest):
    type: Literal["FillPDFForm"]
    content: List[FillPDFFormRequest]


######## return model ##########

"""
ActionMessageResult actions: List[Action]

"""



class ActionMessageResult(BaseModel):
    actions: List[Action]

#*********************************************
class GenerateSpecificationResult(Action):
    type: Literal["GenerateSpecification"]
    content: List[Specification]
#**********************************************
class ActionAndMessageResult(BaseModel):
    actions: List[Action]
    messages: List[Message]

class RejectionReason(BaseModel):
    confident: float
    rationale: str

class ResponseResult(BaseModel):
    is_error: bool
    error_message: str
    result: str

#************************************
class AnalysisResult(BaseModel):
    core_product_or_service: str
    target_market: str
    business_goal: str
    key_benefit: str
    unique_selling_proposition: str
    brand_personality: str
    brand_story: str
    emotional_connection: str
#***************************************
class BusinessNatureAnalysisResult(Action):
    type: Literal["BusinessNatureAnalysis"]
    content: AnalysisResult
#****************************************
class ActionAndMessageResponseResult(BaseModel):
    is_error: bool
    error_message: str
    result: ActionAndMessageResult

class ActionResponseResult(ResponseResult):
    is_error: bool
    error_message: str
    result: ActionMessageResult

class MessageResult(BaseModel):
    messages: List[Message]


class MessageResponseResult(BaseModel):
    is_error: bool
    error_message: str
    result: MessageResult

class ActionResponseResult(BaseModel):
    is_error: bool
    error_message: str
    result: ActionMessageResult

class TrademarkNameValidationResult(BaseModel):
    is_rejected: bool
    rejected_reasons: List[RejectionReason]

class ValidateTrademarkNameResult(Action):
    type: Literal["ValidateTrademarkName"]
    content: List[TrademarkNameValidationResult]

class PdfFile(BaseModel):
    pdf_file_path: str
    error_msg: str
   
class FillPDFFormResult(Action):
    type: Literal["FillPDFForm"]
    content: List[PdfFile]


from fastapi.responses import FileResponse

file_path = "abcde.pdf"


""""""""""""""""""""""""""""""
# accepts an `ActionMessageRequest` as input and returns an `ActionResponseResult`.
@app.post("/api/v1/actionMessageRequest")
def construct_action_response(action_message_request: ActionMessageRequest):
    #print(action_message_request.actions[i].type == "BusinessNatureAnalysis")
    response = [] # Store the result in "ActionMessageResult" and it is an action list

    """assume the request looks like"""
    
    query_business = """I am writing to submit a trademark application and would like to raise a few queries to ensure its accuracy and completeness. 我希望向贵局提交商标申请，并提出以下查询。

            we specialize in providing innovative and eco-friendly products for the home. 我们专注于为家庭提供创新和环保的产品。

            it will be associated with our line of eco-friendly home products. 它将与我们的环保家居产品系列相关联。

            Our target audience is environmentally conscious consumers who are looking for high-quality and sustainable products for their homes. 我们的目标受众是环保意识强的消费者，他们寻求高品质和可持续的家居产品。

            Our competitive advantage lies in our commitment to using eco-friendly materials and our focus on design and functionality. 我们的竞争优势在于致力于使用环保材料，并注重设计和功能。

            We operate in the home goods industry and plan to use our trademark throughout the country. 我们在家居用品行业运营，并计划在全国范围内使用商标。

            Prior to submitting this application, we conducted a thorough search and did not find any other trademarks that are similar to ours. 在提交申请之前，我们进行了全面的搜索，没有发现与我们商标相似的其他商标。

            We plan to expand internationally in the future and would like to apply for international trademark protection. 我们计划在未来扩大国际市场，并希望申请国际商标保护。

            Thank you for your attention to this matter. Please let me know if you require any additional information. 谢谢贵局的关注，如有需要，请告知我需要提供哪些额外信息。"""

    query_specification = """We specialize in providing innovative and eco-friendly products 
    for the home. Our target audience is environmentally conscious consumers who are looking for 
    high-quality and sustainable products for their homes. We plan to expand internationally in the 
    future and would like to apply for international trademark protection. Our competitive advantage 
    lies in our commitment to using eco-friendly materials and our focus on design and functionality. 
    The trademark name will be associated with our line of eco-friendly home products."""

    #1. (fake) Request
    action1 = Action(type = "BusinessNatureAnalysis", content = query_business)
    action2 = Action(type = "GenerateSpecification", content = query_specification)
    #action_message_request = ActionMessageRequest(actions = [action1, action2])

    #print(action_message_request2)

    """assume the result generated from the frontend looks like"""
    #2. Find the length of the request 
    length = len(action_message_request.actions)
    #print(length)
    
    #3. Parse each object (Type + Content) in "ActionMessageRequest"
    for i in range(length):
        
        response1 = ""
        response2 = ""
        
        #Test
        if action_message_request.actions[i].type == "hi":
            response1, response2 =  start_point() 
            print(response1)
            print(response2)
        
        #Business Analysis (Block 1)
        if action_message_request.actions[i].type == "BusinessNatureAnalysis":
            input_query = str(action_message_request.actions[i].content)

            #1.Result Generation
            #response1, response2 =  start_point(action_message_request.actions[0].content) 
            #print(action_message_request.actions[i].content)
            response1, response2 =  start_point(input_query) 

            #print(response1)
            #print(response2)

            #2. Results assigned
            """""
            response1["Core product or service"]['non-Chinese']
            response1["Target market"]['non-Chinese']
            response1["Business goals"]['non-Chinese']
            response1["Key benefits"]['non-Chinese']
            response1["Unique selling proposition"]['non-Chinese']
            response1["Brand Personality"]['non-Chinese']
            response1["Brand Story"]['non-Chinese']
            response1["Emotional Connection"]['non-Chinese']
            response1["Trademark Name"]['non-Chinese']
            """""
            #Results to response
            if response1 == "error" and response2 == "error":
                #Because the attributes of the base model "GenerateSpecificationResult" is remained, generate a fake speficiation
                #print("error!!!!!!!!!!!")
                Speficiation_object = Specification(class_name = 0, specification= "Error case")
                
                #Return the error
                #result = ActionResponseResult(
                #is_error=True,
                #error_message="Please provide more information./Please provide the trademark name.",
                #result=ActionMessageResult(actions=[GenerateSpecificationResult(type="GenerateSpecification", content=[Speficiation_object])]))
                result = BusinessNatureAnalysisResult(
                    type="BusinessNatureAnalysis",
                    content= AnalysisResult(
                        core_product_or_service = "None",
                        target_market = "None",
                        business_goal = "None",
                        key_benefit = "None",
                        unique_selling_proposition = "None",
                        brand_personality = "None",
                        brand_story = "None",
                        emotional_connection = "None",
                    )
                )
            else:
                #print(core_product_or_service = response1["Core product or service"]['Non-chinese'])
                #Result stored
                
                result = BusinessNatureAnalysisResult(
                    type="BusinessNatureAnalysis",
                    content= AnalysisResult(
                        core_product_or_service = response1["Core product or service"]['Non-chinese'],
                        target_market = response1["Target market"]['Non-chinese'],
                        business_goal = response1["Business goals"]['Non-chinese'],
                        key_benefit = response1["Key benefits"]['Non-chinese'],
                        unique_selling_proposition = response1["Unique selling proposition"]['Non-chinese'],
                        brand_personality = response1["Brand Personality"]['Non-chinese'],
                        brand_story = response1["Brand Story"]['Non-chinese'],
                        emotional_connection = response1["Emotional Connection"]['Non-chinese'],
                    )
                )
            response.append(result)
            #print(response1)
            #print(response2)
            
        elif action_message_request.actions[i].type == "GenerateSpecification":
            #1.Generate result
            #response1, response2 =  start_point() 
            """assume the result generated from the block 2 looks like"""
            Specification1 = Specification_block(class_index=9,specification="computer technology solutions")
            Specification2 = Specification_block(class_index=42,specification="finanical portfolio")
            Specification3 = Specification_block(class_index=36,specification="financial analysis")
            response1 = [Specification1,Specification2,Specification3]
            #print(response1)
            print(len((response1)))
            
            #2. Extract useful result
            class_names = []
            specifications = []
            specification_length = len(response1)
            for j in range(specification_length):
                class_names.append(response1[j].class_index)
                specifications.append(response1[j].specification) 
            #print(class_names)
            #print(specifications)

            #3. Store them into the Specification object
            contents = []
            for j in range(specification_length):
                #Create Specification object
                Speficiation_object = Specification(class_name=class_names[j],specification=specifications[j])
                contents.append(Speficiation_object)
            #print(contents)
                
            #4. Response
            result =  GenerateSpecificationResult(type="GenerateSpecification", content=contents)
            response.append(result)
        
        # Block 3 (Reserved)
        elif action_message_request.actions[i].type == "ValidateTrademarkName":
            response1, response2 =  start_point(action_message_request.actions[0].content) 
            result = ActionResponseResult(
            is_error=False,
            error_message="",
            result=ValidateTrademarkNameResult()) # Reserved

    return ActionResponseResult(
        is_error=False,
        error_message="",
        result=ActionMessageResult(actions=response)).model_dump()
# `/api/v1/actionMessageRequest`: This endpoint accepts an `ActionMessageRequest` and returns an `ActionResponseResult`
#  It generates a response containing actions. 
#The response includes a list of `GenerateSpecificationResult` objects, each with a `type` of "GenerateSpecification" and a `content` list of `Specification` objects.

@app.post("/api/v1/messageRequest")
def construct_message_response(message_request: MessageRequest):

    #1. Extract the message 
    # speaker = "you" or "TrademarkRobot"
    """assume the request (Question + History) looks like"""
    #class Message(BaseModel):
    #speaker: str
    #message: str
    #created_at: int
    #id: str
    #suggestion: List[str] = []
    message_request2 = MessageRequest(messages = [
        Message(speaker = "you", message = "what's 5 + 2 and let it is a variable 'a'.", created_at = 456, id = "123", suggestion = [] ),
        Message(speaker = "TrademarkRobot", message = "5 + 2 is 7 and 'a' is 7.", created_at = 456, id = "123", suggestion = []),
        Message(speaker = "you", message = "what's 9 + 11 and let it is a variable 'b'.", created_at = 457, id = "123", suggestion = [] ),
        Message(speaker = "TrademarkRobot", message = "9 + 11 is 20 and 'b' is 20.", created_at = 457, id = "123", suggestion = []),
        Message(speaker = "you", message = "what is the summation of 'a' and 'b'?", created_at = 458, id = "123", suggestion = []),
    ])
    #print(message_request2)

    #2. Create History List
    history = []

    length = len(message_request.messages) # How many messages from the request.
    if length !=0: # There are history
        for i in range(length-1):
            if message_request.messages[i].speaker == "you": # Bedrock limitation (only human, ai, system......)
                history_speaker = "human"
            elif message_request.messages[i].speaker == "TrademarkRobot":
                history_speaker = "ai"
            history_message = message_request.messages[i].message
            history_session = (history_speaker, history_message)
            history.append(history_session)
            
            #print(history_session)
    
    #3. Store the user question
    question = message_request.messages[length-1].message
    #print(question)
    #print(history)

    #4 Answer "you" or "human" and then create new object "Message" 
    answer = HistoryExample(question,history)
    # Answer by "AI" or "TrademarkRobot"
    answer_Message = Message(
        speaker = "TrademarkRobot", 
        message = answer, 
        created_at = message_request.messages[length-1].created_at, #Assume "answer" has the same "created_at" as "question"
        id = message_request.messages[length-1].id, #Assume "answer" has the same "id" as "question"
        suggestion = [] ) # Reserved
    
    #3. Store the "answer"
    message_request.messages.append(answer_Message)
    message_request = message_request.messages

    #print(message_request2)
    #print(message_request.messages)

    #4. Return
    return MessageResponseResult(
        is_error=False,
        error_message="",
        result=MessageResult(messages=message_request)).model_dump()

@app.post("/api/v1/actionAndMessageRequest")
def construct_action_and_message_response(action_and_message_request: ActionAndMessageRequest):
    """action_and_message_request looks like"""
    #actions = 
    messages = [
        Message(speaker = "you", message = "what's 5 + 2 and let it is a variable 'a'.", created_at = 456, id = "123", suggestion = [] ),
        Message(speaker = "TrademarkRobot", message = "5 + 2 is 7 and 'a' is 7.", created_at = 456, id = "123", suggestion = []),
        Message(speaker = "you", message = "what's 9 + 11 and let it is a variable 'b'.", created_at = 457, id = "123", suggestion = [] ),
        Message(speaker = "TrademarkRobot", message = "5 + 2 is 7 and 'a' is 7.", created_at = 457, id = "123", suggestion = []),
        Message(speaker = "you", message = "what is the summation of 'a' and 'b'?", created_at = 458, id = "123", suggestion = []),
    ]
    action_and_message_request2 = ActionAndMessageRequest

    """Action"""
    



    """Message"""
    #1. Extract the message 
    # speaker = "you" or "TrademarkRobot"
    #class Message(BaseModel):
    #speaker: str
    #message: str
    #created_at: int
    #id: str
    #suggestion: List[str] = []
    message_request2 = MessageRequest(messages = [
        Message(speaker = "you", message = "what's 5 + 2 and let it is a variable 'a'.", created_at = 456, id = "123", suggestion = [] ),
        Message(speaker = "TrademarkRobot", message = "5 + 2 is 7 and 'a' is 7.", created_at = 456, id = "123", suggestion = []),
        Message(speaker = "you", message = "what's 9 + 11 and let it is a variable 'b'.", created_at = 457, id = "123", suggestion = [] ),
        Message(speaker = "TrademarkRobot", message = "5 + 2 is 7 and 'a' is 7.", created_at = 457, id = "123", suggestion = []),
        Message(speaker = "you", message = "what is the summation of 'a' and 'b'?", created_at = 458, id = "123", suggestion = []),
    ])
    #print(message_request2)
    history = []
    #print(HistoryExample())
    length = len(message_request2.messages)
    if length !=0: 
        for i in range(length-1):
            if message_request2.messages[i].speaker == "you":
                history_speaker = "human"
            elif message_request2.messages[i].speaker == "TrademarkRobot":
                history_speaker = "ai"
            history_message = message_request2.messages[i].message
            history_session = (history_speaker, history_message)
            history.append(history_session)
            
            #print(history_session)
    question = message_request2.messages[length-1].message
    #print(question)
    #print(history)

    #2 Answer "you" and create object "Message"
    answer = HistoryExample(question,history)
    answer_Message = Message(
        speaker = "TrademarkRobot", 
        message = answer, 
        created_at = message_request2.messages[length-1].created_at, 
        id = message_request2.messages[length-1].id, 
        suggestion = [] )
    
    #3 Store the result
    message_request2.messages.append(answer_Message)
    
    message_request2 = message_request2.messages
    #print(message_request2)

    #print(type(answer))

    #print(message_request.messages)
    
    return ActionAndMessageResponseResult(
        is_error=False,
        error_message="",
        result=ActionAndMessageResult(
            actions=[GenerateSpecificationResult(type="GenerateSpecification", content=[Specification(class_name=45,specification="specification1 sample"), Specification(class_name=42,specification="specification2 sample")])],
            messages=action_and_message_request.messages + [Message(speaker="ai", message="here is the AI response from api", created_at=345678, id="sdfghjk")]
        )).model_dump()


from fastapi import FastAPI

#PDF return
@app.post("/api/v1/pdfActionRequest")
def construct_pdf_action_response(action_message_request: ActionMessageRequest):
    request = [] #To store all the useful information from request
    if (action_message_request.actions[0].type == "FillPDFForm"):
        length = len(action_message_request.actions[0].content)

        #Store all the useful information to "request"
        for i in length:
            request.append(action_message_request.actions[0].content[i])
        """
        block4(request)
        """
    
    file_path = "abcde.pdf" # File name, it is expected that the pdf file is generated locally.
    results={"message":"This is just test message"}
    return FileResponse(path = file_path, filename=file_path,headers = results)
 

"""
    results = ActionResponseResult(
        is_error=False,
        error_message= "",
        result=ActionMessageResult(actions=[GenerateSpecificationResult(type="GenerateSpecification", content=[Specification(class_name=45,specification="specification1 sample"), Specification(class_name=42,specification="specification2 sample")])]))
"""