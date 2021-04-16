from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from vaccination_app.models import Countries
from vaccination_app.serializers import CountrySerializer
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['GET', 'POST', 'DELETE'])
def country_list(request):
    if request.method == 'POST':
        country_data = JSONParser().parse(request)
        country_serializer = CountrySerializer(data=country_data)
        if country_serializer.is_valid():
            country_serializer.save()
            return JsonResponse(country_serializer.data, status= status.HTTP_201_CREATED)
        return JsonResponse(country_serializer.errors, status=status.HTTP_400_BAD_REQUEST)