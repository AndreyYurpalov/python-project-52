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
            messages.success(request, 'Метка успешно создана!')
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
            messages.success(request, 'Метка успешно обновлена!')
            return redirect('label_list')
    else:
        form = LabelForm(instance=label)
    return render(request, 'labels/label_form.html', {'form': form})

@login_required
def label_delete(request, pk):
    label = get_object_or_404(Label, pk=pk)
    if label.tasks.exists():  # Проверяем, есть ли связанные задачи
        messages.error(request, 'Невозможно удалить метку, связанную с задачами.')
        return redirect('label_list')
    if request.method == 'POST':
        label.delete()
        messages.success(request, 'Метка успешно удалена!')
        return redirect('label_list')
    return render(request, 'labels/label_confirm_delete.html', {'label': label})