import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY2")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")

def tanya_gemini(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"[Gagal memproses ke Gemini API]: {e}"
