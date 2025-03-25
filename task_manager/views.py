from django.views.generic import TemplateView
from django.shortcuts import render

from django.contrib import messages

from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login

def index(request):
    messages.success(request, 'Тестовое сообщение для проверки massage!')
    return render(request, 'index.html', context={
        'who': 'Python-project-52',
    })

class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'

class UserCreateView(CreateView):
    model = User
    # fields = ['username', 'password', 'email', 'date_joined']
    form_class = CustomUserCreationForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('login')


class UserUpdateview(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('user_list')

    def get_queryset(self):
        # Возвращаем всех пользователей, чтобы избежать ошибки 404
        return User.objects.all()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect('user_list')

        # Получаем пользователя, которого пытаются изменить
        user = self.get_object()

        # Проверяем, имеет ли текущий пользователь права на изменение
        if not request.user.is_superuser and request.user.id != user.id:
            messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect('user_list')

        return super().dispatch(request, *args, **kwargs)


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')

    def get_queryset(self):
        # Возвращаем всех пользователей, чтобы избежать ошибки 404
        return User.objects.all()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect('user_list')

        # Получаем пользователя, которого пытаются удалить
        user = self.get_object()

        # Проверяем, имеет ли текущий пользователь права на удаление
        if not request.user.is_superuser and request.user.id != user.id:
            messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect('user_list')

        return super().dispatch(request, *args, **kwargs)


"""class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = False
    next_page = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Вы залогинены.')
        return response"""


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True  # Измените на True для лучшей практики

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        messages.success(self.request, 'Вы успешно вошли в систему!')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        url = self.get_redirect_url()
        return url if url else reverse_lazy('index')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем пользователя
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} успешно создан!')
            return redirect('login')  # Перенаправляем на страницу входа
    else:
        form = CustomUserCreationForm()
    return render(request, 'index.html', {'form': form})


class CustomLogoutView(LogoutView):
    next_page = 'index'  # Перенаправление на главную страницу после выхода

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Вы разлогинены.')
        return super().dispatch(request, *args, **kwargs)
