from rest_framework  import serializers

from .models import Driver, Vehicle, InsuranceApplication


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


class InsuranceApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceApplication
        fields = '__all__'
