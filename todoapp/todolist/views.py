from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)

    # Фильтрация по статусу
    status_filter = request.GET.get('status')
    if status_filter == 'completed':
        tasks = tasks.filter(completed=True)
    elif status_filter == 'not_completed':
        tasks = tasks.filter(completed=False)

    # Сортировка
    sort_by = request.GET.get('sort_by')
    if sort_by == 'date':
        tasks = tasks.order_by('created_at')
    elif sort_by == 'date_desc':
        tasks = tasks.order_by('-created_at')
    elif sort_by == 'status':
        tasks = tasks.order_by('completed')  # Сначала невыполненные, потом выполненные

    return render(request, 'todolist/task_list.html', {'tasks': tasks})


@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'todolist/add_task.html', {'form': form})

@login_required
def edit_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todolist/edit_task.html', {'form': form})

@login_required
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'todolist/delete_task.html', {'task': task})

@login_required
def mark_completed(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")