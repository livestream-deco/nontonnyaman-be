import json
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from newsletter.models import Newsletter
from newsletter.views import add_newsletter, view_detail_newsletter

image_name = 'ui_logo.jpg'
image_path = 'newsletter/images/ui_logo.jpg'
image_type = 'image/jpeg'
add_newsletter_url = '/add-newsletter/'
file= SimpleUploadedFile(name='ui_logo.jpg', content=open('newsletter/images/ui_logo.jpg', 'rb').read(), content_type='image/jpeg')
new_picture = SimpleUploadedFile(name='ui_logo.jpg', content=open('newsletter/images/ui_logo.jpg', 'rb').read(), content_type='image/jpeg')
class AddNewsletterTest(TestCase):
    def create_newsletter(self):
        response = self.client.post('newsletter/add-newsletter/', {
            'newsletter_text': 'test',
            'newsletter_picture': file,
        })

    def test_add_newsletter(self):
        test_image = SimpleUploadedFile(name=image_name, content=open(image_path, 'rb').read(), content_type=image_type)
        response = add_newsletter((self.client.post(
            add_newsletter_url, {
                'newsletter_text': 'test',
                'newsletter_picture': test_image,
                })).wsgi_request)
        self.assertEqual(response.status_code, 200)

    def test_get_list_newsletter(self):
        new_picture = SimpleUploadedFile(name='ui_logo.jpg', content=open('newsletter/images/ui_logo.jpg', 'rb').read(), content_type='image/jpeg')
        return Newsletter.objects.create(newsletter_text='test', newsletter_picture=file, newsletter_category='tips')   