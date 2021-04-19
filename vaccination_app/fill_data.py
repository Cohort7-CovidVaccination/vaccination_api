from vaccination_app.models import Countries, Vaccination_registries, Manufacturer
from datetime import datetime
import os
import requests
import csv

def Validate_db():
    '''
    Validate the amount of data in the DB

            Parameters:
                    Not requiered

            Returns:
                    Nothing
    '''

    countries = Countries.objects.count()
    vaccination_registries = Vaccination_registries.objects.count()

    if countries == 0:
        print("Database empty, filling country data")
        Fill_countries()

    if vaccination_registries == 0:
        print("Database empty, filling vaccination data")
        Fill_vaccination()

def download_csv(url):
    '''
    Download the csv data from a given URL

            Parameters:
                    url (string): A URL to the csv file

            Returns:
                    data: a list of list with the csv information
    '''

    with requests.Session() as s:
        data_req = s.get(url)

        if data_req.status_code != 200:
            return[]
        data_content = data_req.content.decode('utf-8')
        data = list(csv.reader(data_content.splitlines(), delimiter=','))

    return data

def Fill_countries():
    '''
    Create registries in country table and manufactured relation (many to many),
    after download the data

            Parameters:
                    nothing

            Returns:
                    nothing
    '''

    data_countries = download_csv(os.environ['URL_COUNTRY_DATA'])

    if len(data_countries) == 0:
        print("failed to download country file")
        pass

    for country in data_countries[1::]:

        country_instance = Countries.objects.create(iso_code=country[1], name= country[0],
                                    source_name=country[4] ,  source_website= country[5])
        country_instance.save()

        #Clean labs column and add the country relationship
        labs_cleaned = clean_labs(country[2])
        insert_manufacturer_country(labs_cleaned, country_instance)

def clean_labs(labs):
    '''
    Clean the manufacturer information to return the manufacturers separated

            Parameters:
                    labs: A list of manufacturers

            Returns:
                    labs_cleaned: A list of labs cleaned and ready to save
    '''

    labs_cleaned = []
    labs_separated = labs.split(',')
    for lab in labs_separated:
        lab = lab.replace('/','-').lower().strip()
        labs_cleaned.append(lab)

    return labs_cleaned

def insert_manufacturer_country(labs_cleaned, country):
    '''
    Create the relation into manufacturers (one or many) to the country.

            Parameters:
                    labs_cleaned: A list of manufacturers, ready to be saved
                    country: A country instance of the created country.

            Returns:
                    nothing
    '''

    for lab in labs_cleaned:
        try:
            manufacturer = Manufacturer.objects.get(name=lab)
        except:
            manufacturer = Manufacturer(name=lab)
            manufacturer.save()

        manufacturer.countries.add(country)

def Fill_vaccination():
    '''
    Create registries in vaccination_registries table, after download the data

            Parameters:
                    nothing

            Returns:
                    nothing
    '''

    data_vacc = download_csv(os.environ['URL_VACCINATION_DATA'])

    if len(data_vacc) == 0:
        print("failed to download vaccination file")
        pass

    for vaccination_data in data_vacc[1::]:

        vacc_data_clean = []
        for data in vaccination_data:

            if data == '':
                data = 0
                vacc_data_clean.append(data)
            else:
                vacc_data_clean.append(data)

        vaccination_data = vacc_data_clean
        try:
            Countries.objects.get(iso_code=vaccination_data[1])
        except:
            print("Country or agregated no detected, creating simple country")
            country_instance = Countries.objects.create(iso_code=vaccination_data[1], name= vaccination_data[0])
            country_instance.save()

        vaccination_registry = Vaccination_registries.objects.create(
        country = Countries.objects.get(iso_code=vaccination_data[1]), date_data = datetime.strptime(vaccination_data[2], '%Y-%m-%d'),
        total_vaccinations = vaccination_data[3], people_vaccinated = vaccination_data[4], people_fully_vaccinated = vaccination_data[5], daily_vaccinations_raw = vaccination_data[6],
        daily_vaccinations = vaccination_data[7], total_vaccinations_per_hundred = vaccination_data[8], people_vaccinated_per_hundred = vaccination_data[9],
        people_fully_vaccinated_per_hundred = vaccination_data[10], daily_vaccinations_per_million = vaccination_data[11]
        )
        vaccination_registry.save()

    print("All data stored")