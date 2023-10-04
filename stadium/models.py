from django.db import models

# TODO Create Friend model that contains name, npm, and DOB (date of birth) here


class Stadium(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    overview = models.TextField()
    
