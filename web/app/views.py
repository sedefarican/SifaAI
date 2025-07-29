from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Patient, AnswerReport, HealthQuestion
from .forms import PatientRegisterForm, PatientLoginForm, ServiceTypeForm, PDFUploadForm
from .utils import extract_text_from_pdf, generate_explanation, generate_simplified_explanation, generate_health_suggestions
from io import BytesIO

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
                uploaded_file = request.FILES['file']
                
                # 1. Dosya içeriğini belleğe al
                file_copy = BytesIO(uploaded_file.read())

                # 2. PDF verisini bellekte oku
                raw_text = extract_text_from_pdf(file_copy)

                # 3. Gemini ile açıklama oluştur
                explanation = generate_explanation(raw_text)

                # 4. Dosyayı kaydet
                pdf = form.save(commit=False)
                pdf.patient = patient
                pdf.save()

                # 5. Açıklamayı veritabanına yaz
                AnswerReport.objects.create(
                    patient=patient,
                    simple_comment=explanation,
                    advices="",  # daha sonra eklenecekse
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
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('login')

    patient = Patient.objects.get(pk=patient_id)
    reports = AnswerReport.objects.filter(patient=patient).order_by('-date')

    suggestions = []
    explanation_text = ""

    if request.method == 'POST':
        pdf_form = PDFUploadForm(request.POST, request.FILES)
        selected_report_id = request.POST.get('report_id')

        # Kullanıcı PDF yüklediyse
        if pdf_form.is_valid() and request.FILES.get('file'):
            file = request.FILES['file']
            text = extract_text_from_pdf(file)
            explanation_text = generate_simplified_explanation(text)

        # Kullanıcı eski bir açıklama seçtiyse
        elif selected_report_id:
            try:
                selected_report = AnswerReport.objects.get(id=selected_report_id, patient=patient)
                explanation_text = selected_report.simple_comment
            except AnswerReport.DoesNotExist:
                explanation_text = ""

        # Açıklama bulunduysa öneri üret
        if explanation_text:
            suggestions = generate_health_suggestions(explanation_text)
    else:
        pdf_form = PDFUploadForm()

    return render(request, 'servis/oneriler_sayfasi.html', {
        'pdf_form': pdf_form,
        'reports': reports,
        'suggestions': suggestions
    })
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('login')

    patient = Patient.objects.get(pk=patient_id)
    reports = AnswerReport.objects.filter(patient=patient).order_by('-date')

    suggestions = []
    explanation_text = ""

    if request.method == 'POST':
        pdf_form = PDFUploadForm(request.POST, request.FILES)
        selected_report_id = request.POST.get('report_id')

        if pdf_form.is_valid() and 'file' in request.FILES:
            # Yeni PDF dosyası yüklendi
            file = request.FILES['file']
            text = extract_text_from_pdf(file)
            explanation_text = generate_simplified_explanation(text)

        elif selected_report_id:
            try:
                selected_report = AnswerReport.objects.get(id=selected_report_id, patient=patient)
                explanation_text = selected_report.simple_comment
            except AnswerReport.DoesNotExist:
                explanation_text = ""

        if explanation_text:
            suggestions = generate_health_suggestions(explanation_text)
    else:
        pdf_form = PDFUploadForm()

    return render(request, 'servis/oneriler_sayfasi.html', {
        'pdf_form': pdf_form,
        'reports': reports,
        'suggestions': suggestions
    })

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
    
    reports = AnswerReport.objects.filter(patient=patient).order_by('-date')
    
    return render(request, 'kullanici/profile.html', {
        'patient': patient, 
        'reports': reports
    })
