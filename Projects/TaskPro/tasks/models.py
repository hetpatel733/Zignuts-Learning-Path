from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = 'Low', 'Low'
        MEDIUM = 'Medium', 'Medium'
        HIGH = 'High', 'High'

    class Status(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        COMPLETED = 'Completed', 'Completed'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
