import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("API anahtarı bulunamadı. .env dosyasını kontrol edin.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

def send_prompt_to_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text
