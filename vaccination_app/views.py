from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from vaccination_app.models import Countries, Vaccination_registries
from vaccination_app.serializers import CountrySerializer, VaccRegistriesSerializer
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

        if (iso_code is None and from_date is None and to_date is None):
            return JsonResponse('Please send almost one of the allowed params iso_code, from or to',
                                safe=False, status= status.HTTP_400_BAD_REQUEST)

        if iso_code is not None:
            try:
                country = Countries.objects.get(iso_code=str(iso_code).upper())
            except:
                return JsonResponse('Failed to search iso_code, try again',
                                safe=False, status= status.HTTP_400_BAD_REQUEST)
            vaccinations = Vaccination_registries.objects.filter(country=country)

        if iso_code is None:
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

        if iso_code is not None:
            try:
                country = Countries.objects.get(iso_code=str(iso_code).upper())
            except:
                return JsonResponse('Failed to search iso_code, try again',
                                safe=False, status= status.HTTP_400_BAD_REQUEST)
            vacc_summary = Vaccination_registries.objects.filter(country=country).order_by('-date_data')[0]
        else:
            return JsonResponse('Please send the iso_code param',
                                safe=False, status= status.HTTP_400_BAD_REQUEST)

        registries_serializer = VaccRegistriesSerializer(vacc_summary)

        return JsonResponse(registries_serializer.data, safe=False, status=status.HTTP_200_OK)