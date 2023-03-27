import pytest
from django.urls import reverse
from django.test import Client
from taskist_app.models import Task
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_login(client, user):
    response = client.get(reverse('login'), {
        'username': 'testuser',
        'password': 'password'
    })
    assert response.status_code == 200
    assert reverse('main')


'''def test_add_view(client):
    user = User.objects.create_user('testuser', password='testpass')
    client.login(username='testuser', password='testpass')
    url = reverse('addtask')
    response = client.get(url)
    assert response.status_code == 200
    assert '<form' in response.content.decode()

    # make a POST request to the add view with form data
    data = {
        'task_name': 'test',
        'points': 1,
        'status': 1,
        'done': 1,
    }
    response = client.post(url, data)

    # check that the response redirects to the detail view
    assert response.status_code == 200
    assert response.url == reverse('main', args=[1])

    # check that the model was saved with the correct data
    obj = MyModel.objects.get(pk=1)
    assert obj.task_name == 'test'
    assert obj.points == 1
    assert obj.status == 1
    assert obj.done == 1'''