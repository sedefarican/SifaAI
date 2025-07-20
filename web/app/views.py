from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Patient, AnswerReport, HealthQuestion
from .forms import PatientRegisterForm, PatientLoginForm, ServiceTypeForm, PDFUploadForm
from .utils import extract_text_from_pdf, generate_simplified_explanation


def register_view(request):
    if request.method == 'POST':
        form = PatientRegisterForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.password = make_password(form.cleaned_data['password'])
            patient.save()
            return redirect('login')
    else:
        form = PatientRegisterForm()
    return render(request, 'kullanici/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = PatientLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                patient = Patient.objects.get(username=username)
                if check_password(password, patient.password):
                    request.session['patient_id'] = patient.patient_id
                    return redirect('dashboard')
                else:
                    form.add_error(None, "Şifre yanlış")
            except Patient.DoesNotExist:
                form.add_error('username', "Kullanıcı bulunamadı")
    else:
        form = PatientLoginForm()
    return render(request, 'kullanici/login.html', {'form': form})


def logout_view(request):
    request.session.flush()
    return redirect('login')


def dashboard_view(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('login')
    patient = Patient.objects.get(pk=patient_id)
    return render(request, 'kullanici/dashboard.html', {'patient': patient})

def service_choice_view(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('login')
    
    patient = Patient.objects.get(pk=patient_id)

    if request.method == 'POST':
        form = ServiceTypeForm(request.POST)
        if form.is_valid():
            tercih_obj = form.save(commit=False)
            tercih_obj.patient = patient
            tercih_obj.save()

            # Yönlendirme tercih türüne göre
            tercih = tercih_obj.tercih
            if tercih == 'tahlil':
                return redirect('tahlil_sayfasi')
            elif tercih == 'oneriler':
                return redirect('oneriler_sayfasi')
            elif tercih == 'hatirlatici':
                return redirect('hatirlatici_sayfasi')
            elif tercih == 'soru':
                return redirect('soru_sayfasi')
    else:
        form = ServiceTypeForm()

    return render(request, 'servis/hizmet_sec.html', {'form': form})


def tahlil_view(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('login')
    
    patient = Patient.objects.get(pk=patient_id)

    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf = form.save(commit=False)
            pdf.patient = patient
            pdf.save()

            # 1. PDF dosyasının yolunu al
            pdf_path = pdf.file.path

            # 2. PDF içeriğini çıkar
            raw_text = extract_text_from_pdf(pdf_path)

            # 3. Gemini ile açıklama üret
            explanation = generate_simplified_explanation(raw_text)

            # 4. Veritabanına kaydet (AnswerReport)
            AnswerReport.objects.create(
                patient=patient,
                simple_comment=explanation,
                advices="",  # şimdilik boş bırakabilirsin
            )

            return render(request, 'servis/tahlil_sayfasi.html', {
                'form': PDFUploadForm(),
                'success': True,
                'explanation': explanation
            })
    else:
        form = PDFUploadForm()

    return render(request, 'servis/tahlil_sayfasi.html', {'form': form})


def oneriler_view(request):
    return render(request, 'servis/oneriler_sayfasi.html')

def hatirlatici_view(request):
    return render(request, 'servis/hatirlatici_sayfasi.html')

def soru_view(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('login')
    
    patient = Patient.objects.get(pk=patient_id)

    if request.method == 'POST':
        soru = request.POST.get('soru')
        if soru:
            HealthQuestion.objects.create(patient=patient, question_text=soru)
            return render(request, 'servis/soru_sayfasi.html', {'success': True})

    return render(request, 'servis/soru_sayfasi.html')

def profile_view(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('login')

    patient = Patient.objects.get(pk=patient_id)
    return render(request, 'kullanici/profile.html', {'patient': patient})
