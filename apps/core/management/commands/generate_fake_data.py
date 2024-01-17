from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from django.core.management.base import BaseCommand

from apps.core.models import Driver, Vehicle, InsuranceApplication



GROUPS = ["manager", "assistant"]

USERS = [
    {
        "username": "admin",
        "email": "admin@site.com",
        "is_staff": True,
        "is_active": True,
        "is_superuser": True,
    },
    {
        "username": "manager1",
        "email": "manager1@site.com",
        "is_staff": False,
        "is_active": True,
        "is_superuser": False,
        "group": "manager"
    },
    {
        "username": "assistant1",
        "email": "assistant1@site.com",
        "is_staff": False,
        "is_active": True,
        "is_superuser": False,
        "group": "assistant"
    },
    {
        "username": "normal1",
        "email": "normal1@site.com",
        "is_staff": False,
        "is_active": True,
        "is_superuser": False,
    }
]

DRIVERS = [
  {
    "name": "Edwin Gutiérrez",
    "email": "mtph@gmail.com",
    "address": "Tijuana BC, Peral"
  },
  {
    "name": "Claudia Ramírez",
    "email": "cramirez@yahoo.com",
    "address": "Ciudad de México, Av. Colón"
  },
  {
    "name": "Alejandro Torres",
    "email": "ale.torres@hotmail.com",
    "address": "Guadalajara, Jalisco, Calle Reforma"
  },
  {
    "name": "Valeria Mendoza",
    "email": "val.mendoza@gmail.com",
    "address": "Monterrey, Nuevo León, Blvd. Independencia"
  },
  {
    "name": "Roberto Vargas",
    "email": "ro.vargas@gmail.com",
    "address": "Querétaro, Qro., Calle Allende"
  },
  {
    "name": "Laura Pérez",
    "email": "laura.perez@gmail.com",
    "address": "Puebla, Pue., Av. Juárez"
  },
  {
    "name": "Juan Castro",
    "email": "juan.castro@yahoo.com",
    "address": "Cancún, QR, Calle Caribe"
  },
  {
    "name": "María Fernández",
    "email": "mafer_25@hotmail.com",
    "address": "Mérida, Yucatán, Calle Montejo"
  },
  {
    "name": "Francisco González",
    "email": "fco.gonzalez@gmail.com",
    "address": "Ciudad Juárez, Chih., Blvd. Insurgentes"
  },
  {
    "name": "Gabriela Sánchez",
    "email": "gabriela.sanchez@yahoo.com",
    "address": "Ensenada BC, Playa Azul"
  }
]

VEHICLES = [
  {
    "brand": "Toyota",
    "serial_number": "123456789",
    "model": "Camry",
    "driver": "mtph@gmail.com"
  },
  {
    "brand": "Ford",
    "serial_number": "987654321",
    "model": "F-150",
    "driver": "cramirez@yahoo.com"
  },
  {
    "brand": "Honda",
    "serial_number": "456789012",
    "model": "Civic",
    "driver": "ale.torres@hotmail.com"
  },
  {
    "brand": "Chevrolet",
    "serial_number": "789012345",
    "model": "Silverado",
    "driver": "val.mendoza@gmail.com"
  },
  {
    "brand": "Nissan",
    "serial_number": "543210987",
    "model": "Altima",
    "driver": "ro.vargas@gmail.com"
  },
  {
    "brand": "BMW",
    "serial_number": "210987654",
    "model": "X5",
    "driver": "laura.perez@gmail.com"
  },
  {
    "brand": "Mercedes-Benz",
    "serial_number": "876543210",
    "model": "E-Class",
    "driver": "juan.castro@yahoo.com"
  },
  {
    "brand": "Audi",
    "serial_number": "321098765",
    "model": "A4",
    "driver": "mafer_25@hotmail.com"
  },
  {
    "brand": "Hyundai",
    "serial_number": "654321098",
    "model": "Santa Fe",
    "driver": "fco.gonzalez@gmail.com"
  },
  {
    "brand": "Kia",
    "serial_number": "234567890",
    "model": "Optima",
    "driver": "gabriela.sanchez@yahoo.com"
  }
]


class Command(BaseCommand):

    def handle(self, *args, **options):
        
        # Groups/Roles
        for group_name in GROUPS:
            try:
                Group.objects.get_or_create(name=group_name)
            except Exception as _:
                print(_)
        
        for u in USERS:
            try:
                user, _ = get_user_model().objects.update_or_create(
                    email=u['email'],
                    username=u['username'],
                    is_staff=u['is_staff'],
                    is_active=u['is_active'],
                    is_superuser=u['is_superuser'],
                )
                
                user.set_password('beastMaster123')
                user.save()
                
                if u['group']:
                    my_group = Group.objects.get(name=u['group']) 
                    my_group.user_set.add(user)
            except Exception as _:
                print(_)

        for d in DRIVERS:
            user = get_user_model().objects.get(username='admin')
            try:
                driver, _ = Driver.objects.get_or_create(
                    email=d['email'],
                    defaults={
                        "name": d['name'],
                        "address": d['address'],
                        "created_by": user,
                        "modified_by": user,    
                    }
                )
            except Exception as _:
                print(_)
                

        for v in VEHICLES:
            user = get_user_model().objects.get(username='admin')
            try:
                driver = Driver.objects.get(email=v['driver'])
                vehicle, _ = Vehicle.objects.get_or_create(
                    serial_number=v['serial_number'],
                    defaults={
                        "brand": v['brand'],
                        "model": v['model'],
                        "driver": driver,
                        "created_by": user,
                        "modified_by": user,
                    }
                )
                vehicle.save()
            except Exception as _:
                print(_)
        
        print('Done!')