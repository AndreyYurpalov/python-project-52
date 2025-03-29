from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from .models import Label
from .forms import LabelForm


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/label_list.html'
    context_object_name = 'labels'

    def get_queryset(self):
        return Label.objects.all().order_by('name')


class LabelCreatedView(LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('labels:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Метка успешно создана'))
        return response

    def get_context_date(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Создание метки')
        return context


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    fields = ['name']
    model_form = LabelForm
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('labels:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Метка успешно обновлена'))
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Изменение метки')
        return context

class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/label_confirm_delete.html'
    success_url = reverse_lazy('labels:list')
    context_object_name = 'label'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.tasks.exists():
            messages.error(request, _('Невозможно изменить связанную с задачей метку'))
            return redirect(self.success_url)

        messages.success(request, _('Метка успешна удалена'))
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('удаление метки')
        context['is_used'] = self.object.tasks.exists()
        return context
