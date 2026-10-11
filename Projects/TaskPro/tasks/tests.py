from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Task

User = get_user_model()

class UserRegistrationTests(APITestCase):
    def test_register_user(self):
        url = reverse('register')
        data = {'username': 'testuser', 'password': 'strongpass123', 'password2': 'strongpass123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_password_mismatch(self):
        url = reverse('register')
        data = {'username': 'testuser', 'password': 'pass1', 'password2': 'pass2'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class JWTAuthTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='jwtuser', password='jwtpass123')

    def test_obtain_token(self):
        url = reverse('token_obtain_pair')
        data = {'username': 'jwtuser', 'password': 'jwtpass123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.access_token = response.data['access']

    def test_protected_endpoint_requires_auth(self):
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_with_token(self):
        token_url = reverse('token_obtain_pair')
        token_resp = self.client.post(token_url, {'username': 'jwtuser', 'password': 'jwtpass123'}, format='json')
        token = token_resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TaskAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass12345')
        self.user2 = User.objects.create_user(username='user2', password='pass12345')
        token_url = reverse('token_obtain_pair')
        token1 = self.client.post(token_url, {'username': 'user1', 'password': 'pass12345'}, format='json').data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token1)

    def test_create_task(self):
        url = reverse('task-list')
        data = {
            'title': 'Test Task',
            'description': 'Task description',
            'due_date': '2030-01-01',
            'priority': 'Medium',
            'status': 'Pending'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.filter(user=self.user1).count(), 1)

    def test_user_sees_own_tasks_only(self):
        Task.objects.create(user=self.user1, title='U1', description='d', due_date='2030-01-01')
        Task.objects.create(user=self.user2, title='U2', description='d', due_date='2030-01-01')
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'U1')

    def test_update_task(self):
        task = Task.objects.create(user=self.user1, title='Old', description='d', due_date='2030-01-01')
        url = reverse('task-detail', args=[task.id])
        data = {'title': 'New', 'description': 'd', 'due_date': '2030-01-01', 'priority': 'High', 'status': 'Completed'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, 'New')
        self.assertEqual(task.priority, 'High')
        self.assertEqual(task.status, 'Completed')

    def test_delete_task(self):
        task = Task.objects.create(user=self.user1, title='Del', description='d', due_date='2030-01-01')
        url = reverse('task-detail', args=[task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_cannot_access_others_task(self):
        task = Task.objects.create(user=self.user2, title='Other', description='d', due_date='2030-01-01')
        url = reverse('task-detail', args=[task.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_filtering_and_search(self):
        Task.objects.create(user=self.user1, title='Alpha', description='d', due_date='2030-01-01', priority='Low', status='Pending')
        Task.objects.create(user=self.user1, title='Beta', description='d', due_date='2030-02-01', priority='High', status='Completed')
        resp = self.client.get(reverse('task-list') + '?status=Pending')
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['title'], 'Alpha')
        resp = self.client.get(reverse('task-list') + '?search=Beta')
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['title'], 'Beta')
        resp = self.client.get(reverse('task-list') + '?ordering=-due_date')
        self.assertEqual(resp.data[0]['title'], 'Beta')
