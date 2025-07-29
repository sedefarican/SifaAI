import google.generativeai as genai
import fitz 
from dotenv import load_dotenv
import os

load_dotenv()
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

def extract_text_from_pdf(file_obj):
    doc = fitz.open(stream=file_obj, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# def generate_simplified_explanation(pdf_text):
#     prompt = f"""
#     Aşağıdaki metin bir sağlık tahlili raporudur. Lütfen bu metni teknik terimlerden arındırarak sadeleştir. 
#     Normal bir hasta anlayacak şekilde açıkla ve önemli uyarıları belirt:
    
#     {pdf_text}
#     """
#     response = model.generate_content(prompt)
#     return response.text

def generate_explanation(text):
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    response = model.generate_content(f"Aşağıdaki tıbbi tahlil metnini hastanın anlayabileceği sade bir dille açıkla:\n\n{text}")
    return response.text

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def generate_simplified_explanation(text):
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    prompt = f"Aşağıdaki tıbbi tahlil metnini hastanın anlayabileceği sade bir dille açıkla:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text.strip()

def generate_health_suggestions(text):
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    prompt = f"""
    Aşağıdaki açıklamaya göre hastaya yönelik 4 kısa sağlık önerisi oluştur. 
    Bunlar: beslenme, egzersiz, stres/uyku ve takviye şeklinde dört başlıkta olsun.
    Her biri tek paragraf halinde kısa öneri içersin.
    Açıklama:
    {text}
    """
    response = model.generate_content(prompt)
    lines = response.text.strip().split("\n\n")
    
    titles = ["🥗 Beslenme", "🏃 Egzersiz", "🧘 Stres ve Uyku", "💊 Takviye"]
    colors = ["#ADEED9", "#D6FBF2", "#FFF4F8", "#C7F5E3"]

    suggestions = []
    for i in range(min(4, len(lines))):
        suggestions.append((titles[i], lines[i], colors[i]))
    return suggestions