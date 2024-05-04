from utils.date_time import get_current_iso_datetime
from utils.emotion_inquiry import generate_emotion_inquiry_analysis
from utils.mongodb import insert_one, find_one, update_one, find_all, delete_many


def analyze_emotion_inquiry(special_consideration_msg: str) -> dict:
    return generate_emotion_inquiry_analysis(special_consideration_msg)


def save_emotion_inquiry_analysis(emotion_analysis: dict, emotion_inquiry: dict) -> dict:
    entry = emotion_inquiry.copy()
    del entry["specialConsiderationMessage"]
    emotion_analysis["specialConsiderationMessage"] = emotion_inquiry["specialConsiderationMessage"]
    emotion_analysis["recordedOn"] = get_current_iso_datetime()
    entry["workEmotions"] = [emotion_analysis]
    if found_entry := find_one(
            {"orgKey": entry["orgKey"], "subjectId": entry["subjectId"]}, {}):
        found_entry["workEmotions"].extend(entry["workEmotions"])
        found_entry["lastUpdateOn"] = get_current_iso_datetime()
        update_one({"orgKey": entry["orgKey"], "subjectId": entry["subjectId"]},
                   {"$set": found_entry})
        return find_one({"_id": found_entry["_id"]}, {})
    entry["lastUpdateOn"] = get_current_iso_datetime()
    insertion = insert_one(entry)
    return find_one({"_id": insertion.inserted_id}, {})


def get_organizational_emotion_inquiry_analysis(org_key: str) -> list[dict]:
    return find_all({"orgKey": org_key}, {}, sort=[("lastUpdateOn", -1)])


def delete_organizational_emotion_inquiry_analysis(org_key: str) -> int:
    return delete_many({"orgKey": org_key}).deleted_count


def authenticate(org_key: str) -> bool:
    return find_one({"orgKey": org_key}, {}) is not None
