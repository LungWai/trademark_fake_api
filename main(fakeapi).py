
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

class Specification(BaseModel):
    class_name: int
    specification: str

class GenerateSpecificationResult(Action):
    type: Literal["GenerateSpecification"]
    content: List[Specification]

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

class AnalysisResult(BaseModel):
    core_product_or_service: str
    target_market: str
    business_goal: str
    key_benefit: str
    unique_selling_proposition: str
    brand_personality: str
    brand_story: str
    emotional_connection: str
    error_msg: str

class BusinessNatureAnalysisResult(Action):
    type: Literal["BusinessNatureAnalysis"]
    content: AnalysisResult

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


@app.post("/api/v1/actionMessageRequest")
def construct_action_response(action_message_request: ActionMessageRequest):
    return ActionResponseResult(
        is_error=False,
        error_message="",
        result=ActionMessageResult(actions=[GenerateSpecificationResult(type="GenerateSpecification", content=[Specification(class_name=45,specification="specification1 sample"), Specification(class_name=42,specification="specification2 sample")])])).model_dump()



@app.post("/api/v1/actionAndMessageRequest")
def construct_action_and_message_response(action_and_message_request: ActionAndMessageRequest):
    result = ActionAndMessageResponseResult(
        is_error=False,
        error_message="",
        result=ActionAndMessageResult(
            actions=[GenerateSpecificationResult(type="GenerateSpecification", content=[Specification(class_name=45,specification="specification1 sample"), Specification(class_name=42,specification="specification2 sample")])],
            messages=action_and_message_request.messages + [Message(speaker="TrademarkRobot", message="here is the AI response from api", created_at=345678, id="sdfghjk")]
        )).model_dump()
    return result



@app.post("/api/v1/messageRequest")
def construct_message_response(message_request: MessageRequest):
    return MessageResponseResult(
        is_error=False,
        error_message="",
        result=MessageResult(messages=message_request.messages + [Message(speaker="TrademarkRobot", message="here is the AI response from api", created_at=345678, id="sdfghjk")])).model_dump()

@app.post("/api/v1/pdfActionRequest")
def construct_pdf_action_response(action_message_request: ActionMessageRequest):
    return ActionResponseResult(
        is_error=False,
        error_message="",
        result=ActionMessageResult(actions=[FillPDFFormResult(type="FillPDFForm", content=[PdfFile(pdf_file_path="/completedForm/output.pdf",error_msg="")])])).model_dump()
