from django.shortcuts import redirect
from django.contrib import messages
from .models import Task, User, Label, Status
from .forms import TaskForm
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset()
        request = self.request

        # Получаем параметры фильтрации
        status_id = request.GET.get('status')
        executor_id = request.GET.get('executor')
        label_id = request.GET.get('label')
        own_tasks = request.GET.get('own_tasks')

        # Применяем фильтры
        if status_id:
            queryset = queryset.filter(status_id=status_id)
        if executor_id:
            queryset = queryset.filter(executor_id=executor_id)
        if label_id:
            queryset = queryset.filter(labels__id=label_id)
        if own_tasks:
            queryset = queryset.filter(author=self.request.user)

        return queryset.distinct().order_by('created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем только используемые в задачах статусы, исполнителей и метки
        context['statuses'] = Status.objects.filter(tasks__isnull=False).distinct()
        context['executors'] = User.objects.filter(executed_tasks__isnull=False).distinct()
        context['labels'] = Label.objects.filter(tasks__isnull=False).distinct()

        # Текущие значения фильтров
        context['current_status'] = self.request.GET.get('status', '')
        context['current_executor'] = self.request.GET.get('executor', '')
        context['current_label'] = self.request.GET.get('label', '')
        context['show_own_tasks'] = bool(self.request.GET.get('own_tasks'))

        context['title'] = _('Список задач')
        return context

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, _('Задача успешно создана'))
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Создание задачи')
        return context

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Задача успешно обновлена'))
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = _('Изменение задачи')
        return context

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks:list')
    context_object_name = 'task'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.author != request.user and not request.user.is_superuser:
            messages.error(request, _('удалять задачу может только автор '))
            return redirect(self.success_url)

        messages.success(request, _('Задача успешно удалена'))
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Удаление задачи')
        return context

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Просмотр задачи')
        return context
