from django.contrib import admin

from .models import Driver, Vehicle, InsuranceApplication

admin.site.register(Driver)
admin.site.register(Vehicle)
admin.site.register(InsuranceApplication)
