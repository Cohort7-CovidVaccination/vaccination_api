from vaccination_app.models import Countries

def Fill_countries():
    country_instance = Countries.objects.create(iso_code='PER', name= "Peru")
    country_instance.save()