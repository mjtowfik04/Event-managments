from django.shortcuts import render, redirect
from django.http import HttpResponse
from events.forms import EventForm, EventModelForm,EventDetailModelForm
from events.models import Participant, Event, EventDetail, Project
from datetime import date
from django.db.models import Q, Count, Max, Min, Avg
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from users.views import is_admin



def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def is_employee(user):
    return user.groups.filter(name='Employee').exists()


# Create your views here.

# @user_passes_test(is_manager, login_url='no-permission')
def manager_dashboard(request):


    type = request.GET.get('type', 'all')


    counts = Event.objects.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(status='COMPLETED')),
        in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
        pending=Count('id', filter=Q(status='PENDING')),
    )

    # Retriving task data

    base_query = Event.objects.select_related(
        'details').prefetch_related('assigned_to')

    if type == 'completed':
        tasks = base_query.filter(status='COMPLETED')
    elif type == 'in-progress':
        tasks = base_query.filter(status='IN_PROGRESS')
    elif type == 'pending':
        tasks = base_query.filter(status='PENDING')
    elif type == 'all':
        tasks = base_query.all()

    context = {
        "tasks": tasks,
        "counts": counts
    }
    return render(request, "dashboard/manager-dashboard.html", context)

# @user_passes_test(is_employee)
def user_dashboard(request):
    type = request.GET.get('type', 'all')


    counts = Event.objects.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(status='COMPLETED')),
        in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
        pending=Count('id', filter=Q(status='PENDING')),
    )

    # Retriving task data

    base_query = Event.objects.select_related(
        'details').prefetch_related('assigned_to')

    if type == 'completed':
        tasks = base_query.filter(status='COMPLETED')
    elif type == 'in-progress':
        tasks = base_query.filter(status='IN_PROGRESS')
    elif type == 'pending':
        tasks = base_query.filter(status='PENDING')
    elif type == 'all':
        tasks = base_query.all()

    context = {
        "tasks": tasks,
        "counts": counts
    }
    # return render(request, "dashboard/manager-dashboard.html", context)
    return render(request, "dashboard/user-dashboard.html",context)

@permission_required("events.add_event", login_url='no-permission')
def create_task(request):
    task_form = EventModelForm()  
    task_detail_form = EventDetailModelForm()

    if request.method == "POST":
        task_form = EventModelForm(request.POST)
        task_detail_form = EventDetailModelForm(request.POST)

        if task_form.is_valid() and task_detail_form.is_valid():

            """ For Model Form Data """
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Created Successfully")
            return redirect('create-task')

    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, "task_form.html", context)


@login_required
@permission_required("events.change_event", login_url='no-permission')
def update_task(request, id):
    task = Event.objects.get(id=id)
    task_form = EventModelForm(instance=task)  

    if task.details:
        task_detail_form = EventDetailModelForm(instance=task.details)

    if request.method == "POST":
        task_form = EventModelForm(request.POST, instance=task)
        task_detail_form = EventDetailModelForm(
            request.POST, instance=task.details)

        if task_form.is_valid() and task_detail_form.is_valid():

            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Updated Successfully")
            return redirect('update-task', id)

    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, "task_form.html", context)


@login_required
@permission_required("events.delete_event", login_url='no-permission')
def delete_task(request, id):
    if request.method == 'POST':
        task = Event.objects.get(id=id)
        task.delete()
        messages.success(request, 'Task Deleted Successfully')
        return redirect('manager-dashboard')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('manager-dashboard')

@login_required

def view_task(request):
    projects =Project.objects.annotate(
        num_task=Count('task')).order_by('num_task')
    return render(request, "show_task.html", {"projects": projects})





@login_required
def dashboard(request):
    if is_manager(request.user):
        return redirect('manager-dashboard')
    elif is_employee(request.user):
        return redirect('user-dashboard')
    elif is_admin(request.user):
        return redirect('admin-dashboard')

    return redirect('no-permission')