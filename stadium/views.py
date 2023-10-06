import json
from django.shortcuts import render
from stadium.forms import StadiumForm
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render,HttpResponseRedirect
from stadium.models import Stadium



@csrf_exempt
def view_all_stadium(request):
    stadium = Stadium.objects.all()
        
    return render(request, 'stadium_list.html', 
        {
		'stadiums':stadium})

def add_stadium(request):
    if require_http_methods(["POST"]):
        context = {}
        context['form'] = StadiumForm(request.POST, request.FILES)
        if context['form'].is_valid():
            context['form'].save()
            context['form'] = StadiumForm()
        return render(request, 'stadium.html', context)   

def delete_stadium(request,id):
    context ={}
    # fetch the object related to passed id
    obj = get_object_or_404(Stadium, id = id)
    if request.method =="POST":
        obj.delete()
        return HttpResponseRedirect("list/")
    
    return render(request, "delete_stadium_view.html", context)

@csrf_exempt
def view_stadium_detail(input_id):
    stadium = Stadium.objects.get(id=input_id)
    stadium_list = []
    print(stadium.stadium_picture.url)
    stadium_list.append({
        'stadium_id' : stadium.id,
        'stadium_name' : stadium.stadium_name,
        'stadium_overview': stadium.stadium_overview,
        'stadium_picture': json.dumps(str(stadium.stadium_picture.url)) if stadium.stadium_picture else None,
        'stadium_map': json.dumps(str(stadium.stadium_map.url)) if stadium.stadium_map else None,
    })
    data = json.dumps(stadium_list)
    return HttpResponse(data, content_type='application/json')


def stadiumhtmk(request):
    obj=Stadium.objects.all()
    return render(request,'stadlist_htmk.html',{"obj":obj})

