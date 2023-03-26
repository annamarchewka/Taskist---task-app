from django.db import models
from django.contrib.auth.models import User

POINTS = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
]

STATUS = [
    (1, 'important'),
    (2, 'urgent'),
    (3, 'not urgent')
]

class Group(models.Model):
    group_name = models.CharField(max_length=64, null=False)
    city = models.CharField(max_length=64, null=True)

class User_info(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name_surname = models.CharField(max_length=64, null=True)
    group_name = models.ForeignKey(Group, on_delete=models.CASCADE)
    score = models.IntegerField(null=True)

class Task(models.Model):
    task_name = models.CharField(max_length=64, null=False)
    task_descr = models.CharField(max_length=64, null=True)
    task_longdescr = models.CharField(max_length=1000, null=True)
    estimated_time = models.IntegerField(null=True)
    points = models.IntegerField(choices=POINTS, default=1)
    username = models.ForeignKey(User_info, on_delete=models.CASCADE, null=True)
    group_name = models.ForeignKey(Group, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS, default=1)
    done = models.IntegerField(default=1, null=True)


class Comment(models.Model):
    task_name = models.ForeignKey(Task, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, null=True)
    content = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

class Subtask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    subtask = models.CharField(max_length=150, null=True)

class Photo(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(upload_to='photos/')