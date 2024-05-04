import uuid

from pydantic import Field, BaseModel

from utils.date_time import get_current_iso_datetime


def generate_id():
    return str(uuid.uuid4())


class SpecialConsiderationEmotionInquiryInput(BaseModel):
    id: str = Field(default_factory=generate_id, alias="_id")
    org_key: str = Field(..., min_length=10, alias="orgKey")
    subject_id: str = Field(..., alias="subjectId")
    special_consideration_message: str = Field(..., alias="specialConsiderationMessage")
    last_update_on: str = Field(default_factory=get_current_iso_datetime, alias="lastUpdateOn")


class Emotion(BaseModel):
    expression: str = Field(...)
    accuracy: int = Field(...)
    valence: int = Field(...)
    arousal: int = Field(...)
    special_consideration_message: str = Field(..., alias="specialConsiderationMessage")
    recorded_on: str = Field(default_factory=get_current_iso_datetime, alias="recordedOn")


class SpecialConsiderationEmotionInquiryOutput(BaseModel):
    id: str = Field(..., alias="_id")
    org_key: str = Field(..., min_length=10, alias="orgKey")
    subject_id: str = Field(..., alias="subjectId")
    work_emotions: list[Emotion] = Field(..., alias="workEmotions")
    last_update_on: str = Field(..., alias="lastUpdateOn")


class AuthOrganization(BaseModel):
    org_key: str = Field(..., alias="orgKey")
