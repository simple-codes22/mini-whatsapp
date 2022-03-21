from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

class Group(models.Model):
    group_id = models.UUIDField(primary_key=True, default=uuid4(), editable=False)
    group_name = models.CharField(max_length=500, unique=True)
    number_of_users = models.PositiveIntegerField(editable=True, default=0)

    def __repr__(self):
        return f'{self.group_name}'

class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid4(), editable=False)
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    content = models.TextField(default='')
    date_time_sent = models.DateTimeField(verbose_name="Time sent", auto_now=True, editable=False)

    def __repr__(self):
        return f"Message sent by {self.from_.username}"
