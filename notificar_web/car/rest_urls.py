from django.conf.urls import url, include
from . import rest_views

urlpatterns = [
    url(r'^v1/car$', rest_views.CarRestV1.as_view(), name='car_rest'),
]