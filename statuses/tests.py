# statuses/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Status

class StatusCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.status = Status.objects.create(name='Test Status')

    def test_status_list_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('statuses:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Status')

    def test_status_create_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('statuses:create'), {'name': 'New Status'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='New Status').exists())

    def test_status_update_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('statuses:update', args=[self.status.id]), {'name': 'Updated Status'})
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Status')

    def test_status_delete_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('statuses:delete', args=[self.status.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(id=self.status.id).exists())
