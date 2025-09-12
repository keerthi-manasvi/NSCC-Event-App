from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.db import IntegrityError
from django.conf import settings
import qrcode
from io import BytesIO
import openpyxl
from .forms import RegistrationForm
from .models import Participant, Attendance
import os

User = get_user_model()

# QR Generation
def generate_qr_for_participant(request, participant):
    # Ensure folder exists
    qr_folder = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
    os.makedirs(qr_folder, exist_ok=True)

    scheme = "https" if request.is_secure() else "http"
    host = request.get_host()
    url = f"{scheme}://{host}/mark_attendance/{participant.registration_id}/"

    img = qrcode.make(url)
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    filebuffer = ContentFile(buffer.getvalue())
    filename = f"qr_{participant.registration_id}.png"

    participant.qr_code_image.save(filename, filebuffer)
    participant.save()

# Participant registration
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            participant = form.save()
            generate_qr_for_participant(request, participant)
            return redirect('participant_qr', reg_id=participant.registration_id)
    else:
        form = RegistrationForm()
    return render(request, 'Event/register.html', {'form': form})

# Show QR code
def participant_qr(request, reg_id):
    participant = get_object_or_404(Participant, registration_id=reg_id)
    return render(request, 'Event/qr.html', {'participant': participant})

# Mark attendance
@csrf_exempt
def mark_attendance(request, reg_id):
    participant = get_object_or_404(Participant, registration_id=reg_id)
    if request.method in ['GET', 'POST']:
        try:
            Attendance.objects.create(participant=participant)
            message = f"✅ Attendance marked for {participant.name}"
        except IntegrityError:
            message = f"⚠️ Already marked for {participant.name}"
        return JsonResponse({'message': message})
    return JsonResponse({'error': 'Invalid request method'}, status=405)

# Scan page
def scan_page(request):
    return render(request, 'Event/scan.html')

# Export attendance to Excel
@staff_member_required
def export_xlsx(request):
    participants = Participant.objects.all().order_by('name')
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Attendance"
    ws.append(['Name', 'Email', 'Registration ID', 'Status', 'Timestamp'])
    for p in participants:
        attendance = getattr(p, 'attendance', None)
        status = attendance.status if attendance else 'Absent'
        ts = attendance.timestamp.strftime('%Y-%m-%d %H:%M:%S') if attendance else ''
        ws.append([p.name, p.email, p.registration_id, status, ts])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=attendance.xlsx'
    wb.save(response)
    return response

# Dashboard
@staff_member_required
def dashboard(request):
    participants = Participant.objects.all().order_by('name')
    return render(request, 'Event/dashboard.html', {'participants': participants})

# Clear participants
@staff_member_required
def clear_participants(request):
    Participant.objects.all().delete()
    return redirect('dashboard')

# Authentication
def SignUp_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        confirmation = request.POST.get("confirmation", "").strip()
        if password != confirmation:
            return render(request, "Event/SignUp.html", {"message": "Passwords do not match."})
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_staff = True
            user.save()
            login(request, user)
            return redirect("dashboard")
        except IntegrityError:
            return render(request, "Event/SignUp.html", {"message": "Username already exists."})
    return render(request, "Event/SignUp.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "Event/login.html", {"message": "Invalid credentials."})
    return render(request, "Event/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")
