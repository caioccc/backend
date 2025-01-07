from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class AuthenticationUserTest(APITestCase):
    def test_register_user(self):
        url = reverse('knox_register')
        data = {
            'username': 'testuser',
            'email': 'caio@gmail.com',
            'password': 'Admin123!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user']['username'], 'testuser')
        self.assertEqual(response.data['user']['email'], 'caio@gmail.com')
        self.assertFalse('password' in response.data)

    def test_login_user(self):
        self.test_register_user()
        url = reverse('knox_login')
        data = {
            'username': 'testuser',
            'password': 'Admin123!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], 'testuser')
        self.assertEqual(response.data['token'], response.data['token'])
