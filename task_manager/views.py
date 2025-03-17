from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def index(request):
    return render(request, 'index.html', context={
        'who': 'Python-project-52',
    })


class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'

class UserCreateView(CreateView):
    model = User
    fields = ['username', 'password', 'email', 'date_joined']
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])  # Хэшируем пароль
        user.save()
        return super().form_valid(form)

class UserUpdateview(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'email']
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')

    def get_queryset(self):
        # Ограничиваем редактирование только своим профилем
        return User.objects.filter(id=self.request.user.id)

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')

    def get_queryset(self):
        # Ограничиваем удаление только своим профилем
        return User.objects.filter(id=self.request.user.id)

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('index')


class CustomLogautView(LogoutView):
    next_page = reverse_lazy('index')

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем пользователя
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} успешно создан!')
            return redirect('login')  # Перенаправляем на страницу входа
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
