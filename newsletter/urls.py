from django.urls import path

from newsletter.views import add_newsletter, view_detail_newsletter,view_all_newsletter
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
     path('add-newsletter/', add_newsletter),
     path('view-detail-newsletter/<str:input_id>/', view_detail_newsletter),
     path('view-all-newsletter/', view_all_newsletter),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)