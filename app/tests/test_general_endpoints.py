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


class PatternCrudUserTest(APITestCase):
    token = None
    user_data = {
        'username': 'testuser',
        'email': 'testuser@gmail.com',
        'password': 'Admin123!'
    }

    def setUp(self):
        url = reverse('knox_register')
        self.client.post(url, self.user_data, format='json')
        url = reverse('knox_login')
        data = {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }
        response_login = self.client.post(url, data, format='json')
        self.user_data = response_login.data['user']
        self.token = response_login.data['token']


class CategoryCrudUserTest(PatternCrudUserTest):
    def test_create_category(self):
        url = reverse('category')
        data = {
            'name': 'test category',
            'user': self.user_data['id']
        }
        print(data)
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'test category')

    def test_list_category(self):
        self.test_create_category()
        url = reverse('category')
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'test category')

    def test_search_by_name_category(self):
        self.test_create_category()
        url = reverse('category') + '?name=test'
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        url = reverse('category') + '?name=undefined'
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_retrieve_category(self):
        self.test_create_category()
        url = reverse('category')
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('category', args=[response.data['results'][0]['id']])
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test category')

    def test_update_category(self):
        self.test_create_category()
        url = reverse('category')
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('category', args=[response.data['results'][0]['id']])
        data = {
            'name': 'updated category',
            'user': self.user_data['id']
        }
        response = self.client.put(url, data, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'updated category')

    def test_delete_category(self):
        self.test_create_category()
        url = reverse('category')
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TaskCrudUserTest(PatternCrudUserTest):

    def create_category(self):
        url = reverse('category')
        data = {
            'name': 'test category',
            'user': self.user_data['id']
        }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        return response.data['id']

    def test_create_task(self):
        category_id = self.create_category()
        url = reverse('task')
        data = {
            'name': 'test task',
            'description': 'test description',
            'category': category_id,
            'user': self.user_data['id']
        }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'test task')
        self.assertEqual(response.data['description'], 'test description')
        self.assertEqual(response.data['category'], category_id)

    def test_pagination_create_12_tasks_and_list(self):
        category_id = self.create_category()
        url = reverse('task')
        for i in range(12):
            data = {
                'name': f'test task {i}',
                'description': f'test description {i}',
                'category': category_id,
                'user': self.user_data['id']
            }
            response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data['name'], f'test task {i}')
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
        response = self.client.get(url + '?page=2', format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_list_task(self):
        self.test_create_task()
        url = reverse('task')
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'test task')
        self.assertEqual(response.data['results'][0]['description'], 'test description')

    def test_search_by_name_task(self):
        self.test_create_task()
        url = reverse('task') + '?name=test'
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        url = reverse('task') + '?name=undefined'
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_retrieve_task(self):
        self.test_create_task()
        url = reverse('task')
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('task', args=[response.data['results'][0]['id']])
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test task')
        self.assertEqual(response.data['description'], 'test description')

    def test_update_task(self):
        self.test_create_task()
        url = reverse('task')
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('task', args=[response.data['results'][0]['id']])
        data = {
            'name': 'updated task',
            'description': 'updated description',
            'user': self.user_data['id'],
        }
        response = self.client.put(url, data, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'updated task')
        self.assertEqual(response.data['description'], 'updated description')

    def test_delete_task(self):
        self.test_create_task()
        url = reverse('task')
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('task', args=[response.data['results'][0]['id']])
        response = self.client.delete(url, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_mark_task_as_done(self):
        self.test_create_task()
        url = reverse('task')
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('task', args=[response.data['results'][0]['id']])
        data = {
            'name': 'test task',
            'status': True,
            'user': self.user_data['id']
        }
        response = self.client.put(url, data, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], True)
        self.assertEqual(response.data['name'], 'test task')


class UserCrudUserTest(PatternCrudUserTest):
    def test_list_user(self):
        url = reverse('user')
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_user(self):
        url = reverse('user')
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('user', args=[response.data[0]['id']])
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')


class SharedTaskUserTest(PatternCrudUserTest):
    def create_category(self):
        url = reverse('category')
        data = {
            'name': 'test category',
            'user': self.user_data['id']
        }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        return response.data['id']

    def create_task(self):
        category_id = self.create_category()
        url = reverse('task')
        data = {
            'name': 'test task',
            'description': 'test description',
            'category': category_id,
            'user': self.user_data['id']
        }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        return response.data['id']

    def test_create_shared_task(self):
        task_id = self.create_task()
        url = reverse('sharedtask')
        data = {
            'task': task_id,
            'user': self.user_data['id']
        }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['task'], task_id)

    def test_list_shared_task(self):
        self.test_create_shared_task()
        url = reverse('sharedtask')
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_delete_shared_task(self):
        self.test_create_shared_task()
        url = reverse('sharedtask')
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('sharedtask', args=[response.data['results'][0]['id']])
        response = self.client.delete(url, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
