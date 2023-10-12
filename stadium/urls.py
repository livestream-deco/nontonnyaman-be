from django.urls import path

from stadium.views import add_stadium,view_all_stadium, view_detail_stadium
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
     path('add-stadium/', add_stadium),
     path('view-detail-stadium/', view_detail_stadium),
     path('view-all-stadium/', view_all_stadium),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)