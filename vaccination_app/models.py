from django.db import models

# Create your models here.
class Countries(models.Model):
    iso_code = models.CharField(max_length=3, blank=False)
    name = models.CharField(max_length=50, blank=False)
    source_name = models.CharField(max_length=100, blank=False, default='')
    source_website = models.CharField(max_length=50, blank=False, default='')