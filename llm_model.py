# pyrefly: ignore [missing-import]
import google.generativeai as genai
from prompt import create_prompt

# Configure Gemini API
genai.configure(api_key="AIzaSyDPMQGbPhM1iTYZCOyfzu-cRiXh_j8DIEQ")

model = genai.GenerativeModel("gemini-2.5-flash")


def explain_detection(detections):
    try:
        prompt = create_prompt(detections)

        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.2
            }
        )

        return response.text

    except Exception as e:
        print("Gemini Error:", e)
        return f"Gemini Error: {str(e)}"