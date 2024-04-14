from pydantic import Field, BaseModel


class SpecialConsiderationEmotionInquiryInput(BaseModel):
    special_consideration_message: str = Field(..., alias="specialConsiderationMessage")


class Emotion(BaseModel):
    expression: str = Field(...)
    accuracy: int = Field(...)
    valence: int = Field(...)
    arousal: int = Field(...)


class SpecialConsiderationEmotionInquiryOutput(BaseModel):
    emotion: Emotion = Field(..., alias="emotion")
