from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from app.models import Question, Answer, Tag
from random import randint
import time


def prepare_tags():
    t = Tag.objects.most_popular()
    colors = ["bg-primary", "bg-secondary", "bg-success", "bg-danger", "bg-warning text-dark", "bg-info text-dark",
              "bg-light text-dark", "bg-dark"]
    res = [{
        'tag': tag["tag"],
        'color': colors[randint(0, 7)]
    } for tag in t]
    return res


TAGS = prepare_tags()
print("PREPARE")


def paginate(objects, page, per_page=10):
    paginator = Paginator(objects, per_page)
    total_pages = paginator.num_pages
    return paginator.page(page).object_list, total_pages


# page -> request


# Create your views here.
def not_found(request):
    return render(request, '404.html')


def index(request):
    # TAGS = prepare_tags()
    QUESTIONS = Question.objects.sort_new()
    page = request.GET.get('page', 1)

    try:
        if int(page) < 1:
            page = 1
    except ValueError:
        page = 1
    try:
        data, total_pages = paginate(QUESTIONS, page)
        return render(request, 'index.html', {'questions': data,
                                              'tags': TAGS, 'page_num': int(page), 'total_pages': int(total_pages)})
    except EmptyPage:
        return not_found(request)


def question(request, question_id):
    # TAGS = prepare_tags()
    QUESTIONS = Question.objects.all()
    page = request.GET.get('page', 1)
    try:
        if int(page) < 1:
            page = 1
    except ValueError:
        page = 1

    try:
        item = QUESTIONS[question_id - 1]
    except IndexError:
        item = QUESTIONS[0]
    answers = Answer.objects.get_answers(question_id)

    try:
        data, total_pages = paginate(answers, page)
        return render(request, 'question.html',
                      {'question': item, 'answers': data, 'tags': TAGS, 'page_num': int(page),
                       'total_pages': int(total_pages)})
    except EmptyPage:
        return not_found(request)


def ask(request):
    # TAGS = prepare_tags()
    return render(request, 'ask.html', {'tags': TAGS})


def login(request):
    # TAGS = prepare_tags()
    return render(request, 'login.html', {'tags': TAGS})


def signup(request):
    # TAGS = prepare_tags()
    return render(request, 'signup.html', {'tags': TAGS})


def settings(request):
    # TAGS = prepare_tags()
    return render(request, 'settings.html', {'tags': TAGS})


def hot(request):
    # TAGS = prepare_tags()
    QUESTIONS = Question.objects.sort_hot()
    page = request.GET.get('page', 1)
    try:
        if int(page) < 1:
            page = 1
    except ValueError:
        page = 1

    try:
        data, total_pages = paginate(QUESTIONS, page)
        return render(request, 'hot.html', {'questions': data,
                                            'tags': TAGS, 'page_num': int(page), 'total_pages': int(total_pages)})
    except EmptyPage:
        return not_found(request)


def tag(request, tag_name):
    # TAGS = prepare_tags()
    page = request.GET.get('page', 1)
    res = Tag.objects.get_questions(tag_name)
    try:
        if int(page) < 1:
            page = 1
    except ValueError:
        page = 1

    try:
        data, total_pages = paginate(res, page)
        return render(request, 'tag.html',
                      {'tag': tag_name, 'questions': data, 'tags': TAGS, 'page_num': int(page),
                       'total_pages': int(total_pages)})
    except EmptyPage:
        return not_found(request)
