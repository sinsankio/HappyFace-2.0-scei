import uvicorn
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder

from api.models import *
from services.special_consideration_emotion_analysis import *
from utils.mongodb import load_db_configs, get_db_connected, get_db_disconnected

app = FastAPI(root_path="/happyface/v2/scei")


@app.on_event("startup")
async def startup_client():
    db_configs = load_db_configs()
    get_db_connected(db_configs.get("DB_URI"), db_configs.get("DB_NAME"))


@app.on_event("shutdown")
def shutdown_client():
    get_db_disconnected()


@app.post(
    "/inquiry",
    response_description="analyze and save special consideration inquiry input",
    status_code=status.HTTP_200_OK,
    response_model=SpecialConsiderationEmotionInquiryOutput)
async def invoke_special_consideration_emotion_inquiry(
        special_consideration_emotion_inquiry: SpecialConsiderationEmotionInquiryInput = Body(...)
) -> dict:
    if emotion_inquiry_analysis_results := analyze_emotion_inquiry(
            special_consideration_emotion_inquiry.special_consideration_message
    ):
        return save_emotion_inquiry_analysis(
            emotion_inquiry_analysis_results["emotion"],
            jsonable_encoder(special_consideration_emotion_inquiry)
        )
    raise HTTPException(status_code=status.HTTP_400_NOT_FOUND, detail="special consideration analysis failed")


@app.post("/emotions",
          response_description="get organizational subject emotion inquiry analysis results",
          status_code=status.HTTP_200_OK,
          response_model=list[SpecialConsiderationEmotionInquiryOutput])
async def invoke_get_organizational_emotion_inquiry_analysis(
        auth_organization: AuthOrganization = Body(...)) -> list:
    if authenticate(auth_organization.org_key):
        return get_organizational_emotion_inquiry_analysis(auth_organization.org_key)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized request")


@app.delete("/emotions",
            response_description="delete already used organizational subject emotion inquiry analysis results",
            status_code=status.HTTP_200_OK)
async def invoke_delete_organizational_emotion_inquiry_analysis(
        auth_organization: AuthOrganization = Body(...)) -> int:
    if authenticate(auth_organization.org_key):
        return delete_organizational_emotion_inquiry_analysis(auth_organization.org_key)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized request")


if __name__ == "__main__":
    uvicorn.run(app, port=5004)
