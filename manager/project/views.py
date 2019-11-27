import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from users.models import CustomUser
from .models import TaskModel, CommentModel
from .forms import CreateTaskForm, CommentForm


class TaskListView(LoginRequiredMixin, ListView):
    model = TaskModel
    context_object_name = 'task_list'
    template_name = 'home.html'
    paginate_by = 8

    def get_queryset(self):
        queryset = TaskModel.objects.filter(
            author=CustomUser.objects.get(username=self.request.user.username)
        )
        return queryset.order_by('-created_at')


class UserTaskViewList(LoginRequiredMixin, ListView):
    model = TaskModel
    context_object_name = 'mytasks'
    template_name = 'user_task.html'
    paginate_by = 8

    def get_queryset(self):
        if CustomUser:
            queryset = TaskModel.objects.filter(
                people=CustomUser.objects.get(
                    username=self.request.user.username
                )
            ).filter(active=True)
            return queryset.order_by('-created_at')
        return TaskModel.objects.all().order_by('-created_at')

@login_required
def task_detail(request, slug):
    task = get_object_or_404(TaskModel, slug=slug)
    comments = task.comments.filter(active=True, parent__isnull=True)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            if parent_id:
                parent_obj = CommentModel.objects.get(id=parent_id)
                if parent_obj:
                    replay_comment = comment_form.save(commit=False)
                    replay_comment.parent = parent_obj
            new_comment = comment_form.save(commit=False)
            new_comment.task = task
            new_comment.author = CustomUser.objects.get(
                username=request.user.username
            )
            new_comment.save()
            return HttpResponseRedirect('')
    else:
        comment_form = CommentForm()
    return render(request,
                  'task-detail.html',
                  {'object': task,
                   'comments': comments,
                   'comment_form': comment_form})


class ExpiredTaskListView(LoginRequiredMixin, ListView):
    model = TaskModel
    context_object_name = 'expired_tasks'
    template_name = 'expired_tasks.html'
    paginate_by = 8

    def get_queryset(self):
        queryset = TaskModel.objects.filter(
            Q(author=CustomUser.objects.get(
                username=self.request.user.username))|Q(
                    people=CustomUser.objects.get(
                        username=self.request.user.username))).filter(
                            deadline_at__lte=datetime.date.today()).distinct()
        return queryset


class CreateTaskFormView(LoginRequiredMixin, CreateView):
    def get(self, request):
        form = CreateTaskForm()
        return render(request, 'create_task.html', context={'form': form})

    def post(self, request):
        if request.method == 'POST':
            bound_form = CreateTaskForm(request.POST, request.FILES)
            if bound_form.is_valid():
                new_task = bound_form.save(commit=False)
                new_task.author = CustomUser.objects.get(
                    username=self.request.user.username
                )
                new_task.save()
                bound_form.save_m2m()
                return redirect('home')
            return render(
                request,
                'create_task.html',
                context={'form': bound_form}
            )


class TaskDeleteView(LoginRequiredMixin, View):
    def get(self, request, slug):
        """This method gets one task to delete"""
        task = TaskModel.objects.get(slug__iexact=slug)
        return render(request, 'task_delete_form.html', {'task':task})

    def post(self, request, slug):
        """This method removes the task"""
        task = TaskModel.objects.get(slug__iexact=slug)
        task.delete()
        return redirect('home')


# class DeleteAllTasksView(LoginRequiredMixin, View):
#     def get(self, request, slug):
#         """This method gets all tasks to delete"""
#         task = TaskModel.objects.filter(username=self.request.user.username)
#         return render(request, 'task_delete_all_form.html', {'task':task})
#
#     def post(self, request, slug):
#         """This method removes all tasks"""
#         task = TaskModel.objects.filter(username=self.request.user.username)
#         task.delete()
#         return redirect('home')


class TaskUpdate(LoginRequiredMixin, View):
    def get(self, request, slug):
        """This method gets form for edit task"""
        task = TaskModel.objects.get(slug__iexact=slug)
        print(task)
        bound_form = CreateTaskForm(instance=task)
        return render(
            request,
            'task_update_form.html',
            {'form': bound_form, 'task': task}
        )

    def post(self, request, slug):
        """This method send updated info of the task"""
        task = TaskModel.objects.get(slug__iexact=slug)
        bound_form = CreateTaskForm(request.POST, request.FILES, instance=task)

        if bound_form.is_valid():
            new_task = bound_form.save(commit=False)
            new_task.save()
            return redirect('home')
        return render(
            request,
            'task_update_form.html',
            {'form': bound_form, 'task': task}
        )
