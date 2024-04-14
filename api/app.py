import uvicorn
from fastapi import FastAPI, APIRouter, Body, HTTPException, status

from api.models import *
from services.special_consideration_emotion_analysis import *

app = FastAPI()

prefix_router = APIRouter(prefix="/hf/v2/scei")


@app.post(
    "/analyze",
    response_description="analyze special consideration input",
    status_code=status.HTTP_200_OK,
    response_model=SpecialConsiderationEmotionInquiryOutput)
async def invoke_special_consideration_emotion_analysis(
        special_consideration_emotion_inquiry: SpecialConsiderationEmotionInquiryInput = Body(...)
) -> dict:
    if special_consideration_emotion_results := generate_emotion_inquiry_analysis(
            special_consideration_emotion_inquiry.special_consideration_message
    ):
        return special_consideration_emotion_results
    raise HTTPException(status_code=status.HTTP_400_NOT_FOUND, detail="special consideration analysis failed")


if __name__ == "__main__":
    app.include_router(prefix_router)
    uvicorn.run(app, port=5004)
