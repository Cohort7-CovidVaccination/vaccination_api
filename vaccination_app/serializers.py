from rest_framework import serializers
from vaccination_app.models import Countries, Vaccination_registries, Manufacturer

class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Countries
        fields = ('id',
                'iso_code',
                'name',
                'source_name',
                'source_website')

class VaccRegistriesSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(read_only=True, source="country.name")

    class Meta:
        model = Vaccination_registries
        fields = ('country',
                'country_name',
                'date_data',
                'total_vaccinations',
                'people_vaccinated',
                'people_fully_vaccinated',
                'daily_vaccinations_raw',
                'daily_vaccinations',
                'total_vaccinations_per_hundred',
                'people_vaccinated_per_hundred',
                'people_fully_vaccinated_per_hundred',
                'daily_vaccinations_per_million')

class ManufacturerSerializer(serializers.ModelSerializer):

    total_countries = serializers.IntegerField()

    class Meta:
        model = Manufacturer
        fields = ('name',
                'countries',
                'total_countries')