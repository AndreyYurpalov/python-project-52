# statuses/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Status
from .forms import StatusForm

@login_required
def status_list(request):
    statuses = Status.objects.all()
    return render(request, 'statuses/status_list.html', {'statuses': statuses})

@login_required
def status_create(request):
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статус успешно создан')
            return redirect('statuses:list')
    else:
        form = StatusForm()
    return render(request, 'statuses/status_form.html', {'form': form})

@login_required
def status_update(request, pk):
    status = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(request, 'статус успешно обнавлен')
            return redirect('statuses:list')
    else:
        form = StatusForm(instance=status)
    return render(request, 'statuses/status_form.html',
                  {'form': form, 'object': object})


@login_required
def status_delete(request, pk):
    status = get_object_or_404(Status, pk=pk)
    form = StatusForm(request.POST, instance=status)
    if request.method == 'POST':

        # Проверяем, используется ли статус в задачах
        if hasattr(status, 'task_set') and status.task_set.exists():
            return redirect('statuses:list')

        try:
            status.delete()
            messages.success(request, 'Статус успешно удалён')
            return redirect('statuses:list')
        except Exception as e:
            messages.error(
                request,
                f'Невозможно удалить статус, потому что он используется'
            )
            return redirect('statuses:list')

    # Для GET-запроса показываем страницу подтверждения
    is_used = hasattr(status, 'task_set') and status.task_set.exists()
    return render(request, 'statuses/status_confirm_delete.html', {
        'form': form,
        'status': status,
        'is_used': is_used
    })