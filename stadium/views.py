from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import redirect, render
from stadium.models import Stadium
from stadium.forms import StadiumForm
from django.http import JsonResponse
# Create your views here.

def index(request):
    stadium = Stadium.objects.all()
    response = {'stadium' : stadium}
    return render(request, 'index.html',response)

def stadium_list(request):
    stadium = Stadium.objects.all()
    response = {'stadium' : stadium}
    return render(request, 'stadium_list.html',response)

def add_stadium(request):
    context = {}
    form = StadiumForm(request.POST, request.FILES or None)
    if form.is_valid():
        # save the form data to model
        form.save()
        return redirect("/stadium")
  
    context['form']= form
    return render(request, "stadium_form.html", context)


# def index(request):
#     stadiums = Stadium.objects.all()
#     data = {'stadiums': list(stadiums.values())}
#     return JsonResponse(data)

# def stadium_list(request):
#     stadiums = Stadium.objects.all()
#     data = {'stadiums': list(stadiums.values())}
#     return JsonResponse(data)

# def add_stadium(request):
#     form = StadiumForm(request.POST, request.FILES or None)
#     if form.is_valid():
#         # save the form data to model
#         form.save()
#         return JsonResponse({'status': 'success'})
  
#     errors = form.errors.as_json()
#     return JsonResponse({'status': 'error', 'errors': errors}, status=400)

