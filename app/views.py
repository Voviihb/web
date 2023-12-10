from django.contrib import auth
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.csrf import csrf_protect

from app.models import Question, Answer, Tag
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist

from .forms import LoginForm, RegisterForm, UserProfileForm, CustomPasswordChangeForm, AskForm, AnswerForm
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
        if request.method == 'POST':
            form = AnswerForm(request.POST)
            if form.is_valid():
                answer_result = Answer(
                    content=form.cleaned_data['content'],
                    correct=False,
                    like=0,
                    author_id=request.user.id,
                )
                answer_result.save()

                question_obj = Question.objects.get(id=question_id)
                question_obj.answers.add(answer_result)
                question_obj.save()

                redirect_url = reverse('question', kwargs={
                    'question_id': question_id}) + f'?page={total_pages}'

                return redirect(redirect_url)
        else:
            form = AnswerForm()

        return render(request, 'question.html',
                      {'question': item, 'form': form, 'answers': data, 'tags': TAGS, 'page_num': int(page),
                       'total_pages': int(total_pages)})
    except EmptyPage:
        return not_found(request)


@login_required(login_url='login')
def ask(request):
    # TAGS = prepare_tags()

    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            question_result = Question(
                title=form.cleaned_data['title'], content=form.cleaned_data['content'],
                like=0, author_id=request.user.id)
            tag_list = [_.strip() for _ in form.cleaned_data['tags'].split(',') if _.strip()]
            question_result.save()

            saved_tags = []
            for _ in tag_list:
                saved_tag, created = Tag.objects.get_or_create(tag=_)
                saved_tags.append(saved_tag)

            question_result.tags.set(saved_tags)
            question_result.save()

            return redirect('question', question_id=question_result.id)
    else:
        form = AskForm()

    return render(request, 'ask.html', {'tags': TAGS, 'form': form})


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
                login(request, user)
                return redirect(request.GET.get('next', 'index'))
            else:
                user_form.add_error(None, "Registration error!")
    return render(request, 'signup.html', {'tags': TAGS, 'form': user_form})


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))


@csrf_protect
@login_required(login_url='login')
def settings(request):
    # TAGS = prepare_tags()
    if request.method == "GET":
        user_form = UserProfileForm(instance=request.user)
        password_form = CustomPasswordChangeForm(request.user)
        print(request.user.userprofile.avatar)
    if request.method == "POST":
        user_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        password_form = CustomPasswordChangeForm(request.user, request.POST)

        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important to maintain the session after password change
            return redirect(request.GET.get('next', 'index'))

        if user_form.is_valid() and request.POST.get('email') and not any(
                [request.POST.get('old_password'), request.POST.get('new_password1'),
                 request.POST.get('new_password2')]):
            user_form.save()
            return redirect(request.GET.get('next', 'index'))

        if not password_form.is_valid():
            password_form.add_error(None, "Changing password error!")
        if not user_form.is_valid() or not request.POST.get('email'):
            user_form.add_error(None, "Changing error!")

    return render(request, 'settings.html', {'tags': TAGS, 'user_form': user_form, 'password_form': password_form})


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
