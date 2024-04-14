import os

from dotenv import dotenv_values
from langchain.chains import LLMChain
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_nvidia_ai_endpoints import ChatNVIDIA

from configs.emotion_inquiry import *

READER_MODEL_API_KEY = None
READER_MODEL = None
EMOTION_INQUIRY_ANALYZE_PROMPT = None
EMOTION_INQUIRY_ANALYZE_CHAIN = None
EMOTION_INQUIRY_ANALYZE_OUTPUT_PARSER = None


class EmotionInquiryAnalysis(BaseModel):
    expression: str = Field()
    accuracy: int = Field(ge=0, le=100)
    valence: int = Field(ge=0, le=100)
    arousal: int = Field(ge=0, le=100)


def load_reader_model_api_key() -> str:
    global READER_MODEL_API_KEY

    if not READER_MODEL_API_KEY:
        secrets = dotenv_values("../secrets.env")
        READER_MODEL_API_KEY = secrets.get("NVIDIA_API_KEY")
        os.environ["NVIDIA_API_KEY"] = READER_MODEL_API_KEY
    return READER_MODEL_API_KEY


def load_reader_model() -> ChatNVIDIA:
    global READER_MODEL

    if not READER_MODEL:
        load_reader_model_api_key()
        READER_MODEL = ChatNVIDIA(
            model=READER_MODEL_NAME,
            temperature=0.3,
            max_tokens=1024
        )
    return READER_MODEL


def load_emotion_inquiry_analyze_output_parser() -> JsonOutputParser:
    global EMOTION_INQUIRY_ANALYZE_OUTPUT_PARSER

    if not EMOTION_INQUIRY_ANALYZE_OUTPUT_PARSER:
        EMOTION_INQUIRY_ANALYZE_OUTPUT_PARSER = JsonOutputParser(pydantic_object=EmotionInquiryAnalysis)
    return EMOTION_INQUIRY_ANALYZE_OUTPUT_PARSER


def load_emotion_inquiry_analyze_prompt() -> PromptTemplate:
    global EMOTION_INQUIRY_ANALYZE_PROMPT

    if not EMOTION_INQUIRY_ANALYZE_PROMPT:
        load_emotion_inquiry_analyze_output_parser()
        EMOTION_INQUIRY_ANALYZE_PROMPT = PromptTemplate(
            input_variables=["special_consideration_message"],
            template=EMOTION_INQUIRY_ANALYZE_PROMPT_TEMPLATE,
            template_format="jinja2",
            partial_variables={
                "format_instructions": load_emotion_inquiry_analyze_output_parser().get_format_instructions()
            }
        )
    return EMOTION_INQUIRY_ANALYZE_PROMPT


def load_emotion_inquiry_analyze_chain() -> LLMChain:
    global EMOTION_INQUIRY_ANALYZE_CHAIN

    if not EMOTION_INQUIRY_ANALYZE_CHAIN:
        EMOTION_INQUIRY_ANALYZE_CHAIN = (
                load_emotion_inquiry_analyze_prompt() |
                load_reader_model() |
                load_emotion_inquiry_analyze_output_parser()
        )
    return EMOTION_INQUIRY_ANALYZE_CHAIN


def generate_emotion_inquiry_analysis(special_consideration_message: str) -> dict:
    query_context_analyze_chain = load_emotion_inquiry_analyze_chain()
    response = query_context_analyze_chain.invoke({
        "special_consideration_message": special_consideration_message
    })
    return response
