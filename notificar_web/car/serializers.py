from rest_framework import serializers
from car.models import Car


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'
        # fields = ('id', 'owner', 'car_model', 'color', 'year', 'mileage')