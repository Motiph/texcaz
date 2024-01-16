from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import Driver, Vehicle, InsuranceApplication
from .serializers import DriverSerializer, VehicleSerializer, InsuranceApplicationSerializer

class BaseModelViewSet(ModelViewSet):
    def get_object(self):
        _id = int(self.kwargs['pk'])
        obj = get_object_or_404(
            self.get_queryset().model, Q(pk=_id)
        )
        self.check_object_permissions(self.request, obj)
        return obj

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.deleted = True
        obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VehicleModelViewSet(BaseModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class DriverModelViewSet(BaseModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer


class InsuranceApplicationModelViewSet(BaseModelViewSet):
    queryset = InsuranceApplication.objects.all()
    serializer_class = InsuranceApplicationSerializer
