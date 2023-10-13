import json
from django.shortcuts import render,redirect
from stadium.forms import StadiumForm,FeatureForm
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from stadium.models import Stadium,StadiumFeature
from user.models import Account
from django.http import HttpResponse, JsonResponse
from django.forms.models import inlineformset_factory

from django.shortcuts import get_object_or_404, render,HttpResponseRedirect
FeatureFormSet = inlineformset_factory(
    Stadium, StadiumFeature, form=FeatureForm, extra=1, can_delete=True
)


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
        'stadium_location' : stadium.stadium_name,
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
    
    # Create a list of dictionaries containing staff information
    staff_info_list = []
    for staff in staff_list:
        staff_info_list.append({
            'staff_id': staff.id,
            'name': staff.name,
            'email': staff.email,
            'stadium_name': staff.stadium.stadium_name if staff.stadium else None,
        })
    
    data = json.dumps(staff_info_list)
    return HttpResponse(data, content_type='application/json')


