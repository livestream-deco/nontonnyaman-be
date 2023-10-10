from django.urls import path
from accomodationsuggestion.views import add_accomodation, view_accomodation, detail_accomodation 
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
     path('add-accomodation/', add_accomodation),
     path('detail-accomodation/<str:input_id>/', detail_accomodation),
     path('view-accomodation/', view_accomodation),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)