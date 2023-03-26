import pytest
from taskist_app.models import Task, Subtask
from django.contrib.auth.models import User
from django.test import Client

@pytest.fixture
def user():
    user = User.objects.create(username='testuser', email='testuser@example.com', password='password')
    return user

@pytest.fixture
def task():
    task = Task.objects.create(task_name='testtask',
                               task_descr='test',
                               task_longdescr='test',
                               estimated_time=1,
                               points=1,
                               username=None,
                               group_name_id=1,
                               status=1,
                               done=1)
    return task

@pytest.fixture
def subtask():
    subtask = Subtask.objects.create(subtask=None,
                               task_id=1)
    return subtask