from datetime import datetime

from django.db import models

from users.models import CustomUser


BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))

class TaskModel(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    text = models.TextField()
    created_at = models.DateField(default=datetime.now)
    deadline_at = models.DateField(blank=True, null=True)
    image = models.ImageField(
        upload_to='images',
        blank=True,
        null=True,
        default='default.png'
    )
    people = models.ManyToManyField(
        CustomUser,
        related_name='coworker',
        blank=True
    )
    slug = models.SlugField(blank=True, null=True, unique=True)
    active = models.BooleanField(default=True, choices=BOOL_CHOICES)

    def __str__(self):
        return self.title


class CommentModel(models.Model):
    task = models.ForeignKey(
        TaskModel,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return '{}-{}'.format(self.task, str(self.author.username))
