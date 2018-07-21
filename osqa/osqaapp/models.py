from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db import models

class Question(models.Model):
    Qname = models.CharField(max_length=254,unique=True)
    created = models.DateField(auto_now_add=True)
    question = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return Question.Qname

class QLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    like=models.IntegerField(default=1)

    def __str__(self):
        return str(self.question_id)


class Qcomment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    comment = models.TextField()

class Answer(models.Model):
    created = models.DateField(auto_now_add=True)
    answer = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class ALike(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    like = models.IntegerField(default=1)
    def __str__(self):
        return str(self.answer_id)

class Acomment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    comment = models.TextField()


