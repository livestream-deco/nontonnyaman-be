from stadium.models import Stadium
from django import forms


class StadiumForm(forms.ModelForm):
    class Meta:
        model = Stadium
        fields = ('stadium_name','stadium_overview','stadium_picture','stadium_map')
        labels = {
            'stadium_name': 'Stadium',
            'stadium_overview': 'Overview',
            'stadium_picture': 'Picture',
            'stadium_map': 'Map',
        }
        help_texts = {
            'stadium_overview': 'Input the overview for the stadium',
            'stadium_picture': 'Upload a picture for the stadium',
            'stadium_map': 'Upload a map of the stadium',
        }
        error_messages = {
            'stadium_overview': {
                'max_length': 'The text is too long',
            },
        }
