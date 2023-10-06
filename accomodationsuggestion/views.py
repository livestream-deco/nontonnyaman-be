import json
from django.shortcuts import render
from accomodationsuggestion.forms import AccomodationForm
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from accomodationsuggestion.models import Accomodation
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,HttpResponseRedirect

def add_accomodation(request):
    if require_http_methods(["POST"]):
        context = {}
        context['form'] = AccomodationForm(request.POST, request.FILES)
        if context['form'].is_valid():
            context['form'].save()
            context['form'] = AccomodationForm()
        return render(request, 'add_accomodation.html', context)   

@csrf_exempt
def detail_accomodation(request):
    accomodation_id = request.GET.get('input_id')
    accomodation = Accomodation.objects.get(id=accomodation_id)
    accomodation_list = []
    accomodation_list.append({
        'accomodation_id' : accomodation.id,
        'accomodation_name' : accomodation.accomodation_name,
        'accomodation_description': accomodation.accomodation_description,
        'accomodation_price': accomodation.accomodation_price,
        'accomodation_picture': json.dumps(str(accomodation.accomodation_picture.url)) if accomodation.accomodation_picture else None,
    })
    data = json.dumps(accomodation_list)
    return HttpResponse(data, content_type='application/json')

@csrf_exempt
def view_accomodation(request):
    accomodation = Accomodation.objects.all()
    return render(request, 'view_all_accomodation.html', 
        {'accomodation': accomodation})

def delete_accomodation(request,id):
    context = {}
    obj = get_object_or_404(Accomodation, id = id)
    if request.method =="POST":
        obj.delete()
        return HttpResponseRedirect("view-accomodation/")    
    return render(request, "delete_accomodation.html", context)
