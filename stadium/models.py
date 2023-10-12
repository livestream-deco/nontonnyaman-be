from django.db import models

class Stadium(models.Model):
    stadium_name = models.TextField(max_length=100, default='')
    stadium_location = models.TextField(max_length=10000, default='')
    stadium_text = models.TextField(max_length=10000, default='')
    stadium_picture = models.ImageField(upload_to='images/', blank=True, null=True)
    stadium_map_picture = models.ImageField(upload_to='images/', blank=True, null=True)

class StadiumFeature(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    stadium = models.ForeignKey(Stadium, related_name='features', on_delete=models.CASCADE)



