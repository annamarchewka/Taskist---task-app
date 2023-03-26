from django import forms
from taskist_app.models import POINTS, STATUS
class AddForm(forms.Form):
    task_name = forms.CharField(label="Title", max_length=64, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1}))
    task_descr = forms.CharField(label="Short", max_length=64, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2.5}))
    task_longdescr = forms.CharField(label="Long description", max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    estimated_time = forms.IntegerField(label="Estimated time in hours", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1}))
    status = forms.IntegerField(label='Urgency status', widget=forms.Select(choices=STATUS, attrs={'class': 'form-control', 'rows': 1}))
    points = forms.IntegerField(label="Points", widget=forms.Select(choices=POINTS, attrs={'class': 'form-control', 'rows': 1}))
class SubtaskForm(forms.Form):
    subtask = forms.CharField(label='', max_length=150)
class CommentForm(forms.Form):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
class EditForm(forms.Form):
    estimated_time = forms.IntegerField(label="Estimated time in hours", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1}))
    status = forms.IntegerField(label='Urgency status', widget=forms.Select(choices=STATUS, attrs={'class': 'form-control', 'rows': 1}))
    points = forms.IntegerField(label="Points", widget=forms.Select(choices=POINTS, attrs={'class': 'form-control', 'rows': 1}))
class PhotoForm(forms.Form):
    image = forms.ImageField(label='image')