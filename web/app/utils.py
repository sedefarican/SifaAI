import google.generativeai as genai
import fitz 
from dotenv import load_dotenv
import os

load_dotenv()
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def generate_simplified_explanation(pdf_text):
    prompt = f"""
    Aşağıdaki metin bir sağlık tahlili raporudur. Lütfen bu metni teknik terimlerden arındırarak sadeleştir. 
    Normal bir hasta anlayacak şekilde açıkla ve önemli uyarıları belirt:
    
    {pdf_text}
    """
    response = model.generate_content(prompt)
    return response.text