from django.urls import path

from stadium.views import add_stadium,view_all_stadium,view_stadium_detail
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
     path('add-stadium/', add_stadium),
     path('view-detail-stadium/<int:input_id>/', view_stadium_detail),
     path('view-all-stadium/', view_all_stadium),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)