import datetime

from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Driver, Vehicle, InsuranceApplication
from .serializers import DriverSerializer, VehicleSerializer, InsuranceApplicationSerializer
from .permissions import IsAssistant, IsManager


class BaseModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'uid'

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        uid = self.kwargs[lookup_url_kwarg]

        filter_kwargs = {self.lookup_field: uid}

        obj = get_object_or_404(self.get_queryset(), **filter_kwargs)

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

    def update(self, request, *args, **kwargs):
        
        obj = self.get_object()
        
        # Validating only managers can approve or reject insurance applications
        if request.data.get('status', None) and request.user.groups.filter(name='manager').exists():
            if obj.review_date is None:
                return Response('It cannot be approved or rejected if it has not been reviewed yet, please remove "status" from payload if you are trying to review', status=status.HTTP_400_BAD_REQUEST)
            else:
                obj.status = request.data.get('status')
                if request.data.get('status') == InsuranceApplication.APPROVED:
                    obj.approval_date = datetime.date.today()
                obj.save()
                return Response(self.get_serializer(obj).data, status=status.HTTP_202_ACCEPTED)
    
        if request.data.get('review_date', None):
            if request.user.groups.filter(name='manager').exists() or request.user.groups.filter(name='assistant').exists():
                obj.review_date = request.data.get('review_date')
                obj.save()
                return Response(self.get_serializer(obj).data, status=status.HTTP_202_ACCEPTED)

        return super().update(request, *args, **kwargs)

