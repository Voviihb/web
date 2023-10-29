from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

QUESTIONS = [
    {
        'id': i,
        'title': f"Question {i}",
        'content': f"Long long lorem ipsum content {i}"
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
        } for i in range(30)
    ]

    try:
        return render(request, 'question.html', {'question': item, 'answers': paginate(answers, page)})
    except EmptyPage:
        return render(request, 'question.html', {'question': item, 'answers': paginate(answers, 1)})
    except PageNotAnInteger:
        return render(request, 'question.html', {'question': item, 'answers': paginate(answers, 1)})


def ask(request):
    return render(request, 'ask.html')
