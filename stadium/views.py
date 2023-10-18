from importlib import import_module
import json
from django.shortcuts import render,redirect
from stadium.forms import StadiumForm,FeatureForm
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from stadium.models import Stadium,StadiumFeature
from user.models import *
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.forms.models import inlineformset_factory


from django.shortcuts import get_object_or_404, render,HttpResponseRedirect
FeatureFormSet = inlineformset_factory(
    Stadium, StadiumFeature, form=FeatureForm, extra=1, can_delete=True
)

@csrf_exempt
def list_request(request):
    session_id = request.GET.get('session_id')
    engine = import_module(settings.SESSION_ENGINE)
    sessionstore = engine.SessionStore
    session = sessionstore(session_id)
    email = session.get('_auth_user_id')
    owninguser = Account.objects.get(email = email)
    staff = StaffProfile.objects.get(user = owninguser)
    staffAssistantList = StaffAssistant.objects.filter(staff=staff)
    userlist = []
    for i in staffAssistantList :
        user = i.user
        userlist.append({
        'name' : user.name,
        'email' : user.email,
        'disability' : user.disability,
        'user_picture': json.dumps(str(user.image.url)) if user.image else None,

        })
    data = json.dumps(userlist)
    return HttpResponse(data, content_type='application/json')

def add_stadium(request):
    # if require_http_methods(["POST"]):
    #     context = {}
    #     context['form'] = StadiumForm(request.POST, request.FILES)
    #     if context['form'].is_valid():
    #         context['form'].save()
    #         context['form'] = StadiumForm()
    #     return render(request, 'stadium.html', context)
    if request.method == 'POST':
        form = StadiumForm(request.POST, request.FILES)
        if form.is_valid():
            stadium = form.save()
            feature_formset = FeatureFormSet(request.POST, instance=stadium)
            if feature_formset.is_valid():
                feature_formset.save()
            context = {'form': form, 'feature_formset': feature_formset}
            return render(request, 'stadium.html', context)
    else:
        form = StadiumForm()
        feature_formset = FeatureFormSet()
    return render(request, 'stadium.html', {'form': form, 'feature_formset': feature_formset})

@csrf_exempt
def view_detail_stadium(request):
    stadium_id = request.GET.get('input_id')
    stadium = Stadium.objects.get(id=stadium_id)
    stadium_list = []
    stadium_data = {
        'stadium_id' : stadium.id,
        'stadium_name' : stadium.stadium_name,
        'stadium_location' : stadium.stadium_location,
        'stadium_text': stadium.stadium_text,
        'stadium_picture': json.dumps(str(stadium.stadium_picture.url)) if stadium.stadium_picture else None,
        'stadium_map_picture': json.dumps(str(stadium.stadium_map_picture.url)) if stadium.stadium_map_picture else None,
    }
    # stadium_list = {
    #     'stadium_id' : stadium.id,
    #     'stadium_name' : stadium.stadium_name,
    #     'stadium_location' : stadium.stadium_name,
    #     'stadium_text': stadium.stadium_text,
    #     'stadium_picture': str(stadium.stadium_picture.url) if stadium.stadium_picture else None,
    #     'stadium_map_picture': str(stadium.stadium_map_picture.url) if stadium.stadium_map_picture else None,
    # }    
    print(stadium_data["stadium_map_picture"])
    features_data = []
    for feature in stadium.features.all():
        features_data.append({
            'name': feature.name,
            'latitude': float(feature.latitude) if feature.latitude else None,
            'longitude': float(feature.longitude) if feature.longitude else None,
        })
    
    stadium_data['features'] = features_data
    stadium_list.append(stadium_data)

    data = json.dumps(stadium_list)
    return HttpResponse(data, content_type='application/json')

@csrf_exempt
def view_all_stadium(request):
    stadiums = Stadium.objects.all()

    stadium_list = []
    for stadium in stadiums:
        features_data = []
        for feature in stadium.features.all():
            features_data.append({
                'name': feature.name,
                'latitude': float(feature.latitude) if feature.latitude else None,
                'longitude': float(feature.longitude) if feature.longitude else None,
            })

        stadium_data = {
            'stadium_id': stadium.id,
            'stadium_name': stadium.stadium_name,
            'stadium_location': stadium.stadium_name,
            'stadium_text': stadium.stadium_text,
            'stadium_picture': json.dumps(str(stadium.stadium_picture.url)) if stadium.stadium_picture else None,
            'stadium_map_picture': json.dumps(str(stadium.stadium_map_picture.url)) if stadium.stadium_map_picture else None,
            'features': features_data,
        }
        stadium_list.append(stadium_data)
    data = json.dumps(stadium_list)
    return HttpResponse(data, content_type='application/json')

def delete_stadium(request,id):
    context ={}
    obj = get_object_or_404(Stadium, id = id) 
    if request.method =="POST":
        obj.delete()
        return HttpResponseRedirect("list/")   
    return render(request, "delete_view.html", context)

def staff_list(request, stadium_id):
    stadium_id = request.GET.get('input_id')
    selected_stadium = Stadium.objects.get(id=stadium_id)
    
    if selected_stadium:
        staff_list = Account.objects.filter(is_staff=True, stadium=selected_stadium)
    else:
        staff_list = Account.objects.filter(is_staff=True)
    
    stadiums = Stadium.objects.all()
    
    context = {
        'staff_list': staff_list,
        'selected_stadium': selected_stadium,
        'stadiums': stadiums,
    }
    
    return render(request, 'staff_list.html', context)


def choose_stadium(request):
    stadiums = Stadium.objects.all()
    
    if request.method == 'POST':
        selected_stadium_id = request.POST.get('stadium')
        return redirect('staff_list', stadium_id=selected_stadium_id)
    
    context = {
        'stadiums': stadiums,
    }
    
    return render(request, 'choose_stadium.html', context)

def staff_list(request):
    stadium_id = request.GET.get('input_id')
    selected_stadium = Stadium.objects.get(id=stadium_id)
    
    if selected_stadium:
        staff_list = Account.objects.filter(is_staff=True, stadium=selected_stadium)
    else:
        staff_list = Account.objects.filter(is_staff=True)

    staff_info_list = []
    for i in staff_list:
        if StaffProfile.objects.get(user = i, is_available = True):
                staff = StaffProfile.objects.get(user = i, is_available = True)
                staff_info_list.append({
                    'staff_id': staff.staff_id,
                    'name': i.name,
                    'email': i.email,
                    'stadium_name': staff.stadium if staff.stadium else None,
                })

    # Create a list of dictionaries containing staff information
    
    data = json.dumps(staff_info_list)
    return HttpResponse(data, content_type='application/json')

@csrf_exempt
def pick_staff(request):
    session_id = request.GET.get('session_id')
    engine = import_module(settings.SESSION_ENGINE)
    sessionstore = engine.SessionStore
    session = sessionstore(session_id)
    email = session.get('_auth_user_id')
    owninguser = Account.objects.get(email = email)
    owninguser.has_chose = True
    owninguser.save()
    staff_id = request.GET.get('input_id')
    staff = StaffProfile.objects.get(staff_id = staff_id)
    staffAssistant = StaffAssistant.objects.create(user=owninguser, staff=staff)
    staffAssistant.save()
    return JsonResponse({'isSuccessful':True},safe = False)


    






