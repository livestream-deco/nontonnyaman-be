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
from .forms import StaffAddForm  # Create this form in forms.py

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

def add_staff(request):
    if request.method == 'POST':
        form = StaffAddForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            stadium_id = form.cleaned_data['stadium']
            is_staff = form.cleaned_data['is_staff']

            # Create a new staff member
            staff = Account.objects.create(email=email, name=name, is_staff=is_staff)
            if is_staff:
                # Associate the staff member with a stadium
                staff.stadium_id = stadium_id
                staff.save()
            
            return redirect('staff_list')  # Redirect to a staff list view or another page
    else:
        form = StaffAddForm()

    context = {
        'form': form,
    }
    return render(request, 'add_staff.html', context)

