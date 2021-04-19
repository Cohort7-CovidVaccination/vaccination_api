from django.db import models

# Create your models here.
class Countries(models.Model):
    """
    Represent a country with the iso_code as index
    """

    iso_code        = models.CharField(max_length=8, blank=False, db_index=True)
    name            = models.CharField(max_length=50, blank=False)
    source_name     = models.CharField(max_length=150, blank=True, default='')
    source_website  = models.CharField(max_length=400, blank=True, default='')

class Vaccination_registries(models.Model):
    """
    Represent a register of vaccinations of a country in a certain date
    """

    country                     = models.ForeignKey('Countries', on_delete=models.PROTECT)
    date_data                   = models.DateField(blank=False, db_index=True)
    total_vaccinations           = models.IntegerField(blank=True)
    people_vaccinated           = models.IntegerField(blank=True)
    people_fully_vaccinated     = models.IntegerField(blank=True)
    daily_vaccinations_raw      = models.IntegerField(blank=True)
    daily_vaccinations          = models.IntegerField(blank=True)
    total_vaccinations_per_hundred       = models.FloatField(blank=True)
    people_vaccinated_per_hundred       = models.FloatField(blank=True)
    people_fully_vaccinated_per_hundred = models.FloatField(blank=True)
    daily_vaccinations_per_million      = models.FloatField(blank=True)

class Manufacturer(models.Model):
    """
    Represent a manufacturer of vaccines
    """

    name = models.CharField(max_length=150, blank=False, db_index=True)
    countries = models.ManyToManyField(Countries)