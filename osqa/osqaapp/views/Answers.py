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
from osqaapp.form import AddAnswer
from osqaapp.models import Question, Answer, ALike


class AnswerView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        q = Question.objects.annotate(likes=Count('qlike')).filter(id=kwargs['pk']).values()
        id=q[0]['id']
        a=Answer.objects.filter(question__id=kwargs['pk']).annotate(likes=Count('alike')).order_by('-likes').values()
        return render(request,"answer_list.html",context={'question':q,'answers':a,'id':id})


class AnswerListView(LoginRequiredMixin, ListView):
            login_url = '/osqa/'
            model =Answer
            context_object_name = 'answers'
            template_name = "useranswers.html"

            def get_object(self, queryset=None):
                return get_object_or_404(self, **self.kwargs)

            def get_context_data(self, **kwargs):
               # ipdb.set_trace()
                context = super(AnswerListView, self).get_context_data(**kwargs)
                q = Question.objects.annotate(likes=Count('qlike')).filter(id=self.kwargs['pk']).values()
                id = q[0]['id']
                a = Answer.objects.filter(question__id=self.kwargs['pk']).annotate(likes=Count('alike')).order_by(
                    '-likes').values()
                context.update(
                    {
                        'question': q, 'answers': a,'id':id,
                        'user_permissions': self.request.user.get_all_permissions()})
                return context

class Addanswers(CreateView):
    form_class = AddAnswer
    template_name = 'add_answer.html'
    def post(self, request, *args, **kwargs):
        card_form = AddAnswer(request.POST)
        if card_form.is_valid():
            card = card_form.save(commit=False)
            card.user = self.request.user
            card.question_id=kwargs['pk']
            card.save()
            return redirect(request.path_info[:-11])
        else:
            return redirect(request.path_info[:-11])


class EditAnswerView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    login_url = '/osqa'
    model=Question
    form_class = AddAnswer
    template_name = 'add_answer.html'
    permission_required = "osqaapp.change_answer"
    permission_denied_message = "user does not have permission to edit this answer"
    raise_exception = True
    def has_permission(self,**kwargs):
        if (self.request.user.id == Answer.objects.filter(id = self.kwargs.get('pk')).values_list('user')[0][0]):
            return True
        return False
  #  ipdb.set_trace()
    success_url = '/osqa/userquestion'
    def get_object(self , queryset=None):
        return get_object_or_404(Question, **self.kwargs)

class DeleteAnswerView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    login_url = '/osqa'
    model = Question
    permission_required = "osqaapp.delete_answer"
    permission_denied_message = "user does not have permission to delete this answer"
    raise_exception = True
    def has_permission(self, **kwargs):
        if (self.request.user.id == Answer.objects.filter(id = self.kwargs.get('pk')).values_list('user')[0][0]):
            return True
        return False
    success_url = '/osqa/questions'


def ALikeCreate(request,pk):
    new_like,created = ALike.objects.get_or_create(user=request.user,answer_id=pk)
    val=Answer.objects.filter(id=new_like.answer.id).values('question_id')
    if not created:
        ALike.objects.filter(id=new_like.id).delete()
    return redirect("/osqa/questions/%d" %val[0]['question_id'])