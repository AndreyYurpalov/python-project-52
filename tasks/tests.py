from django.test import TestCase, RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from tasks.models import Task
from tasks.views import task_list, task_create, task_update, task_delete, task_detail
from statuses.models import Status
from labels.models import Label

User = get_user_model()


class TaskViewsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.status = Status.objects.create(name='Test Status')
        self.label = Label.objects.create(name='Test Label')

        self.task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            status=self.status,
            author=self.user
        )
        self.task.labels.add(self.label)

    def test_task_list_view(self):
        request = self.factory.get(reverse('task_list'))
        request.user = self.user
        response = task_list(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

    def test_task_create_view_get(self):
        request = self.factory.get(reverse('task_create'))
        request.user = self.user
        response = task_create(request)
        self.assertEqual(response.status_code, 200)

    def test_task_create_view_post(self):
        request = self.factory.post(reverse('task_create'), {
            'name': 'New Task',
            'description': 'New Description',
            'status': self.status.id,
            'labels': [self.label.id]
        })
        request.user = self.user

        # Добавляем messages в request
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = task_create(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('task_list'))
        self.assertEqual(Task.objects.count(), 2)

    def test_task_update_view_get(self):
        request = self.factory.get(reverse('task_update', args=[self.task.pk]))
        request.user = self.user
        response = task_update(request, pk=self.task.pk)
        self.assertEqual(response.status_code, 200)

    def test_task_update_view_post(self):
        request = self.factory.post(reverse('task_update', args=[self.task.pk]), {
            'name': 'Updated Task',
            'description': 'Updated Description',
            'status': self.status.id,
            'labels': [self.label.id]
        })
        request.user = self.user

        # Добавляем messages в request
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = task_update(request, pk=self.task.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('task_list'))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')

    def test_task_delete_view_get(self):
        request = self.factory.get(reverse('task_delete', args=[self.task.pk]))
        request.user = self.user
        response = task_delete(request, pk=self.task.pk)
        self.assertEqual(response.status_code, 200)

    def test_task_delete_view_post_author(self):
        request = self.factory.post(reverse('task_delete', args=[self.task.pk]))
        request.user = self.user

        # Добавляем messages в request
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = task_delete(request, pk=self.task.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('task_list'))
        self.assertEqual(Task.objects.count(), 0)

    def test_task_delete_view_post_not_author(self):
        request = self.factory.post(reverse('task_delete', args=[self.task.pk]))
        request.user = self.other_user

        # Добавляем messages в request
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = task_delete(request, pk=self.task.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('task_list'))
        self.assertEqual(Task.objects.count(), 1)  # Задача не удалена

    def test_task_detail_view(self):
        request = self.factory.get(reverse('task_detail', args=[self.task.pk]))
        request.user = self.user
        response = task_detail(request, pk=self.task.pk)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

from django.contrib.messages import get_messages

class TaskMessagesTest(TestCase):
    def setUp(self):
        self.client = TestCase.client_class()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.status = Status.objects.create(name='Test Status')
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            status=self.status,
            author=self.user
        )
        self.client.login(username='testuser', password='testpass123')

    def test_create_task_message(self):
        response = self.client.post(reverse('task_create'), {
            'name': 'New Task',
            'description': 'New Description',
            'status': self.status.id
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), _('Задача успешно создана!'))

    def test_update_task_message(self):
        response = self.client.post(reverse('task_update', args=[self.task.pk]), {
            'name': 'Updated Task',
            'description': 'Updated Description',
            'status': self.status.id
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Задача успешно обновлена!')

    def test_delete_task_message(self):
        response = self.client.post(reverse('task_delete', args=[self.task.pk]))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Задача успешно удалена')

    def test_delete_task_not_author_message(self):
        other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.post(reverse('task_delete', args=[self.task.pk]))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Задачу может удалить только ее автор')