import streamlit as st

# Terim sözlüğü
terim_sozlugu = {
    "Hipertansiyon": "Kan basıncının normalin üzerinde olması",
    "LDL Kolesterol": "Kötü huylu kolesterol; damarları tıkayabilir",
    "HDL Kolesterol": "İyi huylu kolesterol; damarları korur",
    "Trigliserid": "Kandaki yağ türü; yüksekliği riskli olabilir",
    "HbA1c": "Son 3 ayın ortalama kan şekeri değeri",
    "Kreatinin": "Böbrek fonksiyonlarını gösteren bir değer",
    "TSH": "Tiroid bezini kontrol eden hormon",
    "AST / ALT": "Karaciğerin sağlığını gösteren enzimler",
    "Anemi": "Kan değerlerinin düşüklüğü; halsizlik yapar",
    "Statin": "Kolesterolü düşüren ilaç grubu",
    "Metformin": "Diyabet hastalarında şeker kontrolü için kullanılan ilaç",
    "Lisinopril": "Tansiyon düşürücü bir ilaç",
    "Levotiroksin": "Tiroid hormonu eksikliğinde kullanılan ilaç",
    "Sertralin": "Depresyon ve kaygı bozukluklarında kullanılan ilaç",
    "Osteoporoz": "Kemiklerin zayıflayıp kolay kırılması durumu",
    "Tiroid Yetmezliği": "Tiroid hormonunun yeterince üretilememesi",
    "Gut": "Ürik asit birikimiyle oluşan, eklem ağrılarına yol açan hastalık",
    "Romatoid Artrit": "Eklemlerde ağrı ve şişlikle giden otoimmün hastalık",
    "B12 Eksikliği": "Sinir sistemi ve enerji üretimi için gerekli bir vitaminin eksikliği",
    "D Vitamini Eksikliği": "Kemik sağlığı ve bağışıklık için gerekli bir vitaminin eksikliği"
}

st.set_page_config(page_title="Tıbbi Terim Açıklayıcı", layout="centered")
st.title("Tıbbi Terim Açıklama Sistemi")

user_input = st.text_area("Doktor açıklaması ya da sistem çıktısı:", height=200)

if st.button("Açıklamaları Göster"):
    if not user_input.strip():
        st.warning("Lütfen bir metin giriniz.")
    else:
        st.subheader("🔍 Açıklamalı Metin")

        tokens = user_input.split()
        highlighted = []

        for word in tokens:
            clean_word = word.strip(".,;!?()[]")
            explanation = terim_sozlugu.get(clean_word)
            if explanation:
                highlighted.append(f"<span title='{explanation}' style='background-color:#fff3cd;'>{word}</span>")
            else:
                highlighted.append(word)

        result = " ".join(highlighted)
        st.markdown(result, unsafe_allow_html=True)


file_path = "/mnt/data/s2-3_streamlit_sozluk_demo.py"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(streamlit_code)

file_path
