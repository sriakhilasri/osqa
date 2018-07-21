"""osqa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from osqa import settings
from osqaapp.form import AddQcomment
from osqaapp.views.Answers import AnswerView, ALikeCreate, Addanswers, AnswerListView, EditAnswerView
from osqaapp.views.Question import QuestionView, AddQuestions, QuestionListView, DeleteQuestionView, EditQuestionView, \
    QLikeCreate
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from osqaapp.views.auth import loginview, signupview, logoutpage
from osqaapp.views.comments import QCommentView, AddQcomments, ACommentView, AddAcomments

app_name='osqaapp'



urlpatterns = [
    url(r'^$', loginview.as_view(), name='login'),
    url(r'^signup$', signupview.as_view(), name='signup'),
    url(r'^questions$', QuestionView.as_view(), name='questions'),
    url(r'^userquestion$', QuestionListView.as_view(), name='contributions'),
    url(r'^updatequestion/(?P<pk>[\w-]+)$', EditQuestionView.as_view(), name='updatequestion'),
    url(r'^deletequestion/(?P<pk>[\w-]+)$', DeleteQuestionView.as_view(), name='deletequestion'),
    url(r'^addquestion$', AddQuestions.as_view(), name='addquestion'),
    url(r'^QLike/(?P<pk>[\w-]+)$', QLikeCreate, name='questionlike'),
    url(r'^ALike/(?P<pk>[\w-]+)$', ALikeCreate, name='answerslike'),
    url(r'^questions/(?P<pk>[\w-]+)$', AnswerView.as_view(), name='answers'),
    url(r'^questions/(?P<pk>[\w-]+)/comments$', QCommentView.as_view(), name='comments'),
    url(r'^userquestion/(?P<pk>[\w-]+)$', AnswerListView.as_view(), name='answers'),
    url(r'^userquestion/(?P<pk>[\w-]+)/comments/(?P<pk1>[\w-]+)$', ACommentView.as_view(), name='comments'),
    url(r'^questions/(?P<pk>[\w-]+)/comments/(?P<pk1>[\w-]+)$', ACommentView.as_view(), name='comments'),
    url(r'^questions/(?P<pk>[\w-]+)/comments/(?P<pk1>[\w-]+)/addcomments$', AddAcomments.as_view(), name='addcomments'),
    url(r'^userquestion/(?P<pk>[\w-]+)/comments$', QCommentView.as_view(), name='comments'),
    url(r'^questions/(?P<pk>[\w-]+)/addanswers$', Addanswers.as_view(), name='addanswers'),
    url(r'^questions/(?P<pk>[\w-]+)/editanswers$', EditAnswerView.as_view(), name='editanswers'),
    url(r'^userquestion/(?P<pk>[\w-]+)/addanswers$', Addanswers.as_view(), name='addanswers1'),
    url(r'^questions/(?P<pk>[\w-]+)/addcomments$', AddQcomments.as_view(), name='addcomments'),
    url(r'^logout$', logoutpage, name='logout'),
]