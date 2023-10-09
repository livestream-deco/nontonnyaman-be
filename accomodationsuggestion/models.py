from django.db import models

class Accomodation(models.Model):
    accomodation_name = models.TextField(max_length=100, default='')
    accomodation_description = models.TextField(max_length=10000, default='')
    accomodation_price = models.IntegerField()
    accomodation_picture = models.ImageField(upload_to='images/', blank=True, null=True)

