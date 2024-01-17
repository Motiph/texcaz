from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.core.models import Driver, Vehicle


class TestInsuranceApplication(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='admin1', password='beastMaster1', is_staff=True, is_superuser=True)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        self.manager_group = Group.objects.create(name='manager')
        self.assistant_group = Group.objects.create(name='assistant')

        self.manager = get_user_model().objects.create(username='manager', password='beastMaster1')
        self.manager_token = Token.objects.create(user=self.manager)
        
        self.assistant = get_user_model().objects.create(username='assistant', password='beastMaster1', is_staff=False, is_superuser=True)
        self.assistant_token = Token.objects.create(user=self.assistant)

        self.manager_group.user_set.add(self.manager)
        self.assistant_group.user_set.add(self.assistant)

        self.driver1 = Driver.objects.create(
            name='Edwin Gutiérrez',
            email='mtph@gmail.com',
            address='Tijuana BC, Peral',
            created_by=self.user,
            modified_by=self.user  
        )
        
        self.driver2 = Driver.objects.create(
            name='Francisco González',
            email='fco.gonzalez@gmail.com',
            address='Ciudad Juárez, Chih., Blvd. Insurgentes',
            created_by=self.user,
            modified_by=self.user  
        )
        
        self.vehicle1 = Vehicle.objects.create(
            brand='Toyota',
            serial_number='123456789',
            model='Camry',
            driver=self.driver1,
            created_by=self.user,
            modified_by=self.user  
        )
        
        self.vehicle2 = Vehicle.objects.create(
            brand='Ford',
            serial_number='987654321',
            model='F-150',
            driver=self.driver2,
            created_by=self.user,
            modified_by=self.user  
        )

        self.url = '/api/v1/insurance-applications/'

        return super().setUp()

    def test_all_users_can_submit_insurance_application(self):
        payload = {
            'drivers': [self.driver1.id, self.driver2.id]
        }
    
        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, 201)
        
        # manager token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.manager_token.key}')

        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, 201)

        # assistant token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.assistant_token.key}')

        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, 201)
    
    def test_manager_and_assistant_can_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.manager_token.key}')
        
        payload = {
            'drivers': [self.driver1.id, self.driver2.id]
        }
        
        response = self.client.post(self.url, payload, format='json')

        pk = response.json()['uid']

        self.assertEqual(response.status_code, 201)
        
        payload = {
            'review_date': '2024-10-10'
        }
        
        response = self.client.patch(f'{self.url}{pk}/', payload, format='json')

        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.json()['review_date'], '2024-10-10')
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.assistant_token.key}')
        
        payload = {
            'review_date': '2024-11-11'
        }
        
        response = self.client.patch(f'{self.url}{pk}/', payload, format='json')

        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.json()['review_date'], '2024-11-11')
    
    def test_manager_can_approve_reject(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.manager_token.key}')

        payload = {
            'drivers': [self.driver1.id, self.driver2.id]
        }
    
        response = self.client.post(self.url, payload, format='json')

        pk = response.json()['uid']

        self.assertEqual(response.status_code, 201)
        
        payload = {
            'review_date': '2024-10-10'
        }

        response = self.client.patch(f'{self.url}{pk}/', payload, format='json')

        self.assertEqual(response.status_code, 202)
        
        payload = {
            'status': 'APPROVED'
        }

        response = self.client.patch(f'{self.url}{pk}/', payload, format='json')
        
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.json()['status'], 'APPROVED')
