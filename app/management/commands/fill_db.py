from django.core.management import BaseCommand
from faker import Faker
from random import randint

from app.models import Question, Answer, Tag, User

fake = Faker()


class Command(BaseCommand):
    help = "Fills database with fake data"

    def add_arguments(self, parser):
        parser.add_argument("num", type=int)

    def handle(self, *args, **kwargs):
        num = kwargs['num']

        tags = [
            Tag(
                tag=fake.company().split(" ")[0]
            ) for _ in range(num)
        ]
        Tag.objects.bulk_create(tags)
        tags = Tag.objects.all()
        tags_count = tags.count()

        users = [
            User(
                username=fake.user_name(),
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name()
            ) for _ in range(num)
        ]

        User.objects.bulk_create(users)
        users = User.objects.all()
        users_count = users.count()

        answers = [
            Answer(
                content=fake.text(max_nb_chars=100),
                correct=fake.boolean(),
                like=randint(0, users_count - 1) % 100,
                author=users[fake.random_int(min=0, max=users_count - 1)],
                # rated_by=users[fake.random_int(min=0, max=users_count - 1)]
            ) for _ in range(100 * num)
        ]

        Answer.objects.bulk_create(answers)
        for _ in range(1, 100 * num):
            ans = Answer.objects.get(id=_)
            for j in range(ans.like):
                ans.rated_by.add(users[fake.random_int(min=0, max=users_count - 1)])

        answers = Answer.objects.all()
        answers_count = answers.count()

        questions = [
            Question(
                title=fake.job(), content=fake.paragraph(nb_sentences=5),
                like=randint(0, users_count - 1) % 100,
                # answers=answers[fake.random_int(min=0, max=answers_count - 1)],
                author=users[fake.random_int(min=0, max=users_count - 1)],
                # liked_by=users[fake.random_int(min=0, max=users_count - 1)]
            ) for _ in range(10 * num)
        ]

        Question.objects.bulk_create(questions)

        for _ in range(1, 10 * num):
            que = Question.objects.get(id=_)
            for j in range(que.like):
                que.liked_by.add(users[fake.random_int(min=0, max=users_count - 1)])
            for j in range(0, randint(0, 5)):
                que.answers.add(answers[fake.random_int(min=0, max=answers_count - 1)])
            for j in range(0, randint(0, 3)):
                que.tags.add(tags[fake.random_int(min=0, max=tags_count - 1)])
