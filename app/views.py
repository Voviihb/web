from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from app.models import Question, Answer, Tag
from random import randint

QUESTIONS = [
    {
        'id': i,
        'title': f"Question {i}",
        'content': f"Long long lorem ipsum content {i}",
        'tags': ['Python', 'AI', 'Django']
    } for i in range(100)
]


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
        return render(request, 'index.html', {'questions': paginate(QUESTIONS, 1)})
    except PageNotAnInteger:
        return render(request, 'index.html', {'questions': paginate(QUESTIONS, 1)})


def question(request, question_id):
    QUESTIONS = Question.objects.all()
    page = request.GET.get('page', 1)
    try:
        item = QUESTIONS[question_id - 1]
    except IndexError:
        item = QUESTIONS[0]
    answers = Answer.objects.get_answers(question_id)

    try:
        return render(request, 'question.html', {'question': item, 'answers': paginate(answers, page)})
    except EmptyPage:
        return render(request, 'question.html', {'question': item, 'answers': paginate(answers, 1)})
    except PageNotAnInteger:
        return render(request, 'question.html', {'question': item, 'answers': paginate(answers, 1)})


def ask(request):
    return render(request, 'ask.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def settings(request):
    return render(request, 'settings.html')


def hot(request):
    QUESTIONS = Question.objects.sort_hot().all()
    page = request.GET.get('page', 1)
    try:
        return render(request, 'hot.html', {'questions': paginate(QUESTIONS, page)})
    except EmptyPage:
        return render(request, 'hot.html', {'questions': paginate(QUESTIONS, 1)})
    except PageNotAnInteger:
        return render(request, 'hot.html', {'questions': paginate(QUESTIONS, 1)})


def tag(request, tag_name):
    page = request.GET.get('page', 1)
    res = Tag.objects.get_questions(tag_name)
    for i in res:
        print(i)

    try:
        return render(request, 'tag.html', {'tag': tag_name, 'questions': paginate(res, page)})
    except EmptyPage:
        return render(request, 'tag.html', {'questions': paginate(res, 1)})
    except PageNotAnInteger:
        return render(request, 'tag.html', {'questions': paginate(res, 1)})
