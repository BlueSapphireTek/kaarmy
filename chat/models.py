from django.db import models
from django.contrib.auth import get_user_model
from byhand.models import *

# Create your models here.


class Message(models.Model):
    sender = models.ForeignKey(CustomUser,on_delete = models.CASCADE, related_name="sent_message")
    receiver = models.ForeignKey(CustomUser,on_delete = models.CASCADE, related_name="recieve_message")
    message = models.TextField()
    files = models.FileField(upload_to='chat',null=True,blank=True)
    sender_delete = models.BooleanField(default=False)
    receiver_delete = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("date_created",)
class Group(models.Model):
    name = models.CharField(max_length=60)
    icon = models.ImageField(upload_to='groupicon')
    date_created = models.DateTimeField(auto_now_add=True)
class GroupMembers(models.Model):
    group = models.ForeignKey(Group,on_delete = models.CASCADE,)
    member = models.ForeignKey(CustomUser,on_delete = models.CASCADE,)
    admin = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
class GroupMessage(models.Model):
    group = models.ForeignKey(Group,on_delete = models.CASCADE,)
    member = models.ForeignKey(CustomUser,on_delete = models.CASCADE,)
    chat = models.CharField(max_length=50000)
    files = models.FileField(upload_to='chat',null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
class GroupSeen(models.Model):
    message = models.ForeignKey(GroupMessage,on_delete = models.CASCADE,)
    member = models.ForeignKey(CustomUser,on_delete = models.CASCADE,)
    group = models.ForeignKey(Group,on_delete = models.CASCADE,)
    seen = models.BooleanField(default=False)

