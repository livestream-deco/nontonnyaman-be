from django.urls import path
from .views import index,add_stadium,stadium_list

urlpatterns = [
    path('', index, name='index'),
    path('add/',add_stadium, name='add' ),
    path('stadium-list/',stadium_list, name='add_note' )
]