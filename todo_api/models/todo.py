from django.db import models
from .user import User


class Todo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    text = models.CharField(max_length=200, blank=False)
    date = models.DateTimeField(auto_created=True, auto_now=True)
