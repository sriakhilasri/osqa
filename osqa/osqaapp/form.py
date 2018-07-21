from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django import forms

from osqaapp.models import Question, Answer, Qcomment, Acomment


class AddQuestion(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ['id','created','user']
        widgets = {
            'Qname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your question name'}),
            'question': forms.Textarea(attrs={'cols': 100, 'rows': 5,'placeholder': 'Enter your question'}),
        }


class AddAnswer(forms.ModelForm):
    class Meta:
        model = Answer
        exclude = ['id', 'created', 'question','user']
        widgets = {
            'answer': forms.TextInput(attrs={'cols': 100, 'rows': 5, 'placeholder': 'Enter your answer'}),
        }


class AddQcomment(forms.ModelForm):
    class Meta:
        model = Qcomment
        exclude = ['id','question','user']
        widgets = {
            'comment': forms.TextInput(attrs={'cols': 100, 'rows': 2, 'placeholder': 'Enter your comment on question'}),
        }


class AddAcomment(forms.ModelForm):
    class Meta:
        model = Acomment
        exclude = ['id','answer','user']
        widgets = {
            'comment': forms.TextInput(attrs={'cols': 100, 'rows': 2, 'placeholder': 'Enter your comment on answer'}),
        }
