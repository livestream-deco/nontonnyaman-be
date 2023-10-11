from stadium.models import Stadium
from django import forms


class StadiumForm(forms.ModelForm):
    class Meta:
        model = Stadium
        fields = ('stadium_name','stadium_location','stadium_text', 'stadium_picture', 'stadium_map_picture')
        labels = {
            'stadium_name': 'Title',
            'stadium_location': 'Text',
            'stadium_text': 'Text',
            'stadium_picture': 'Picture',
            'stadium_map_picture': 'Picture',
        }
        help_texts = {
            'stadium_text': 'Enter the text for the newsletter',
            'stadium_map_picture': 'Upload a picture for the newsletter',
        }
        error_messages = {
            'stadium_text': {
                'max_length': 'The text is too long',
            },
        }
