"""from django import forms
from .models import Task
from labels.models import Label


class TaskForm(forms.ModelForm):
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'assigned_to', 'labels']"""


from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Task
from statuses.models import Status
from .models import User
from labels.models import Label


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].empty_label = _("---------")
        self.fields['executor'].empty_label = _("---------")
        self.fields['labels'].required = False

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'name': _('Имя'),
            'description': _('Описание'),
            'status': _('Статус'),
            'executor': _('Исполнитель'),
            'labels': _('Метки'),
        }
        help_texts = {
            'name': _('Обязательное поле. Не более 150 символов.'),
            'labels': _('Удерживайте Ctrl для выбора нескольких меток'),
        }