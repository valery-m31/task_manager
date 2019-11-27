from django.contrib import admin
from .models import TaskModel, CommentModel


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'active')
    list_filter = ('created_at', 'active')
    search_fields = ('author__username', 'title')
    date_hierarchy = ('created_at')


admin.site.register(TaskModel, TaskAdmin)
admin.site.register(CommentModel)
