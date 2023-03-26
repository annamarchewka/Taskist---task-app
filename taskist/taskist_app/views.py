from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User_info, Task, Subtask, Comment
from .forms import SubtaskForm, CommentForm, AddForm, EditForm, PhotoForm



class LoginFormView(LoginView):
    template_name = 'login.html'
    success_url = 'main/'
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            return redirect('login')

def logout_view(request):
    logout(request)
    return redirect('login')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})

class MainView(View):
    def get(self, request):
        user = request.user
        profile = User_info.objects.get(pk=user)
        members = User_info.objects.all()
        gn = profile.group_name
        g = gn.group_name
        return render(request, "main.html", {"members": members, "group_name": g})

class TaskView(View):
    def get(self, request, usernameid):
        mytasks = Task.objects.filter(username_id=usernameid).filter(done=1)
        freetasks = Task.objects.filter(username_id__isnull=True).filter(done=1)
        takentasks = Task.objects.filter(username_id__gt=usernameid).filter(username_id__gte=usernameid).filter(done=1)
        return render(request, 'tasks.html', {'mytasks': mytasks, 'freetasks': freetasks, 'takentasks': takentasks})
    def post(self, request, usernameid):
        if 'task_id' in request.POST:
            task_id = request.POST.get('task_id')
            task = Task.objects.get(pk=task_id)
            task.username_id = usernameid
            task.save()
            points = task.points
            user = User_info.objects.get(username_id=usernameid)
            user.score = user.score + points
            user.save()
            return redirect("tasks", usernameid=usernameid)
        elif 'mytask_id' in request.POST:
            mytask_id = request.POST.get('mytask_id')
            mytask = Task.objects.get(pk=mytask_id)
            mytask.username_id = None
            mytask.save()
            points = mytask.points
            user = User_info.objects.get(username_id=usernameid)
            user.score = user.score - points
            user.save()
            return redirect("tasks", usernameid=usernameid)
        elif 'othertask_id' in request.POST:
            othertask_id = request.POST.get('othertask_id')
            othertask = Task.objects.get(pk=othertask_id)
            a = othertask.username_id
            return redirect("profile", usernameid=a)
        elif 'done_id' in request.POST:
            done_id = request.POST.get('done_id')
            donetask = Task.objects.get(pk=done_id)
            donetask.done = 0
            donetask.save()
            a = donetask.username_id
            points = donetask.points
            user = User_info.objects.get(username_id=usernameid)
            user.score = user.score - points
            user.save()
            return redirect("tasks", usernameid=a)

class TaskDetailView(View):
    def get(self, request, id):
        task = Task.objects.get(pk=id)
        subtask1 = Subtask.objects.filter(task_id=id)
        subtask = subtask1.order_by('id')
        form = SubtaskForm()
        comments1 = Comment.objects.filter(task_name_id=id)
        comments = comments1.order_by('-id')
        sec_form = CommentForm()
        return render(request, 'taskdetail.html', {'task': task, 'subtask': subtask, 'form': form, 'comments': comments, 'sec_form': sec_form})
    def post(self, request, id):
        if 'first' in request.POST:
            form = SubtaskForm(request.POST)
            if form.is_valid():
                newsubtask = form.cleaned_data['subtask']
                new = Subtask.objects.create(task_id=id, subtask=newsubtask)
                return redirect("taskdetail", id=id)
            else:
                HttpResponse("Incorrect value!")
            return redirect("taskdetail", id=id)
        elif 'delsubtask' in request.POST:
            delsubtask = request.POST.get('delsubtask')
            subtodel = Subtask.objects.filter(pk=delsubtask)
            subtodel.delete()
            return redirect("taskdetail", id=id)
        elif 'deltask' in request.POST:
            deltask = request.POST.get('deltask')
            deletet = Task.objects.get(pk=deltask)
            deletet.delete()
            user = request.user.id
            points = deletet.points
            u = deletet.username_id
            if u == None:
                pass
            else:
                user2 = User_info.objects.get(username_id=u)
                user2.score = user2.score - points
                user2.save()
            return redirect("tasks", usernameid=user)
        elif 'com' in request.POST:
            sec_form = CommentForm(request.POST)
            if sec_form.is_valid():
                newcom = sec_form.cleaned_data['content']
                newc = Comment.objects.create(task_name_id=id, username=request.user, content=newcom)
                return redirect("taskdetail", id=id)
            else:
                HttpResponse("Incorrect value!")
        elif 'delcom' in request.POST:
            delcom = request.POST.get('delcom')
            delc = Comment.objects.filter(pk=delcom)
            delc.delete()
            return redirect("taskdetail", id=id)
        elif 'edit' in request.POST:
            edittask = request.POST.get('edit')
            return redirect("edit", id=edittask)

class EditView(View):
    def get(self, request, id):
        task = Task.objects.get(pk=id)
        form = EditForm()
        return render(request, 'edit_form.html', {"form": form, 'task': task})
    def post(self, request, id):
        if 'edittask' in request.POST:
            form = EditForm(request.POST)
            if form.is_valid():
                task = Task.objects.get(pk=id)
                new_estimated_time = form.cleaned_data['estimated_time']
                new_points = form.cleaned_data['points']
                new_status = form.cleaned_data['status']
                task.estimated_time = new_estimated_time
                task.points = new_points
                task.status = new_status
                task.save()
                return redirect("taskdetail", id=id)
            else:
                return HttpResponse("Incorrect values. Check again")


class AddTaskView(View):
    def get(self, request):
        all = Task.objects.all()
        form = AddForm()
        return render(request, 'addtask_form.html', {"form": form, 'all': all})
    def post(self, request):
        if 'addtask' in request.POST:
            form = AddForm(request.POST)
            if form.is_valid():
                task_name = form.cleaned_data['task_name']
                task_descr = form.cleaned_data['task_descr']
                task_longdescr = form.cleaned_data['task_longdescr']
                estimated_time = form.cleaned_data['estimated_time']
                points = form.cleaned_data['points']
                status = form.cleaned_data['status']
                usernameid = request.user.id
                new = Task.objects.create(task_name=task_name, task_descr=task_descr, estimated_time=estimated_time, points=points, group_name_id=1, status=status, task_longdescr=task_longdescr)
                return redirect("tasks", usernameid=usernameid)
            else:
                return HttpResponse("Incorrect values. Check again")


class ProfileView(View):
 def get(self, request, usernameid):
     profile = User_info.objects.get(pk=usernameid)
     tasks = Task.objects.filter(done=1).filter(username_id=usernameid)
     histtasks = Task.objects.filter(username_id=usernameid).filter(done=0)
     score = profile.score
     return render(request, 'profile.html', {'profile': profile, 'tasks': tasks, 'score': score, 'histtasks': histtasks})


class ScoreView(View):
    def get(self, request, usernameid):
        user = User_info.objects.all()
        users = user.order_by('-score')
        tasks = Task.objects.filter(done=1)
        points = []
        for i in users:
            score = i.score
            points.append(score)
            takenscore = sum(points)
        points2 = []
        for j in tasks:
            score2 = j.points
            points2.append(score2)
            alltaskscore = sum(points2)
        freescore = alltaskscore-takenscore
        return render(request, 'score.html', {'users': users, 'takenscore': takenscore, 'alltaskscore': alltaskscore, 'freescore':freescore})
    def post(self, request):
        pass


def upload_photo(request):
    if request.method == 'POST':
        img_form = PhotoForm(request.POST, request.FILES)
        if img_form.is_valid():
            img_form.save()
            return redirect('settings')
    else:
        img_form = PhotoForm()
    return render(request, 'change_password.html', {'img_form': img_form})