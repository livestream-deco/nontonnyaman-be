from django.urls import path

from stadium.views import add_stadium,view_all_stadium, view_detail_stadium,staff_list,choose_stadium, pick_staff,list_request
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
     path('add-stadium/', add_stadium),
     path('view-detail-stadium/', view_detail_stadium),
     path('view-all-stadium/', view_all_stadium),
     path('choose-stadium/', choose_stadium, name='choose_stadium'),
     path('staff-list/', staff_list, name='staff_list'),
      path('staff-list2/', staff_list, name='staff_list2'),
      path('pick-staff/', pick_staff,name='pick_staff'),
      path('list-request/',list_request,)

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)