from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import DriverModelViewSet, VehicleModelViewSet, InsuranceApplicationModelViewSet


router = DefaultRouter()
router.register(r'drivers', DriverModelViewSet, basename='drivers')
router.register(r'vehicles', VehicleModelViewSet, basename='vehicles')
router.register(r'insurance-applications', InsuranceApplicationModelViewSet, basename='insurance-applications')


urlpatterns = [
    path('', include(router.urls)),
]
