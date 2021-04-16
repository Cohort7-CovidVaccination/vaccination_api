from django.conf.urls import url
from vaccination_app import views

urlpatterns = [
    url(r'^api/countries$', views.country_list),
    #url(r'^api/countries/(?P<pk>[0-9]+)$', views.tutorial_detail)
]