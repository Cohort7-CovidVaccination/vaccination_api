from rest_framework import serializers
from vaccination_app.models import Countries, Vaccination_registries

class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Countries
        fields = ('id',
                'iso_code',
                'name',
                'source_name',
                'source_website')

class VaccRegistriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vaccination_registries
        fields = ('country_id',
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