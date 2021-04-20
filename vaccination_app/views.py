from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.db.models import Count

from vaccination_app.models import Countries, Vaccination_registries, Manufacturer
from vaccination_app.serializers import CountrySerializer, VaccRegistriesSerializer, ManufacturerSerializer
from rest_framework.decorators import api_view

from datetime import datetime

@api_view(['GET'])
def countries_list(request):
    """
    Return the country list with the basic information.
    Without params return the all list.
    With iso_code param return the information of the requiered country
    """
    if request.method == 'GET':
        countries = Countries.objects.all()

        iso_code = request.GET.get('iso_code', None)
        if iso_code is not None:
            countries = countries.filter(iso_code__icontains=str(iso_code).upper())

            if countries.count() == 0:
                return JsonResponse('Country iso_code not found',safe=False, status= status.HTTP_400_BAD_REQUEST)

        country_name = request.GET.get('country_name', None)
        if country_name is not None:
            countries = countries.filter(name__icontains=str(country_name).lower())

            if countries.count() == 0:
                return JsonResponse('Country name not found',safe=False, status= status.HTTP_400_BAD_REQUEST)

        countries_serializer = CountrySerializer(countries, many=True)

        return JsonResponse(countries_serializer.data, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
def vaccinations(request):
    """
    Return all the vaccination registries according to the params query
    Without params: Not allowed 404 returned requiring almost one param
    With iso_code param return all the vaccination registries for that country
    With From param return all teh vaccination registries for all countries from that date
    With To param return all teh vaccination registries for all countries to that date

    Param can be merged: Ex. ?iso_code=col&from=2021-04-20&to=2021-04-09
    """
    if request.method == 'GET':

        iso_code = request.GET.get('iso_code', None)
        from_date = request.GET.get('from', None)
        to_date = request.GET.get('to', None)
        country_name = request.GET.get('country_name', None)

        if (iso_code is None and from_date is None and to_date is None and country_name is None):
            return JsonResponse('Please send almost one of the allowed params country_name, iso_code, from or to',
                                safe=False, status= status.HTTP_400_BAD_REQUEST)

        if iso_code is not None:
            try:
                country = Countries.objects.get(iso_code=str(iso_code).upper())
            except:
                return JsonResponse('Failed to search iso_code, try again',
                                safe=False, status= status.HTTP_400_BAD_REQUEST)
            vaccinations = Vaccination_registries.objects.filter(country=country)

        if country_name is not None:
            try:
                country = Countries.objects.get(name__icontains=str(country_name).lower())
            except:
                return JsonResponse('Failed to search country_name, try again',
                                safe=False, status= status.HTTP_400_BAD_REQUEST)
            vaccinations = Vaccination_registries.objects.filter(country=country)

        if iso_code is None and country_name is None:
            if from_date is not None and to_date is None:
                vaccinations = Vaccination_registries.objects.filter(date_data__gte=datetime.strptime(from_date, '%Y-%m-%d'))

            if from_date is None and to_date is not None:
                vaccinations = Vaccination_registries.objects.filter(date_data__lte=datetime.strptime(to_date, '%Y-%m-%d'))

            if from_date is not None and to_date is not None:
                vaccinations = Vaccination_registries.objects.filter(date_data__gte=datetime.strptime(from_date, '%Y-%m-%d')).filter(
                    date_data__lte=datetime.strptime(to_date, '%Y-%m-%d'))

        else:
            if from_date is not None and to_date is None:
                vaccinations = vaccinations.filter(date_data__gte=datetime.strptime(from_date, '%Y-%m-%d'))

            if from_date is None and to_date is not None:
                vaccinations = vaccinations.filter(date_data__lte=datetime.strptime(to_date, '%Y-%m-%d'))

            if from_date is not None and to_date is not None:
                vaccinations = vaccinations.filter(date_data__gte=datetime.strptime(from_date, '%Y-%m-%d')).filter(
                    date_data__lte=datetime.strptime(to_date, '%Y-%m-%d'))

        registries_serializer = VaccRegistriesSerializer(vaccinations, many=True)

        return JsonResponse(registries_serializer.data, safe=False, status=status.HTTP_200_OK)


@api_view(['GET'])
def vacc_summary(request):
    """
    Return the last vaccination register of the requiered country.
    Without params not allowed 404 returned
    With iso_code param return the last vaccination register of the  country
    """
    if request.method == 'GET':

        iso_code = request.GET.get('iso_code', None)
        country_name = request.GET.get('country_name', None)

        if iso_code is not None:
            try:
                country = Countries.objects.get(iso_code=str(iso_code).upper())
            except:
                return JsonResponse('Failed to search iso_code, try again',
                                safe=False, status= status.HTTP_400_BAD_REQUEST)
            vacc_summary = Vaccination_registries.objects.filter(country=country).order_by('-date_data')[0]

        if country_name is not None:
            try:
                country = Countries.objects.get(name__icontains=str(country_name).lower())
            except:
                return JsonResponse('Failed to search country_name, try again',
                                safe=False, status= status.HTTP_400_BAD_REQUEST)
            vacc_summary = Vaccination_registries.objects.filter(country=country).order_by('-date_data')[0]
        else:
            return JsonResponse('Please send the iso_code param',
                                safe=False, status= status.HTTP_400_BAD_REQUEST)

        registries_serializer = VaccRegistriesSerializer(vacc_summary)

        return JsonResponse(registries_serializer.data, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
def manufacturers(request):
    """
    Return the manufacturers list with the basic information.
    Without params return the all list.
    With iso_code param return the information of the requiered country
    With manufacturer param return the manufactured and countries related
    """
    if request.method == 'GET':
        manufacturers = Manufacturer.objects.all().annotate(total_countries=Count('countries'))

        iso_code = request.GET.get('iso_code', None)
        manufacturer = request.GET.get('manufacturer', None)
        country_name = request.GET.get('country_name', None)

        if iso_code is not None and manufacturer is not None:
            return JsonResponse('''Use one of the allowed params: iso_code or manufactured
                                or no params, try again''',
                                safe=False, status= status.HTTP_400_BAD_REQUEST)

        if iso_code is not None:
            try:
                country = Countries.objects.get(iso_code=str(iso_code).upper())
            except:
                return JsonResponse('Failed to search iso_code, try again',
                                safe=False, status= status.HTTP_400_BAD_REQUEST)

            manufacturers = manufacturers.filter(countries=country)

        if country_name is not None:
            try:
                country = Countries.objects.get(name__icontains=str(country_name).lower())
            except:
                return JsonResponse('Failed to search country_name, try again',
                                safe=False, status= status.HTTP_400_BAD_REQUEST)

            manufacturers = manufacturers.filter(countries=country)

        if manufacturer is not None:
            try:
                manufacturers = manufacturers.filter(name__icontains=str(manufacturer).lower())
            except:
                return JsonResponse('Failed to search manufacturer, try again',
                                safe=False, status= status.HTTP_400_BAD_REQUEST)

        manufacturers_serializer = ManufacturerSerializer(manufacturers, many=True)

        return JsonResponse(manufacturers_serializer.data, safe=False, status=status.HTTP_200_OK)