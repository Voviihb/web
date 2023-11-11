from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Question(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    like = models.ForeignKey('QuestionLikes', on_delete=models.PROTECT)
    tags = models.ManyToManyField('Tag', related_name='questions')
    answers = models.ManyToManyField('Answer', related_name='questions')


class Tag(models.Model):
    tag = models.CharField(max_length=30)


class QuestionLikes(models.Model):
    likes = models.IntegerField()


class Answer(models.Model):
    correct = models.BooleanField()
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    like = models.ForeignKey('AnswerLikes', on_delete=models.PROTECT)


class AnswerLikes(models.Model):
    likes = models.IntegerField()


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    nickname = models.CharField(max_length=100)
    avatar = models.TextField()
