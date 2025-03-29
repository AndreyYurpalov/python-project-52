from django.test import TestCase, RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .models import Task, Status, Label
from .forms import TaskForm
from .views import TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView, TaskDetailView


class TaskViewsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.superuser = User.objects.create_superuser(
            username='admin',
            password='adminpass'
        )
        self.status = Status.objects.create(name='Test Status')
        self.label = Label.objects.create(name='Test Label')
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            author=self.user,
            status=self.status
        )
        self.task.labels.add(self.label)

    def setup_request(self, request):
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        return request

    # TaskListView Tests
    def test_task_list_view(self):
        request = self.factory.get(reverse('tasks:list'))
        request = self.setup_request(request)
        response = TaskListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('tasks', response.context_data)

    def test_task_list_filtering(self):
        # Test status filter
        request = self.factory.get(reverse('tasks:list') + f'?status={self.status.id}')
        request = self.setup_request(request)
        response = TaskListView.as_view()(request)
        self.assertEqual(len(response.context_data['tasks']), 1)

        # Test own tasks filter
        request = self.factory.get(reverse('tasks:list') + '?own_tasks=on')
        request = self.setup_request(request)
        response = TaskListView.as_view()(request)
        self.assertEqual(len(response.context_data['tasks']), 1)

        # Test label filter
        request = self.factory.get(reverse('tasks:list') + f'?label={self.label.id}')
        request = self.setup_request(request)
        response = TaskListView.as_view()(request)
        self.assertEqual(len(response.context_data['tasks']), 1)

    # TaskCreateView Tests
    def test_task_create_view_get(self):
        request = self.factory.get(reverse('tasks:create'))
        request = self.setup_request(request)
        response = TaskCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context_data['form'], TaskForm)

    def test_task_create_view_post(self):
        data = {
            'name': 'New Task',
            'description': 'New Description',
            'status': self.status.id,
            'labels': [self.label.id]
        }
        request = self.factory.post(reverse('tasks:create'), data)
        request = self.setup_request(request)
        response = TaskCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(Task.objects.last().author, self.user)

    # TaskUpdateView Tests
    def test_task_update_view_get(self):
        request = self.factory.get(reverse('tasks:update', args=[self.task.pk]))
        request = self.setup_request(request)
        response = TaskUpdateView.as_view()(request, pk=self.task.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['title'], _('Изменение задачи'))

    def test_task_update_view_post(self):
        data = {
            'name': 'Updated Task',
            'description': 'Updated Description',
            'status': self.status.id,
            'labels': [self.label.id]
        }
        request = self.factory.post(
            reverse('tasks:update', args=[self.task.pk]),
            data
        )
        request = self.setup_request(request)
        response = TaskUpdateView.as_view()(request, pk=self.task.pk)
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')

    # TaskDeleteView Tests
    def test_task_delete_view_author(self):
        request = self.factory.post(reverse('tasks:delete', args=[self.task.pk]))
        request = self.setup_request(request)
        response = TaskDeleteView.as_view()(request, pk=self.task.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 0)

    def test_task_delete_view_not_author(self):
        other_user = User.objects.create_user(username='other', password='testpass')
        request = self.factory.post(reverse('tasks:delete', args=[self.task.pk]))
        request.user = other_user
        request = self.setup_request(request)
        response = TaskDeleteView.as_view()(request, pk=self.task.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 1)

    def test_task_delete_view_superuser(self):
        request = self.factory.post(reverse('tasks:delete', args=[self.task.pk]))
        request.user = self.superuser
        request = self.setup_request(request)
        response = TaskDeleteView.as_view()(request, pk=self.task.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 0)

    # TaskDetailView Tests
    def test_task_detail_view(self):
        request = self.factory.get(reverse('tasks:detail', args=[self.task.pk]))
        request = self.setup_request(request)
        response = TaskDetailView.as_view()(request, pk=self.task.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['task'], self.task)

    def test_task_create_sets_author(self):
        data = {
            'name': 'Author Test Task',
            'description': 'Test',
            'status': self.status.id
        }
        request = self.factory.post(reverse('tasks:create'), data)
        request = self.setup_request(request)
        TaskCreateView.as_view()(request)
        task = Task.objects.get(name='Author Test Task')
        self.assertEqual(task.author, self.user)

    def test_delete_view_messages(self):
        request = self.factory.post(reverse('tasks:delete', args=[self.task.pk]))
        request.user = self.superuser
        request = self.setup_request(request)
        TaskDeleteView.as_view()(request, pk=self.task.pk)
        messages = list(request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), _('Задача успешно удалена'))