from django.contrib import admin
from .models import Patient, ServiceType, UpdatedFiles, AnswerReport, Reminder

# Register your models here.

admin.site.register(Patient)
admin.site.register(ServiceType)
admin.site.register(UpdatedFiles)
admin.site.register(AnswerReport)
admin.site.register(Reminder)