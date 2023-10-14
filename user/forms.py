from django import forms
from .models import StaffProfile
from stadium.models import Stadium

class StaffRegistrationForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = ['user', 'staff_id', 'department', 'is_available', 'phone_number','stadium']

class StaffListForm(forms.Form):
    staff_member = forms.ModelChoiceField(
        queryset=StaffProfile.objects.all(),
        empty_label='Select a staff member',
    )
    stadium = forms.ModelChoiceField(
        queryset=Stadium.objects.all(),
        empty_label='Select a stadium',
    )

class StaffChoiceForm(forms.Form):
    stadium = forms.ModelChoiceField(
        queryset=Stadium.objects.all(),
        empty_label='Select a stadium',
    )
    staff_choices = forms.ModelMultipleChoiceField(
        queryset=StaffProfile.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
