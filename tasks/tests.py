from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task

class TaskTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.task = Task.objects.create(name='Test Task', description='Test Description', author=self.user)

    def test_task_list_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

    def test_task_create_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('task_create'), {
            'name': 'New Task',
            'description': 'New Description',
            'status': 'todo',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name='New Task').exists())

    def test_task_update_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('task_update', args=[self.task.pk]), {
            'name': 'Updated Task',
            'description': 'Updated Description',
            'status': 'in_progress',
        })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')

    def test_task_delete_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('task_delete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
