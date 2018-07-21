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

from osqaapp.form import AddQuestion
from osqaapp.models import Question, Answer, QLike


class QuestionView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        q=Question.objects.annotate(likes=Count('qlike')).order_by('-likes').values()
        return render(request,"question_list.html",context={'Questions':q})

class QuestionListView(LoginRequiredMixin, ListView):
            login_url = '/osqa/'
            model = Question
            context_object_name = 'Questions'
            template_name = "userquestions.html"
            def get_context_data(self, **kwargs):
                context = super(QuestionListView, self).get_context_data(**kwargs)
                context.update(
                    {
                        'Questions': Question.objects.filter(user=self.request.user).annotate(likes=Count('qlike')).order_by('-likes').values(), 'name': self.request.user.username,
                        'user_permissions': self.request.user.get_all_permissions()})
                return context

class AddQuestions(CreateView):
    form_class = AddQuestion
    template_name = 'add_question.html'
    def post(self, request, *args, **kwargs):
        card_form = AddQuestion(request.POST)
        if card_form.is_valid():
            card = card_form.save(commit=False)
            card.user = self.request.user
            card.save()
            return redirect("/osqa/questions")
        else:
            return redirect("/osqa/questions")


class EditQuestionView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    login_url = '/osqa'
    model=Question
    form_class = AddQuestion
    template_name = 'add_question.html'
    permission_required = "osqaapp.change_question"
    permission_denied_message = "user does not have permission to edit this question"
    raise_exception = True
    def has_permission(self,**kwargs):
        if (self.request.user.id == Question.objects.filter(id = self.kwargs.get('pk')).values_list('user')[0][0]):
            return True
        return False
    success_url = '/osqa/userquestion'
    def get_object(self , queryset=None):
        return get_object_or_404(Question, **self.kwargs)

class DeleteQuestionView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    login_url = '/osqa'
    model = Question
    permission_required = "osqaapp.delete_question"
    permission_denied_message = "user does not have permission to delete this card"
    raise_exception = True
    def has_permission(self, **kwargs):
        if (self.request.user.id == Question.objects.filter(id = self.kwargs.get('pk')).values_list('user')[0][0]):
            return True
        return False
    success_url = '/osqa/userquestions'

def QLikeCreate(request,pk):
    new_like,created = QLike.objects.get_or_create(user=request.user,question_id=pk)
    if not created:
        QLike.objects.filter(id=new_like.id).delete()
    return redirect("/osqa/questions")