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
        register_user = Account.objects.create(email=cleaned["email"], name = cleaned["name"])
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
        
@csrf_exempt
def list_staff(request):
    stadium_id = request.GET.get('input_id')
    stadiums = Stadium.objects.get(id=stadium_id)
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
    return HttpResponse(data, content_type='application/json')

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

def flutter_user_info(request):
    if request.method == "GET":
        user = request.user
        if user.is_authenticated:
            return JsonResponse({
                "email": user.email,
                "name": user.name,
                "is_staff": user.is_staff,
                "role_users": user.role_users,
                "session-id": request.session.session_key,
            })
        else:
            return HttpResponseForbidden("You are not authenticated")
        

def flutter_edit_user(request):
    if request.method == "POST":
        user = request.user
        if user.is_authenticated:
            data = request.body.decode('utf-8')
            cleaned_data = json.loads(data)
            if 'email' in cleaned_data:
                user.email = cleaned_data['email']
            if 'name' in cleaned_data:
                user.name = cleaned_data['name']
            if 'password' in cleaned_data:
                user.set_password(cleaned_data['password'])
            user.save()
            return JsonResponse({
                "message": "User information updated successfully.",
                "email": user.email,
                "name": user.name,
                "is_staff": user.is_staff,
                "role_users": user.role_users,
                "session-id": request.session.session_key,
            })
        else:
            return HttpResponseForbidden("You are not authenticated")

@csrf_exempt
def staff_detail(request):
    staff_id = request.GET.get('input_id')
    staff = StaffProfile.objects.get(staff_id = staff_id)
    staff_detail = []
    staff_detail.append({
        'staff_id': staff_id,
        'department': staff.department,
        'is_available': staff.is_available,
        'phone_number': staff.phone_number,
        'stadium': staff.stadium.stadium_name,
        'user': staff.user.email,
    })
    data = json.dumps(staff_detail)
    return HttpResponse(data, content_type='application/json')

@csrf_exempt
def flutter_get_user_info(request):
    session_id = request.GET.get('session_id')
    engine = import_module(settings.SESSION_ENGINE)
    sessionstore = engine.SessionStore
    session = sessionstore(session_id)
    email = session.get('_auth_user_id')
    user = Account.objects.get(email=email)
    response_data = {
        "session-id": request.session.session_key,
        "email": user.email,
        "name": user.name
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json")

