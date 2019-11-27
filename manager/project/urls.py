from django.urls import path

from .views import (
    TaskListView,
    CreateTaskFormView,
    task_detail,
    TaskDeleteView,
    TaskUpdate,
    UserTaskViewList,
    ExpiredTaskListView
)


urlpatterns = [
    path('', TaskListView.as_view(), name='home'),
    path('usertasks/', UserTaskViewList.as_view(), name='user-task'),
    path('create-task/', CreateTaskFormView.as_view(), name='create-task'),
    path('expired-tasks/', ExpiredTaskListView.as_view(), name='expired-tasks'),
    path('delete/<str:slug>/', TaskDeleteView.as_view(), name='delete-task'),
    path('detail/<str:slug>/', task_detail, name='task-detail'),
    path('edit/<str:slug>/', TaskUpdate.as_view(), name='update-task-form'),
]
