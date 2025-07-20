from django.db import models

# Create your models here.
class Patient (models.Model):
     patient_id = models.AutoField(primary_key=True)
     name = models.CharField(max_length=100)
     username = models.CharField(max_length=100, unique=True)
     password = models.CharField(max_length=100)
     email = models.EmailField(unique=True)
     birth_date = models.DateField()
     gender = models.CharField(max_length=10)
     weight = models.FloatField()
     height = models.FloatField()
     illness = models.CharField(max_length=200, blank=True, null=True)
     drugs = models.CharField(max_length=200, blank=True, null=True)
     surgical_history = models.TextField(blank=True, null=True)
     age = models.IntegerField()


     def __str__(self):
          return self.name
    
    
class ServiceType(models.Model):
     service_type_id = models.AutoField(primary_key=True)
     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
     SERVICE_CHOICES = [
          ('tahlil', 'Tahlil sonucu açıklatmak'),
          ('soru', 'Sağlıkla ilgili soru sormak'),
          ('oneriler', 'Beslenme / egzersiz önerisi almak'),
          ('hatirlatici', 'Hatırlatıcı kurmak')
     ]
     tercih = models.CharField(max_length=20, choices=SERVICE_CHOICES, default='tahlil')
     tarih = models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return f"{self.patient.username} - {self.tercih()} - {self.tarih}"
   
class UpdatedFiles(models.Model):
     updated_file_id = models.AutoField(primary_key=True)
     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
     file = models.FileField(upload_to='updated_files/')
     date = models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return f"{self.patient.username} - PDF {self.patient.username}"
   
class AnswerReport(models.Model):
     report_id = models.AutoField(primary_key=True)
     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
     simple_comment = models.TextField()
     advices = models.TextField()
     date = models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return f"{self.patient.username} - Sağlık Raporu {self.date}"
   
class Reminder(models.Model):
     reminder_id = models.AutoField(primary_key=True)
     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
     title = models.CharField(max_length=100)
     description = models.TextField(blank=True)
     date = models.DateTimeField()
     calender_id = models.CharField(max_length=255, blank=True, null=True)  # Google Calendar ID

     def __str__(self):
          return f"{self.patient.username} - Hatırlatıcı: {self.title}"
     
     
class HealthQuestion(models.Model):
    question_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    question_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.username} - {self.created_at.strftime('%d.%m.%Y %H:%M')}"
