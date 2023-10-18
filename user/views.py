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
from django.core.files.storage import default_storage

@csrf_exempt
def end_task(request):
    session_id = request.GET.get('session_id')
    engine = import_module(settings.SESSION_ENGINE)
    sessionstore = engine.SessionStore
    session = sessionstore(session_id)
    email = session.get('_auth_user_id')
    user = Account.objects.get(email=email)
    staffUser = StaffProfile.objects.get(user=user)
    staffConfirm = StaffAssistant.objects.get(staff=staffUser)
    staffConfirm.user.has_chose = False
    staffUser.is_available = True
    staffUser.save()
    staffConfirm.user.save()
    staffConfirm.delete()
    return JsonResponse({"session-id": request.session.session_key, "email": user.email, "name": user.name})

@csrf_exempt
def flutter_register_user(request):
    if request.method == "POST":
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            name = request.POST.get('name')
            disability = request.POST.get('disability')
            image = request.FILES.get('image')
            # You need to handle the image data appropriately based on your setup
            # Here, I'm saving the uploaded file to Django's default storage
            # and using its path to create the Account
            file_path = default_storage.save(image.name, image)
            image = request.FILES.get('image')
            if image is not None:
                file_path = default_storage.save(image.name, image)
            else:
                file_path = None 

            
            register_user = Account.objects.create(email=email, name=name, disability=disability,image = file_path)
            register_user.set_password(password)
            register_user.save()

            login(request, register_user)

            return JsonResponse({
                "session-id": request.session.session_key,
                "is_staff": False, 
                "role_users": True, 
                "email": register_user.email, 
                "name": register_user.name, 
                "disability" : register_user.disability,
                "image": file_path
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def flutter_user_login(request):
    if request.method == "POST":
        data = request.body.decode("utf-8")
        cleaned_data = json.loads(data)
        email = cleaned_data["email"]
        password = cleaned_data["password"]
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            is_staff = StaffProfile.objects.filter(user=user).exists()
            
            return JsonResponse({
                "session-id": request.session.session_key, 
                "is_staff": is_staff, 
                "role_users": True, 
                "email": user.email
            })

        else:
            return JsonResponse({"error": "Invalid login credentials"})
        

        
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
            'userpicture': json.dumps(str(i.user.image.url)) if i.user.image.url else None
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
        'user_picture': json.dumps(str(staff.user.image.url)) if staff.user.image.url else None
    })
    data = json.dumps(staff_detail)
    return HttpResponse(data, content_type='application/json')

@csrf_exempt
def flutter_user_info(request):
    emails = request.GET.get('email')
    user = Account.objects.get(email=emails)
    listkosong = []
    response_data = {
        "email": user.email,
        "name": user.name,
        "disability" : user.disability,
        'user_picture': json.dumps(str(user.image.url)) if user.image.url else None,
        "has_chose" : user.has_chose,
    }
    listkosong.append(response_data)
    data = json.dumps(listkosong)

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def flutter_get_user_info(request):
    session_id = request.GET.get('session_id')
    engine = import_module(settings.SESSION_ENGINE)
    sessionstore = engine.SessionStore
    session = sessionstore(session_id)
    email = session.get('_auth_user_id')
    user = Account.objects.get(email=email)
    listkosong = []
    if (user.staff_assistant):
        staff = user.staff_assistant.staff
        response_data = {
        "session-id": request.session.session_key,
        "email": user.email,
        "name": user.name,
        "disability" : user.disability,
        'user_picture': json.dumps(str(user.image.url)) if user.image.url else None,
        "staff_picture": json.dumps(str(user.staff_assistant.staff.user.image.url)) if user.staff_assistant.staff.user.image.url else None,
        "has_chose" : user.has_chose,
        "staff_email" : staff.user.email,
        "staff_name" : staff.user.name,
        "staff_number" : staff.phone_number,
        "staff" : True,
         }
    else:
        response_data = {
            "session-id": request.session.session_key,
            "email": user.email,
            "name": user.name,
            "disability" : user.disability,
            'user_picture': json.dumps(str(user.image.url)) if user.image.url else None,
            "has_chose" : user.has_chose,
            "staff" : False,
        }
    listkosong.append(response_data)
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def flutter_edit_user(request):
    if request.method == "POST":
        session_id = request.POST.get('session_id')
        engine = import_module(settings.SESSION_ENGINE)
        sessionstore = engine.SessionStore
        session = sessionstore(session_id)
        email = session.get('_auth_user_id')   
        print(email)
        password = request.POST.get('password')
        name = request.POST.get('name')
        disability = request.POST.get('disability')
        image = request.FILES.get('image')
        user = Account.objects.get(email = email)
        if image is not None:
            file_path = default_storage.save(image.name, image)
            user.image = file_path
        user.disability = disability
        user.name = name

        user.save()
        return JsonResponse({"session-id": request.session.session_key})
    
