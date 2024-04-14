from utils.emotion_inquiry import generate_emotion_inquiry_analysis


def analyze_emotion_inquiry(special_consideration_msg: str) -> dict:
    return generate_emotion_inquiry_analysis(special_consideration_msg)
