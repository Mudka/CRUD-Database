from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Employee

class EmployeeTests(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Obtain JWT token
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'testuser',
            'password': 'testpassword'
        }, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Create test employees
        self.employee1 = Employee.objects.create(name="Test1", department="Test1", workflow=30)
        self.employee2 = Employee.objects.create(name="Test2", department="Test2", workflow=40)

        self.employee_data = {
            'name': 'New Employee',
            'department': 'New Department',
            'workflow': 50
        }

    def test_create_employee(self):
        response = self.client.post(reverse('employee-list'), self.employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('name', response.data['data'])
        self.assertEqual(response.data['data']['name'], self.employee_data['name'])
        self.assertEqual(response.data['data']['workflow'], self.employee_data['workflow'])

    def test_get_employees(self):
        response = self.client.get(reverse('employee-list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 2)  # Ensure both employees are listed

    def test_get_single_employee(self):
        response = self.client.get(reverse('employee-detail', args=[self.employee1.id]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('name', response.data['data'])
        self.assertEqual(response.data['data']['name'], self.employee1.name)
        self.assertEqual(response.data['data']['workflow'], self.employee1.workflow)

    def test_update_employee(self):
        updated_data = {
            'name': 'Updated Employee',
            'department': 'Updated Department',
            'workflow': 60,
        }
        response = self.client.put(reverse('employee-detail', args=[self.employee1.id]), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('name', response.data['data'])
        self.assertEqual(response.data['data']['name'], updated_data['name'])
        self.assertEqual(response.data['data']['workflow'], updated_data['workflow'])

    def test_delete_employee(self):
        response = self.client.delete(reverse('employee-detail', args=[self.employee1.id]), format='json')
        self.assertTrue(response.status_code in [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK])
        self.assertEqual(Employee.objects.count(), 1)  # Ensure one employee is deleted, one remains
