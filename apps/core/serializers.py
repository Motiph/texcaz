from rest_framework  import serializers

from .models import Driver, Vehicle, InsuranceApplication


EXTRAS = {
    'created_by': {'default': serializers.CurrentUserDefault()},
    'modified_by': {'default': serializers.CurrentUserDefault()},
}

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'
        extra_kwargs = EXTRAS
        lookup_field = 'uid'


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'
        extra_kwargs = EXTRAS
        lookup_field = 'uid'


class InsuranceApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceApplication
        fields = ('uid', 'created_at', 'updated_at', 'modified_by', 'review_date', 'status', 'created_by', 'modified_by', 'drivers')
        extra_kwargs = EXTRAS
        lookup_field = 'uid'
