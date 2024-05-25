from Backend.Message.ChatBot import ChatBot
from Backend.BusinessNatureAnalysis_action.BusinessNatureAnalysis import Business_Analysis
from Backend.FillPDFForm_action.FillPDFForm import DataAndForm_assignment


from fastapi.responses import FileResponse

from typing import Union

from fastapi import FastAPI, Path
from typing import Optional

from typing import Union, List, Any, Literal
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


file_path = "Backend\FillPDFForm_action\Report.pdf"

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

######## query model ##########

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
#************************************
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

""""""""""""""""""""""""""""""
# accepts an `ActionMessageRequest` as input and returns an `ActionResponseResult`.
@app.post("/api/v1/actionMessageRequest")
def construct_action_response(action_message_request: ActionMessageRequest):

    response = [] 
    """assume the result generated from the frontend looks like"""
    #2. Find the length of the request 
    length = len(action_message_request.actions)
    #print(length)
    def BA_pipe(content):
        response1, response2 =  Business_Analysis(content) 
        #Results to response
        if response1 == "error" and response2 == "error":
            Speficiation_object = Specification(class_name = 0, specification= "Error case")
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
        return result

    
    #3. Parse each object (Type + Content) in "ActionMessageRequest"
    for i in range(length):
        response1 = ""
        response2 = ""
        #Business Analysis (Block 1)
        if action_message_request.actions[i].type == "BusinessNatureAnalysis":
            input_query = str(action_message_request.actions[i].content)
            result = BA_pipe(input_query)
            response.append(result)

        elif action_message_request.actions[i].type == "GenerateSpecification":

            """assume the result generated from the block 2 looks like"""
            Specification1 = Specification_block(class_index=9,specification="computer technology solutions")
            Specification2 = Specification_block(class_index=42,specification="finanical portfolio")
            Specification3 = Specification_block(class_index=36,specification="financial analysis")
            response1 = [Specification1,Specification2,Specification3]
            print(len((response1)))
            
            #2. Extract useful result
            class_names = []
            specifications = []
            specification_length = len(response1)
            for j in range(specification_length):
                class_names.append(response1[j].class_index)
                specifications.append(response1[j].specification) 
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
            response1, response2 =  Business_Analysis(action_message_request.actions[0].content) 
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
    answer = ChatBot(question,history)
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
    answer = ChatBot(question,history)
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
    print("hi")
    length = len(action_message_request.actions)
    for i in range(length):
        if action_message_request.actions[i].type == "FillPDFForm":
            """
            #Data extraction and assign value
            input =  {"ui_applicant_name_1" :  action_message_request.actions[i].content[0],
            "ui_applicant_flat_address_1" : action_message_request.actions[i].content[1], 
            "ui_applicant_street_address_1" : action_message_request.actions[i].content[2], 
            "ui_applicant_state_address_1" : action_message_request.actions[i].content[3], 
            "ui_applicant_type_1" : action_message_request.actions[i].content[4], 
            "ui_incorporation_country_1" : action_message_request.actions[i].content[5], 
            "ui_incorporation_state_1" : action_message_request.actions[i].content[6], 
            "ui_correspondence_name_2" : action_message_request.actions[i].content[7], 
            "ui_correspondence_flat_address_2" : action_message_request.actions[i].content[8], 
            "ui_correspondence_street_address_2" : action_message_request.actions[i].content[9], 
            "ui_correspondence_telephone_2" : action_message_request.actions[i].content[10], 
            "ui_correspondence_fax_2" : action_message_request.actions[i].content[11], 
            "ui_correspondence_reference_2" : action_message_request.actions[i].content[12], 
            "ui_agent_name_3" : action_message_request.actions[i].content[13], 
            "ui_agentr_flat_address_3" : action_message_request.actions[i].content[14], 
            "ui_agent_street_address_3" : action_message_request.actions[i].content[15], 
            "ui_agent_country_address_3" : action_message_request.actions[i].content[16], 
            "ui_agent_telephone_3" : action_message_request.actions[i].content[17], 
            "ui_agent_fax_3" : action_message_request.actions[i].content[18], 
            "ui_agent_reference_3" : action_message_request.actions[i].content[19], 
            "ui_language_5" : action_message_request.actions[i].content[20], 
            "ui_translation_letters_5" : action_message_request.actions[i].content[21], 
            "ui_translation_transliteration1_5" : action_message_request.actions[i].content[22], 
            "ui_translation_transliteration2_5" : action_message_request.actions[i].content[23], 
            "ui_checkBox_color_6" : action_message_request.actions[i].content[24], 
            "ui_color_6" : action_message_request.actions[i].content[25], 
            "ui_checkBox_shape_6" : action_message_request.actions[i].content[26], 
            "ui_shape_6" : action_message_request.actions[i].content[27], 
            "ui_checkBox_sound_6" : action_message_request.actions[i].content[28], 
            "ui_checkBox_smell_6" : action_message_request.actions[i].content[29], 
            "ui_checkBox_others_6" : action_message_request.actions[i].content[30], 
            "ui_others_6" : action_message_request.actions[i].content[31], 
            "ui_convention_date_8" : action_message_request.actions[i].content[32], 
            "ui_convention_countries_8" : action_message_request.actions[i].content[33], 
            "ui_convention_applications_8" : action_message_request.actions[i].content[34], 
            "ui_convention_details_8" : action_message_request.actions[i].content[35], 
            "ui_checkbox_certification_9" : action_message_request.actions[i].content[36], 
            "ui_checkbox_collective_9" : action_message_request.actions[i].content[37], 
            "ui_checkbox_defensive_9" : action_message_request.actions[i].content[38], 
            "ui_disclaimer_10" : action_message_request.actions[i].content[39], 
            "ui_confirmation_signatory_11" : action_message_request.actions[i].content[40], 
            "ui_confirmation_capacity_11" : action_message_request.actions[i].content[41], 
            "ui_confirmation_date_11" : action_message_request.actions[i].content[42]}
            input = str(input)
            """
            #sample input
            input = '{"ui_applicant_name_1" : "ABCC Company Limited","ui_applicant_flat_address_1" : "Suite 1223 Happy Plaza", "ui_applicant_street_address_1" : "121 Des Voeux Road Central", "ui_applicant_state_address_1" : "Hong Kong", "ui_applicant_type_1" : "2", "ui_incorporation_country_1" : "UNITED STATES OF AMERICA", "ui_incorporation_state_1" : "NA", "ui_correspondence_name_2" : "Lee & Co", "ui_correspondence_flat_address_2" : "Suite 507 Delight Plaza", "ui_correspondence_street_address_2" : "130 Des Voeux Road", "ui_correspondence_telephone_2" : "21234567", "ui_correspondence_fax_2" : "23216547", "ui_correspondence_reference_2" : "TM/0507", "ui_agent_name_3" : "Lee & Co", "ui_agentr_flat_address_3" : "Suite 507 Delight Plaza", "ui_agent_street_address_3" : "130 Des Voeux Road", "ui_agent_country_address_3" : "HONG KONG", "ui_agent_telephone_3" : "21234567", "ui_agent_fax_3" : "23216547", "ui_agent_reference_3" : "TM/0507", "ui_language_5" : "Symbolic", "ui_translation_letters_5" : "wew", "ui_translation_transliteration1_5" : "T", "ui_translation_transliteration2_5" : "M", "ui_checkBox_color_6" : "True", "ui_color_6" : "Color combination is part of the mark", "ui_checkBox_shape_6" : "", "ui_shape_6" : "", "ui_checkBox_sound_6" : "", "ui_checkBox_smell_6" : "", "ui_checkBox_others_6" : "True", "ui_others_6" : "Stylized letters are part of the mark", "ui_convention_date_8" : "01-01-2020", "ui_convention_countries_8" : "", "ui_convention_applications_8" : "", "ui_convention_details_8" : "", "ui_checkbox_certification_9" : "True", "ui_checkbox_collective_9" : "", "ui_checkbox_defensive_9" : "", "ui_disclaimer_10" : "The logo shall be our exclusive intellectual property", "ui_confirmation_signatory_11" : "John Doe", "ui_confirmation_capacity_11" : "Founder", "ui_confirmation_date_11" : "03-05-2024"}'
            
            #Form filling
            DataAndForm_assignment(input)
            
            #Extract file
            file_path = "Backend\FillPDFForm_action\Report.pdf" 
            results={"message":"This is just test message"}
            return FileResponse(path = file_path, filename=file_path,headers = results)
 