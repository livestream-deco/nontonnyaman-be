from django.urls import path
from user.views import *
urlpatterns = [
     path('flu-register-user/', flutter_register_user),
     path('flu-login/',flutter_user_login),
     path('user_info/', flutter_user_info, name='user_info'),
     path('edit_user/', flutter_edit_user, name='edit_user'),
]