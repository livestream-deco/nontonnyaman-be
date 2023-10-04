from stadium.models import Stadium
from django.db import models
from django.forms import ModelForm

class StadiumForm(ModelForm):
    class Meta:
        model = Stadium
        fields = "__all__"
