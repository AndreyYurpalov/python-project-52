from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

class UserCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('create')  # URL для регистрации (создания пользователя)
        self.login_url = reverse('login')  # URL для входа
        self.user_list_url = reverse('user_list')  # URL для списка пользователей
        self.user_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
        }

    def test_user_registration(self):
        """
        Тест для регистрации пользователя (Create).
        """
        response = self.client.post(self.register_url, data=self.user_data)
        self.assertEqual(response.status_code, 302)  # Ожидаем редирект после успешной регистрации
        self.assertTrue(User.objects.filter(username='testuser').exists())  # Пользователь должен быть создан
        self.assertRedirects(response, self.login_url)  # Редирект на страницу входа

    def test_user_update(self):
        """
        Тест для обновления данных пользователя (Update).
        """
        # Создаем пользователя для теста
        user = User.objects.create_user(
            username='testuser',
            password='strongpassword123',
            first_name='OldName',
            last_name='OldLastName',
            email='oldemail@example.com'
        )
        self.client.login(username='testuser', password='strongpassword123')  # Авторизуем пользователя

        # Данные для обновления
        update_data = {
            'username': 'updateduser',
            'first_name': 'NewName',
            'last_name': 'NewLastName',
            'email': 'newemail@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        }

        # URL для обновления пользователя
        update_url = reverse('user_update', args=[user.id])

        # Отправляем POST-запрос для обновления данных
        response = self.client.post(update_url, data=update_data)

        # Проверяем, что данные обновились
        self.assertEqual(response.status_code, 302)  # Ожидаем редирект после успешного обновления
        updated_user = User.objects.get(id=user.id)
        self.assertEqual(updated_user.username, 'updateduser')
        self.assertEqual(updated_user.first_name, 'NewName')
        self.assertEqual(updated_user.last_name, 'NewLastName')
        self.assertEqual(updated_user.email, 'newemail@example.com')
        self.assertRedirects(response, self.user_list_url)  # Редирект на список пользователей

    def test_user_delete(self):
        """
        Тест для удаления пользователя (Delete).
        """
        # Создаем пользователя для теста
        user = User.objects.create_user(
            username='testuser',
            password='strongpassword123',
            first_name='Test',
            last_name='User',
            email='testuser@example.com'
        )
        self.client.login(username='testuser', password='strongpassword123')  # Авторизуем пользователя

        # URL для удаления пользователя
        delete_url = reverse('user_delete', args=[user.id])

        # Отправляем POST-запрос для удаления пользователя
        response = self.client.post(delete_url)

        # Проверяем, что пользователь был удален
        self.assertEqual(response.status_code, 302)  # Ожидаем редирект после успешного удаления
        self.assertFalse(User.objects.filter(username='testuser').exists())  # Пользователь не должен существовать
        self.assertRedirects(response, self.user_list_url)  # Редирект на список пользователей

    def test_unauthorized_user_update(self):
        """
        Тест для проверки доступа к обновлению данных для неавторизованных пользователей.
        """
        # Создаем пользователя для теста
        user = User.objects.create_user(
            username='testuser',
            password='strongpassword123',
            first_name='Test',
            last_name='User',
            email='testuser@example.com'
        )

        # URL для обновления пользователя
        update_url = reverse('user_update', args=[user.id])

        # Отправляем POST-запрос без авторизации
        response = self.client.post(update_url)

        # Проверяем, что доступ запрещен (редирект на страницу входа)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_list'))

    def test_unauthorized_user_delete(self):
        """
        Тест для проверки доступа к удалению данных для неавторизованных пользователей.
        """
        # Создаем пользователя для теста
        user = User.objects.create_user(
            username='testuser',
            password='strongpassword123',
            first_name='Test',
            last_name='User',
            email='testuser@example.com'
        )

        # URL для удаления пользователя
        delete_url = reverse('user_delete', args=[user.id])

        # Отправляем POST-запрос без авторизации
        response = self.client.post(delete_url)

        # Проверяем, что доступ запрещен (редирект на страницу входа)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_list'))