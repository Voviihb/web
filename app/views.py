from django.shortcuts import render
from django.http import HttpResponse

QUESTIONS = [
    {
        'id': i,
        'title': f"Question {i}",
        'content': f"Long long lorem ipsum content {i}"
    } for i in range(15)
]


# Create your views here.
def index(request):
    return render(request, 'index.html', {'questions': QUESTIONS})


def question(request, question_id):
    item = QUESTIONS[question_id]
    answers = [
        {
            'id': i,
            'correct': False,
            'content': f"Very informative answer {i}"
        } for i in range(10)
    ]
    return render(request, 'question.html', {'question': item, 'answers': answers})
