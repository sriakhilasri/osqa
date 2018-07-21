from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count
from django.forms import forms
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.views import View
import ipdb
from osqaapp.form import AddAnswer, AddQcomment, AddAcomment
from osqaapp.models import Question, Answer, ALike, Qcomment, Acomment


class QCommentView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        q = Question.objects.filter(id=kwargs['pk']).values()
        id=q[0]['id']
        a=Qcomment.objects.filter(question__id=kwargs['pk']).values()
        return render(request,"comment_list.html",context={'question':q,'comments':a,'id':id})


class AddQcomments(CreateView):
    form_class = AddQcomment
    template_name = 'add_comment.html'
    def post(self, request, *args, **kwargs):
        card_form = AddQcomment(request.POST)
        if card_form.is_valid():
            card = card_form.save(commit=False)
            card.user = self.request.user
            card.question_id=kwargs['pk']
            card.save()
            return redirect(request.path_info[:-11]+'comments')
        else:
            return redirect(request.path_info[:-11]+'comments')


class ACommentView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        a = Answer.objects.filter(id=kwargs['pk1']).values()
        id=a[0]['id']
        c=Acomment.objects.filter(answer__id=kwargs['pk1']).values()
        return render(request,"commenta_list.html",context={'answer':a,'comments':c,'id':id})


class AddAcomments(CreateView):
    form_class = AddAcomment
    template_name = 'add_comment.html'
    def post(self, request, *args, **kwargs):
        card_form = AddAcomment(request.POST)
        if card_form.is_valid():
            card = card_form.save(commit=False)
            card.user = self.request.user
            card.answer_id=kwargs['pk1']
            card.save()
     #       ipdb.set_trace()
            return redirect(request.path_info[:-12])
        else:
            return redirect(request.path_info[:-12])

