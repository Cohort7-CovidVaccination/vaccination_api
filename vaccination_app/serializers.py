from rest_framework import serializers
from vaccination_app.models import Countries

class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Countries
        fields = ('id',
                'iso_code',
                'name',
                'source_name',
                'source_website')