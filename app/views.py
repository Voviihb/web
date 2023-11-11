from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from app.models import Question, Answer, Tag
from random import randint


def prepare_tags():
    t = Tag.objects.most_popular()
    colors = ["bg-primary", "bg-secondary", "bg-success", "bg-danger", "bg-warning text-dark", "bg-info text-dark",
              "bg-light text-dark", "bg-dark"]
    res = [{
        'tag': tag["tag"],
        'color': colors[randint(0, 7)]
    } for tag in t]
    return res


def paginate(objects, page, per_page=10):
    paginator = Paginator(objects, per_page)
    return paginator.page(page).object_list


# page -> request


# Create your views here.
def index(request):
    TAGS = prepare_tags()
    QUESTIONS = Question.objects.sort_new().all()
    page = request.GET.get('page', 1)
    try:
        return render(request, 'index.html', {'questions': paginate(QUESTIONS, page), 'tags': TAGS})
    except EmptyPage:
        return render(request, 'index.html', {'questions': paginate(QUESTIONS, 1), 'tags': TAGS})
    except PageNotAnInteger:
        return render(request, 'index.html', {'questions': paginate(QUESTIONS, 1), 'tags': TAGS})


def question(request, question_id):
    TAGS = prepare_tags()
    QUESTIONS = Question.objects.all()
    page = request.GET.get('page', 1)
    try:
        item = QUESTIONS[question_id - 1]
    except IndexError:
        item = QUESTIONS[0]
    answers = Answer.objects.get_answers(question_id)

    try:
        return render(request, 'question.html', {'question': item, 'answers': paginate(answers, page), 'tags': TAGS})
    except EmptyPage:
        return render(request, 'question.html', {'question': item, 'answers': paginate(answers, 1), 'tags': TAGS})
    except PageNotAnInteger:
        return render(request, 'question.html', {'question': item, 'answers': paginate(answers, 1), 'tags': TAGS})


def ask(request):
    TAGS = prepare_tags()
    return render(request, 'ask.html', {'tags': TAGS})


def login(request):
    TAGS = prepare_tags()
    return render(request, 'login.html', {'tags': TAGS})


def signup(request):
    TAGS = prepare_tags()
    return render(request, 'signup.html', {'tags': TAGS})


def settings(request):
    TAGS = prepare_tags()
    return render(request, 'settings.html', {'tags': TAGS})


def hot(request):
    TAGS = prepare_tags()
    QUESTIONS = Question.objects.sort_hot().all()
    page = request.GET.get('page', 1)
    try:
        return render(request, 'hot.html', {'questions': paginate(QUESTIONS, page), 'tags': TAGS})
    except EmptyPage:
        return render(request, 'hot.html', {'questions': paginate(QUESTIONS, 1), 'tags': TAGS})
    except PageNotAnInteger:
        return render(request, 'hot.html', {'questions': paginate(QUESTIONS, 1), 'tags': TAGS})


def tag(request, tag_name):
    TAGS = prepare_tags()
    page = request.GET.get('page', 1)
    res = Tag.objects.get_questions(tag_name)

    try:
        return render(request, 'tag.html', {'tag': tag_name, 'questions': paginate(res, page), 'tags': TAGS})
    except EmptyPage:
        return render(request, 'tag.html', {'questions': paginate(res, 1), 'tags': TAGS})
    except PageNotAnInteger:
        return render(request, 'tag.html', {'questions': paginate(res, 1), 'tags': TAGS})
