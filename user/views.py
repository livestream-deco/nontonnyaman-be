from django.shortcuts import render

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,logout,login
import json
from importlib import import_module
from django.conf import settings
from .models import *
import json
from django.http.response import HttpResponse, HttpResponseForbidden, JsonResponse
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .models import Account
from stadium.models import Stadium
from .forms import StaffRegistrationForm, StaffListForm, StaffChoiceForm  # Create this form in forms.py

@csrf_exempt
def flutter_register_user(request):
    if request.method == "POST":
        raw = request.body.decode('utf-8')
        cleaned = json.loads(raw)
        register_user = Account.objects.create(role_users=True, email=cleaned["email"], name = cleaned["name"])
        register_user.set_password(cleaned["password"])
        try:
            register_user.save()
        except:
            return HttpResponse(status=409)
        login(request, register_user)
        return JsonResponse({"session-id": request.session.session_key,"is_staff": False, "role_users": True, "email": register_user.email, "name": register_user.name})

@csrf_exempt
def flutter_user_login(request):
    if request.method == "POST":
        data = request.body.decode("utf-8")
        cleaned_data = json.loads(data)
        email = cleaned_data["email"]
        password = cleaned_data["password"]
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return JsonResponse({"session-id": request.session.session_key, "is_staff": False, "role_users": True, "email": user.email})
        
        
def list_staff(request):
    stadium_id = request.GET.get('input_id')
    stadiums = Stadium.objects.get(id=2)
    list_staff = []
    staff = StaffProfile.objects.filter(stadium=stadiums, is_available=True)
    for i in staff:
        list_staff.append({
            'staff_id': i.staff_id,
            'department': i.department,
            'is_available': i.is_available,
            'phone_number': i.phone_number,
            'stadium': i.stadium.stadium_name,
            'user': i.user.email,
        })
    data = json.dumps(list_staff)
    return JsonResponse(data, safe=False)

def register_staff(request):
    if request.method == 'POST':
        staff_form = StaffRegistrationForm(request.POST)

        if staff_form.is_valid():
            staff_form.save()

            # Optionally, set the 'has_chose' attribute to True for the associated Account
            selected_user = staff_form.cleaned_data['user']
            selected_user.has_chose = True
            selected_user.save()

            return redirect('staff_list')  # Redirect to the staff list or a success page
    else:
        staff_form = StaffRegistrationForm()

    return render(request, 'register_staff.html', {'staff_form': staff_form})

def choose_staff(request):
    session_id = request.GET.get('session_id')
    engine = import_module(settings.SESSION_ENGINE)
    sessionstore = engine.SessionStore
    session = sessionstore(session_id)
    email = session.get('_auth_user_id')
    user = Account.objects.get(email = email)
    staff = StaffProfile.objects.get(user = user)
    staff = StaffAssistant.objects.create(user = user, staff = staff)
    user.staff_assistant = staff
    user.save()
    staff.is_available = False
    staff.save()
    return JsonResponse({'isSuccessful':True},safe = False)

def check_list(request):
    staffassistant = Account.objects.get(email = "aldi8@gmail.com")
    staff = StaffAssistant.objects.filter(staff = staffassistant )
    list_staff = []
    for i in staff.user:
        list_staff.append({
            i
        })
    data = json.dumps(list_staff)
    return JsonResponse(data, safe=False)

