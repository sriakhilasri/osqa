from django.views import View
from django.shortcuts import *
from django.views.generic import ListView,DetailView,CreateView,DeleteView,UpdateView
from django import forms
from django.urls import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages


class SignUpForm(forms.Form):
    first_name = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name ' ,'style': 'border-color: blue;'})
    )

    last_name = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name '})
    )

    username = forms.CharField(
        max_length = 15,
        required=True,
        widget =forms.TextInput(attrs={'class':'form-control','placeholder':'User Name'})
    )

    password = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'})
    )


class signupview(View):
    def get(self,request):
        form=SignUpForm()
        return render(request,template_name="signup.html",context={'form':form})
    def post(self,request):
        form=SignUpForm(request.POST)
        if form.is_valid():
            user=User.objects.create_user(**form.cleaned_data)
            user=authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request,user)
                return redirect("/osqa/questions")
            else:
                messages.error(request,'Invalid data')

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length = 15,
        required=True,
        widget =forms.TextInput(attrs={'class':'form-control','placeholder':'User Name','style': 'border-color: red;'})
    )

    password = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password','style': 'border-color: red;'})
    )


class loginview(View):
    def get(self,request):
        form=LoginForm()
        return render(request,template_name="login.html",context={'form':form})
    def post(self,request):
        form=LoginForm(request.POST)
        if form.is_valid():
            user=authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request,user)
                return redirect("/osqa/questions")
            else:
                messages.error(request,'Invalid data')


def logoutpage(request):
    logout(request)
    return redirect("/osqa")
