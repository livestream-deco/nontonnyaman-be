import json
from django.shortcuts import render
from newsletter.forms import NewsletterForm
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from newsletter.models import Newsletter
from django.http import HttpResponse, JsonResponse

from django.shortcuts import get_object_or_404, render,HttpResponseRedirect

from newsletter.models import Newsletter

def add_newsletter(request):
    if require_http_methods(["POST"]):
        context = {}
        context['form'] = NewsletterForm(request.POST, request.FILES)
        if context['form'].is_valid():
            context['form'].save()
            context['form'] = NewsletterForm()
        return render(request, 'newsletter.html', context)   

# def add_newsletter(request):
#     if request.method ==  "POST":
#         form = NewsletterForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('add-newsletter/')

@csrf_exempt
def view_detail_newsletter(request, input_id):
    newsletter = Newsletter.objects.get(id=input_id)
    newsletter_list = []
    newsletter_list.append({
        'newsletter_id' : newsletter.id,
        'newsletter_title' : newsletter.newsletter_title,
        'newsletter_text': newsletter.newsletter_text,
        'newsletter_picture': json.dumps(str(newsletter.newsletter_picture.url)) if newsletter.newsletter_picture else None,
    })
    data = json.dumps(newsletter_list)
    return HttpResponse(data, content_type='application/json')

@csrf_exempt
def view_all_newsletter(request):
    newsletters = Newsletter.objects.all()
        
    return render(request, 'viewall.html', 
        {
		'newsletters':newsletters})

def delete_newsletter(request,id):
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(Newsletter, id = id)
 
 
    if request.method =="POST":
        obj.delete()
        return HttpResponseRedirect("list/")
    
    return render(request, "delete_view.html", context)

def newsletterhtmk(request):
    obj=Newsletter.objects.all()
    return render(request,'list.html',{"obj":obj})
