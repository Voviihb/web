from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.csrf import csrf_protect

from app.models import Question, Answer, Tag
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from .forms import LoginForm, RegisterForm
from .models import prepare_tags

TAGS = []

# uncomment after DB generation
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
        item = QUESTIONS[question_id - 1]
    except IndexError:
        return not_found(request)
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


@csrf_protect
def log_in(request):
    # TAGS = prepare_tags()
    if request.method == "GET":
        login_form = LoginForm()
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            if user is not None:
                login(request, user)
                return redirect(request.GET.get('next', 'index'))
            else:
                login_form.add_error(None, "Wrong username or password!")
    return render(request, 'login.html', {'tags': TAGS, 'form': login_form})


def signup(request):
    # TAGS = prepare_tags()
    if request.method == "GET":
        user_form = RegisterForm()
    if request.method == "POST":
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            if user:
                return redirect(request.GET.get('next', 'index'))
            else:
                user_form.add_error(None, "Registration error!")
    return render(request, 'signup.html', {'tags': TAGS, 'form': user_form})

def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))


@login_required(login_url='login')
def settings(request):
    # TAGS = prepare_tags()
    return render(request, 'settings.html', {'tags': TAGS})


def hot(request):
    # TAGS = prepare_tags()
    QUESTIONS = Question.objects.sort_hot()
    page = request.GET.get('page', 1)

    try:
        data, total_pages = paginate(QUESTIONS, page)
        return render(request, 'hot.html', {'questions': data,
                                            'tags': TAGS, 'page_num': int(page), 'total_pages': int(total_pages)})
    except EmptyPage:
        return not_found(request)


def tag(request, tag_name):
    # TAGS = prepare_tags()
    page = request.GET.get('page', 1)
    try:
        res = Tag.objects.get_questions(tag_name)
    except ObjectDoesNotExist:
        return not_found(request)

    try:
        data, total_pages = paginate(res, page)
        return render(request, 'tag.html',
                      {'tag': tag_name, 'questions': data, 'tags': TAGS, 'page_num': int(page),
                       'total_pages': int(total_pages)})
    except EmptyPage:
        return not_found(request)
