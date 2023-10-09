from newsletter.models import Newsletter
from django import forms


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ('newsletter_title','newsletter_text','newsletter_picture')
        labels = {
            'newsletter_title': 'Title',
            'newsletter_text': 'Text',
            'newsletter_picture': 'Picture',
            'newsletter_category': 'Category',
        }
        help_texts = {
            'newsletter_text': 'Enter the text for the newsletter',
            'newsletter_picture': 'Upload a picture for the newsletter',
        }
        error_messages = {
            'newsletter_text': {
                'max_length': 'The text is too long',
            },
        }
