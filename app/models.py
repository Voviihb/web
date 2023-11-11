from django.contrib.auth.models import User
from django.db import models
from django.db.models.functions import Coalesce


# Create your models here.
class QuestionManager(models.Manager):
    def sort_new(self):
        return self.order_by('-created').annotate(cnt=Coalesce(models.Count('answers'), 0))

    def sort_hot(self):
        return self.order_by('-like', '-created').annotate(cnt=Coalesce(models.Count('answers'), 0))


class Question(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0, editable=False)
    tags = models.ManyToManyField('Tag', related_name='questions')
    answers = models.ManyToManyField('Answer', related_name='questions', blank=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    liked_by = models.ManyToManyField(User, related_name='questions', blank=True)

    objects = QuestionManager()

    def __str__(self):
        return f"{self.title}"


class TagManager(models.Manager):
    def most_popular(self):
        return self.values('tag').annotate(total=models.Sum('questions__like')).order_by('-total')[:9]

    def get_questions(self, t):
        t_id = self.get(tag=t)
        # return self.values('questions').filter(questions__tags=t_id)
        return Question.objects.filter(tags=t_id).annotate(cnt=Coalesce(models.Count('answers'), 0))

class Tag(models.Model):
    tag = models.CharField(max_length=30, unique=True)

    objects = TagManager()

    def __str__(self):
        return f"{self.tag}"


class AnswerManager(models.Manager):
    def sort_by_date(self):
        return self.order_by('created')

    def get_answers(self, q_id):
        return self.filter(questions__id=q_id).order_by('created')


class Answer(models.Model):
    correct = models.BooleanField()
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0, editable=False)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    rated_by = models.ManyToManyField(User, related_name='answers', blank=True)

    objects = AnswerManager()

    def __str__(self):
        return f"{self.content}"


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    nickname = models.CharField(max_length=100)
    avatar = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nickname}"
