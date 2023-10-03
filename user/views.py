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
from django.contrib.auth.decorators import login_required

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

@login_required
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
        
@login_required
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