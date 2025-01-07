from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class RegisterUserTest(APITestCase):
    def test_register_user(self):
        url = reverse('knox_register')
        data = {
            'username': 'testuser',
            'email': 'caio@gmail.com',
            'password': 'Admin123!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'caio@gmail.com')
        self.assertFalse('password' in response.data)
