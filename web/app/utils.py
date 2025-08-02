import google.generativeai as genai
import fitz 
from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import datetime


load_dotenv()
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash-lite")

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
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
    #model = genai.GenerativeModel("gemini-1.5-flash-latest")
    response = model.generate_content(f"Aşağıdaki tıbbi tahlil metnini hastanın anlayabileceği sade bir dille açıkla:\n\n{text}")
    return response.text

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def generate_simplified_explanation(text):
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
    #model = genai.GenerativeModel("gemini-1.5-flash-latest")
    prompt = f"Aşağıdaki tıbbi tahlil metnini hastanın anlayabileceği sade bir dille açıkla:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text.strip()

def generate_health_suggestions(text):
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
    #model = genai.GenerativeModel("gemini-1.5-flash-latest")
    prompt = f"""
    Aşağıdaki açıklamaya göre hastaya yönelik 4 kısa sağlık önerisi oluştur. 
    Bunlar: beslenme, egzersiz, stres/uyku ve takviye şeklinde dört başlıkta olsun.
    Her biri tek paragraf halinde kısa öneri içersin. 
    Önünde tabii, hemen yapıyorum gibi ifadeler olmasın. İçerik ile başla.
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

def ask_gemini(question_text: str) -> str:
    try:
        response = model.generate_content(
            f"Hasta şu soruyu sordu: {question_text}. "
            f"Cevabı sade ve anlaşılır bir dille açıkla."
        )
        return response.text
    except Exception as e:
        return f"Hata: {str(e)}"
    
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def get_calendar_service():
    creds = None
    token_path = 'token.json'

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)

def create_reminder_event(title, description, start_time, recurrence_rule):
    service = get_calendar_service()

    event = {
        'summary': title,
        'description': description,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Europe/Istanbul',
        },
        'end': {
            'dateTime': (start_time + datetime.timedelta(minutes=30)).isoformat(),
            'timeZone': 'Europe/Istanbul',
        },
        'recurrence': [
            recurrence_rule
        ],
    }

    return service.events().insert(calendarId='primary', body=event).execute()