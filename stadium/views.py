import json
from django.shortcuts import render
from stadium.forms import StadiumForm
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from stadium.models import Stadium
from django.http import HttpResponse, JsonResponse

from django.shortcuts import get_object_or_404, render,HttpResponseRedirect



def add_stadium(request):
    if require_http_methods(["POST"]):
        context = {}
        context['form'] = StadiumForm(request.POST, request.FILES)
        if context['form'].is_valid():
            context['form'].save()
            context['form'] = StadiumForm()
        return render(request, 'stadium.html', context)

@csrf_exempt
def view_detail_stadium(request):
    stadium_id = request.GET.get('input_id')
    stadium = Stadium.objects.get(id=stadium_id)
    stadium_list = []
    stadium_list.append({
        'stadium_id' : stadium.id,
        'stadium_name' : stadium.stadium_name,
        'stadium_location' : stadium.stadium_name,
        'stadium_text': stadium.stadium_text,
        'stadium_picture': json.dumps(str(stadium.stadium_picture.url)) if stadium.stadium_picture else None,
        'stadium_map_picture': json.dumps(str(stadium.stadium_map_picture.url)) if stadium.stadium_map_picture else None,
    })
    data = json.dumps(stadium_list)
    return HttpResponse(data, content_type='application/json')

@csrf_exempt
def view_all_stadium(request):
    stadiums = Stadium.objects.all()
    
    stadium_list = []
    for stadium in stadiums:
        stadium_list.append({
            'stadium_id' : stadium.id,
            'stadium_name' : stadium.stadium_name,
            'stadium_location' : stadium.stadium_name,
            'stadium_text': stadium.stadium_text,
            'stadium_picture': json.dumps(str(stadium.stadium_picture.url)),
            'stadium_map_picture': json.dumps(str(stadium.stadium_map_picture.url))
        })
        
    data = json.dumps(stadium_list)
    return HttpResponse(data, content_type='application/json')

def delete_stadium(request,id):
    context ={}
    obj = get_object_or_404(Stadium, id = id) 
    if request.method =="POST":
        obj.delete()
        return HttpResponseRedirect("list/")   
    return render(request, "delete_view.html", context)
