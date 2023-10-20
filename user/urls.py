from django.urls import path
from user.views import *

## URL Patterns used in the application

urlpatterns = [
     path('flu-register-user/', flutter_register_user),
     path('flu-login/',flutter_user_login),
     path('register-staff/', register_staff, name='add_staff'),
     path('list_staff/', list_staff, name='list_staff'),
     path('choose_staff/', choose_staff, name='choose_staff'),
     path('user_info/', flutter_get_user_info, name='user_info'),
     path('edit_user/', flutter_edit_user, name='edit_user'),
     path('staff-detail/',staff_detail),
     path('user-info-detail/',flutter_user_info),
     path('confirm-user/',confirm_user),
     path('info-staff/',info_staff),
     path('end-task/', end_task),
     path('decline-user/', decline_user)
]