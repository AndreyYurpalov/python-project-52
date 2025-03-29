from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Status
from .forms import StatusForm
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/status_list.html'
    context_object_name = 'statuses'

    def get_queryset(self):
        return Status.objects.all().order_by('name')

class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Статус успешно создан'))
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Создание статуса')
        return context

class StstusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    #fields = ['name']
    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Метка успешно изменена'))
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Изменение статуса')
        return context

class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status

    template_name = 'statuses/status_confirm_delete.html'
    success_url = reverse_lazy('statuses:list')
    context_object_name = 'status'


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.tasks.exists():
            messages.error(request, _('Невозможно удалить статус использующийся в задаче'))
            return redirect(self.success_url)

        messages.success(request, _('Статус успешно удален'))
        return super().post(request,*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Удаление статуса')
        context['is_used'] = self.object.tasks.exists()
        return context