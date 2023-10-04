from django.db import models

class Newsletter(models.Model):
    newsletter_title = models.TextField(max_length=100, default='')
    newsletter_text = models.TextField(max_length=10000, default='')
    newsletter_picture = models.ImageField(upload_to='images/', blank=True, null=True)

