from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Label
from .forms import LabelForm

@login_required
def label_list(request):
    labels = Label.objects.all()
    return render(request, 'labels/label_list.html', {'labels': labels})

@login_required
def label_create(request):
    if request.method == 'POST':
        form = LabelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Метка успешно создана')
            return redirect('label_list')
    else:
        form = LabelForm()
    return render(request, 'labels/label_form.html', {'form': form})

@login_required
def label_update(request, pk):
    label = get_object_or_404(Label, pk=pk)
    if request.method == 'POST':
        form = LabelForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            messages.success(request, 'Метка успешно обновлена')
            return redirect('label_list')
    else:
        form = LabelForm(instance=label)
    return render(request, 'labels/label_form.html',
                  {'form': form,
                  'object': object})

@login_required
def label_delete(request, pk):
    label = get_object_or_404(Label, pk=pk)
    if request.method == 'POST':
        # Проверяем связь только при подтверждении удаления
        if label.tasks.exists():
            messages.error(request, 'Невозможно удалить метку, потому что она используется')
            return redirect('label_list')
        else:
            label.delete()
            messages.success(request, 'Метка успешно удалена')
        return redirect('label_list')

        # Для GET-запроса просто показываем страницу подтверждения
    return render(request, 'labels/label_confirm_delete.html', {'label': label})