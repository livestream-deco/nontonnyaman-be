from django import forms
from .models import Stadium

class StaffAddForm(forms.Form):
    email = forms.EmailField(label='Email')
    name = forms.CharField(max_length=100, label='Name')
    password = forms.CharField(max_length=100, widget=forms.PasswordInput, label='Password')
    stadium = forms.ModelChoiceField(queryset=Stadium.objects.all(), empty_label='Select a Stadium', label='Stadium')
    is_staff = forms.BooleanField(initial=True, required=False, label='Is Staff Member')
