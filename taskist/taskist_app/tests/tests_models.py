from taskist_app.models import Task, Subtask
from django.contrib.auth.models import User
import pytest
@pytest.mark.django_db
def test_user_model(user):
    assert len(User.objects.all()) == 1
    assert User.objects.get(username="testuser") == user

@pytest.mark.django_db
def test_task_model(task):
    assert len(Task.objects.all()) == 1
    assert Task.objects.get(task_name="testtask") == task

@pytest.mark.django_db
def test_subtask_model(subtask):
    assert len(Subtask.objects.all()) == 1
    assert Subtask.objects.get(subtask=None) == subtask