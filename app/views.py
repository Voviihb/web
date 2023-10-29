from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

QUESTIONS = [
    {
        'id': i,
        'title': f"Question {i}",
        'content': f"Long long lorem ipsum content {i}",
        'tags': ['Python', 'AI', 'Django']
    } for i in range(100)
]


def paginate(objects, page, per_page=10):
    paginator = Paginator(objects, per_page)
    return paginator.page(page).object_list


# Create your views here.
def index(request):
    page = request.GET.get('page', 1)
    try:
        return render(request, 'index.html', {'questions': paginate(QUESTIONS, page)})
    except EmptyPage:
        return render(request, 'index.html', {'questions': paginate(QUESTIONS, 1)})
    except PageNotAnInteger:
        return render(request, 'index.html', {'questions': paginate(QUESTIONS, 1)})


def question(request, question_id):
    page = request.GET.get('page', 1)
    item = QUESTIONS[question_id]
    answers = [
        {
            'id': i,
            'correct': False,
            'content': f"Very informative answer {i}"
        } for i in range(50)
    ]

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
    page = request.GET.get('page', 1)
    try:
        return render(request, 'hot.html', {'questions': paginate(QUESTIONS, page)})
    except EmptyPage:
        return render(request, 'hot.html', {'questions': paginate(QUESTIONS, 1)})
    except PageNotAnInteger:
        return render(request, 'hot.html', {'questions': paginate(QUESTIONS, 1)})


def tag(request, tag_name):
    page = request.GET.get('page', 1)
    res = []
    for item in QUESTIONS:
        if tag_name in item['tags']:
            res.append(item)

    try:
        return render(request, 'tag.html', {'tag': tag_name, 'questions': paginate(res, page)})
    except EmptyPage:
        return render(request, 'tag.html', {'questions': paginate(res, 1)})
    except PageNotAnInteger:
        return render(request, 'tag.html', {'questions': paginate(res, 1)})
