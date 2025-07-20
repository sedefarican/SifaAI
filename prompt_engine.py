def generate_tahlil_prompt(user, tahlil_metni):
    return f"""
Kullanıcı Bilgileri:
İsim: {user["isim"]}
Yaş: {user["yaş"]}
Cinsiyet: {user["cinsiyet"]}
Kilo: {user["kilo"]}
Boy: {user["boy"]}
Kronik Hastalıklar: {", ".join(user["kronikHastalıklar"])}
İlaçlar: {", ".join(user["ilaçlar"])}
Alerjiler: {", ".join(user["alerjiler"])}

Tahlil Sonuçları:
{tahlil_metni}

Tahlil sonucu ile ilgili medikal bir açıklama yap.
Ardından bu değerlerin vücutta yol açabileceği belirtileri sade bir dille açıkla.
Son olarak, kişinin neler yapması gerektiğine dair 3 öneri ver.
"""

def generate_reminder_prompt(user):
    return f"""
{user['isim']} adlı hasta, saat 21:00'de Metformin ilacını almalıdır.
Doktoru bu ilacı akşam aç karnına almasını önermiştir.
Bunu hatırlatan sade ve nazik bir mesaj üret.
"""
