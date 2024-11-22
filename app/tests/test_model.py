from django.test import TestCase
from app.models import UserProfile, Question, Answer, User, Tag


# Create your tests here.
class QuestionAnswerTagsModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user1 = User.objects.create(username='TestUser1',
                                    first_name='Test1',
                                    last_name='User1')
        user2 = User.objects.create(username='TestUser2',
                                    first_name='Test2',
                                    last_name='User2')
        tag = Tag.objects.create(tag="Tag1")
        answer = Answer.objects.create(correct=False, content='UsefulAnswer', like=0, author=user2)
        question = Question.objects.create(title='NeedHelp', content='Please help me', like=1, author=user1)
        question.tags.add(tag)
        question.answers.add(answer)
        question.liked_by.add(user2)

    # проверка что имя соответствует действительности
    def test_user1(self):
        user = User.objects.get(id=1)
        field_label = user.username
        self.assertEquals(field_label, 'TestUser1')

    # проверка что имя соответствует действительности
    def test_user2(self):
        user = User.objects.get(id=2)
        field_label = user.username
        self.assertEquals(field_label, 'TestUser2')

    # проверка что тэг соответствует действительности
    def test_tag(self):
        tag = Tag.objects.get(id=1)
        field_label = tag.tag
        self.assertEquals(field_label, 'Tag1')

    # проверка что ответ соответствует действительности
    def test_answer(self):
        answer = Answer.objects.get(id=1)
        field_label = answer.content
        self.assertEquals(field_label, 'UsefulAnswer')

    # проверка что вопрос соответствует действительности
    def test_question(self):
        answer = Answer.objects.get(id=1)
        question = Question.objects.get(id=1)
        field_label = question.title
        self.assertEquals(field_label, 'NeedHelp')
        answers = question.answers.all()
        self.assertEquals(answer in answers, True)
        self.assertEquals(question.like, 1)

    # связей вопрос-ответ, проверка ModelManager
    def test_answer_question(self):
        answer = Answer.objects.get(id=1)
        question = Question.objects.get(id=1)
        user1 = User.objects.get(id=1)
        self.assertEquals(answer.correct, False)
        Answer.objects.toggle_correct(user=user1, answer=answer, question=question)
        self.assertEquals(Answer.objects.get(id=1).correct, True)
        self.assertEquals(answer.like, 0)
        Answer.objects.toggle_like(user=user1, answer=answer)
        self.assertEquals(Answer.objects.get(id=1).like, 1)


class UserProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create(username='TestUser',
                                   first_name='Test',
                                   last_name='User')
        UserProfile.objects.create(user=user)

    # проверка что имя соответствует действительности
    def test_first_name(self):
        user = User.objects.get(id=3)
        field_label = user.first_name
        self.assertEquals(field_label, 'Test')

    # проверка что ник соответствует действительности
    def test_username(self):
        user = User.objects.get(id=3)
        field_label = user.username
        self.assertEquals(field_label, 'TestUser')

    # проверка что аватарка поставилась по умолчанию
    def test_avatar(self):
        profile = UserProfile.objects.get(id=1)
        field_label = profile.avatar.url
        self.assertEquals(field_label, '/uploads/avatar.png')
