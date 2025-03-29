from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Label

class LabelTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.label = Label.objects.create(name='Test Label')

    def test_label_list_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('labels:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Label')

    def test_label_create_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('labels:create'), {
            'name': 'New Label',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='New Label').exists())

    def test_label_update_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('labels:update', args=[self.label.pk]), {
            'name': 'Updated Label',
        })
        self.assertEqual(response.status_code, 302)
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Updated Label')

    def test_label_delete_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('labels:delete', args=[self.label.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())
