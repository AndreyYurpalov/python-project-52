from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import TaskForm

from django.utils.translation import gettext_lazy as _


@login_required
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            form.save_m2m()  # Для сохранения меток
            messages.success(request, _('Задача успешно создана!'))
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(request, 'tasks/task_form.html',
                  {'form': form,
                   'title': _('Создать задачу')})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    #if request.user != task.author:
     #   messages.error(request, 'Вы не можете редактировать эту задачу.')
      #  return redirect('task_create')
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Задача успешно обновлена!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html',
                  {'form': form,
                   'title': _('Изменение задачи'),
                   'object': task})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.user != task.author:
        messages.error(request, 'Задачу может удалить только ее автор')
        return redirect('task_list')
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Задача успешно удалена')
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})