@csrf_exempt
def confirm_user(request):
    session_id = request.GET.get('session_id')
    engine = import_module(settings.SESSION_ENGINE)
    sessionstore = engine.SessionStore
    session = sessionstore(session_id)
    email = session.get('_auth_user_id')
    email_user = request.GET.get('email')
    user = Account.objects.get(email=email)
    staffUser = StaffProfile.objects.get(user=user)
    userRequest = Account.objects.get(email=email_user)
    staffConfirm = StaffAssistant.objects.get(staff=staffUser, user=userRequest)
    userRequest.staff_assistant = staffConfirm
    userRequest.save()
    staffUser.is_available = False
    staffUser.save()
    staffAll = StaffAssistant.objects.filter(staff=staffUser)
    for i in staffAll:
        if i.user != userRequest:
            i.user.has_chose = False
            i.user.has_chose.save()
    # Delete StaffAssistant objects where user is not equal to userRequest
    StaffAssistant.objects.exclude(user=userRequest, staff = staffUser).delete()
    return JsonResponse({"session-id": request.session.session_key, "email": user.email, "name": user.name})

@csrf_exempt
def info_staff(request):
    session_id = request.GET.get('session_id')
    engine = import_module(settings.SESSION_ENGINE)
    sessionstore = engine.SessionStore
    session = sessionstore(session_id)
    email = session.get('_auth_user_id')
    user = Account.objects.get(email=email)
    staff = StaffProfile.objects.get(user = user)
    if not StaffAssistant.objects.filter(staff=staff).exists():
        response_data = {
            "confirmed" : False,
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        staffUser = StaffProfile.objects.get(user=user)
        staffConfirm = StaffAssistant.objects.get(staff=staffUser)
        print(staffConfirm.user.image)
        if not staffUser.is_available:
            response_data = {
                "email": staffConfirm.user.name,
                "name": staffConfirm.user.email,
                "disability" : staffConfirm.user.disability,
                'user_picture': json.dumps(str(staffConfirm.user.image.url)) if staffConfirm.user.image.url else None,
                "confirmed" : True,
            }
        else:
            response_data = {
                "confirmed" : False,
            }
        
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def decline_user(request):
    session_id = request.GET.get('session_id')
    engine = import_module(settings.SESSION_ENGINE)
    sessionstore = engine.SessionStore
    session = sessionstore(session_id)
    email = session.get('_auth_user_id')
    email_user = request.GET.get('email')
    user = Account.objects.get(email=email)
    staffUser = StaffProfile.objects.get(user=user)
    userRequest = Account.objects.get(email=email_user)
    staffConfirm = StaffAssistant.objects.get(staff=staffUser, user=userRequest)
    staffConfirm.delete()
    userRequest.has_chose = False
    userRequest.save()
    # Delete StaffAssistant objects where user is not equal to userRequest
    return JsonResponse({"session-id": request.session.session_key, "email": user.email, "name": user.name})







    


    

    




