from django.test import TestCase
from app.models import UserProfile, Question, Answer, User, Tag
from faker import Faker
from django.urls import reverse
from bs4 import BeautifulSoup

# Create your tests here.
fake = Faker()


class IndexViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create 15 question for pagination tests
        num = 15
        for i in range(num):
            user = User.objects.create(username=fake.user_name(),
                                       first_name=fake.first_name(),
                                       last_name=fake.last_name())

            Question.objects.create(
                title=fake.job(), content=fake.paragraph(nb_sentences=5),
                like=1, author=user,
            )

    # проверка доступности по url
    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    # проверка доступности по названию пути
    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)

    # проверка, что пагинация работает (выводит 10 элементов)
    def test_pagination_is_ten(self):
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)
        soup = BeautifulSoup(resp.content, 'html.parser')
        question_elements = soup.find_all(class_='row question')
        self.assertEqual(len(question_elements), 10)

    # проверка, что пагинация работает (выводит остаток)
    def test_list_all_left_questions(self):
        # Get second page and confirm it has (exactly) remaining 5 items
        resp = self.client.get(reverse('index') + '?page=2')
        self.assertEqual(resp.status_code, 200)
        soup = BeautifulSoup(resp.content, 'html.parser')
        question_elements = soup.find_all(class_='row question')
        self.assertEqual(len(question_elements), 5)

    # проверка существования страницы конкретного вопроса
    def test_separate_question_view(self):
        resp = self.client.get(reverse('question', kwargs={'question_id': 2}))
        self.assertEqual(resp.status_code, 200)


# класс проверок доступности по названию пути
class PagesViewTest(TestCase):

    def test_hot_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('hot'))
        self.assertEqual(resp.status_code, 200)

    def test_login_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)

    def test_signup_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)


class AnswerQuestionsViewTest(TestCase):

    def setUp(self):
        # Создание пользователей
        test_user1 = User.objects.create_user(username='testuser1', password='ASDF1234')
        test_user1.save()
        test_user2 = User.objects.create_user(username='testuser2', password='ASDF1234')
        test_user2.save()

        # Создание вопроса
        question = Question.objects.create(
            title=fake.job(), content=fake.paragraph(nb_sentences=5),
            like=0, author=test_user1
        )
        question.save()

    # тесты без авторизации
    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('ask'))
        self.assertRedirects(resp, '/login?next=/ask')
        resp = self.client.post(reverse('like_question'), {'question_id': 1})
        self.assertRedirects(resp, '/login?next=/like_question')

    # тесты с выполненной авторизацией
    def test_logged_in(self):
        login = self.client.login(username='testuser2', password='ASDF1234')
        resp = self.client.get(reverse('ask'))

        # Проверка что пользователь залогинился
        self.assertEqual(str(resp.context['user']), 'testuser2')
        self.assertEqual(resp.status_code, 200)

        # Проверка постановки лайка
        prev_like = Question.objects.get(id=1).like
        resp = self.client.post(reverse('like_question'), {'question_id': 1})
        self.assertEqual(resp.status_code, 200)
        cur_like = Question.objects.get(id=1).like
        self.assertTrue(abs(prev_like - cur_like) == 1)

        # Проверка что пользователь разлогинился
        resp = self.client.get(reverse('logout'))
        self.assertRedirects(resp, '/login')
