from django.conf.urls import url
from vaccination_app import views

urlpatterns = [
    url(r'^api/v1/countries$', views.countries_list),
    url(r'^api/v1/vaccinations$', views.vaccinations),
    url(r'^api/v1/vaccinations/summary$', views.vacc_summary),
    url(r'^api/v1/manufacturers$', views.manufacturers)
]