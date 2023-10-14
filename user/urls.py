from django.urls import path
from user.views import *
urlpatterns = [
     path('flu-register-user/', flutter_register_user),
     path('flu-login/',flutter_user_login),
     path('register-staff/', register_staff, name='add_staff'),
     path('list_staff/', list_staff, name='list_staff'),
     path('choose_staff/', choose_staff, name='choose_staff'),

]