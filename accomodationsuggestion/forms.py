from accomodationsuggestion.models import Accomodation
from django import forms


class AccomodationForm(forms.ModelForm):
    class Meta:
        model = Accomodation
        fields = ('accomodation_name','accomodation_description','accomodation_price','accomodation_picture')
        labels = {
            'accomodation_name': 'Name',
            'accomodation_description': 'Description',
            'accomodation_price': 'Price',
            'accomodation_picture': 'Picture',
        }
        help_texts = {
            'accomodation_description': 'Enter the description for the accomodation suggestion',
            'accomodation_picture': 'Please upload a picture for the Accomodation',
        }
        error_messages = {
            'accomodation_description': {
                'max_length': 'The description is too long',
            },
        }
