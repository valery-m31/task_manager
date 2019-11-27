
from django import forms

from .models import TaskModel, CommentModel


class CreateTaskForm(forms.ModelForm):

    class Meta:
        model = TaskModel
        fields = [
            'title',
            'text',
            'image',
            'deadline_at',
            'slug',
            'people',
            'active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Please add a title. Max: 65 characters',
                'size': 65}),
            'text': forms.Textarea(attrs={
                'cols': 80,
                'rows': 10,
                'placeholder': 'Starting typing your task...'}),
            'slug': forms.TextInput(attrs={
                'placeholder': 'Please add a slug',
                'size': 65}),
            'deadline_at': forms.DateInput(format='%m/%d/%Y', attrs={
                'placeholder':'Input date mm/dd/yyyy'}),
            'people': forms.CheckboxSelectMultiple,
            'active': forms.RadioSelect}


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={
                'placeholder': 'Please enter your comment.'}),
        }
