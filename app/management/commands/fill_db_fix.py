from django.core.management import BaseCommand
from faker import Faker
from random import randint
import time

from app.models import Question, Answer, Tag, User, UserProfile

fake = Faker()


class Command(BaseCommand):
    help = "Fills database with fake data"

    def add_arguments(self, parser):
        parser.add_argument("num", type=int)

    def handle(self, *args, **kwargs):
        num = kwargs['num']

        # Create Tags in bulk
        Tag.objects.bulk_create([Tag(tag=" ".join(fake.catch_phrase()[:40].split("/"))) for _ in range(num)])
        tags_count = num

        # Create Users in bulk
        User.objects.bulk_create([User(
            username=fake.user_name() + str(randint(1, 100)) + str(randint(1, 100)),
            first_name=fake.first_name(),
            last_name=fake.last_name()
        ) for _ in range(num)])
        users_count = num

        UserProfile.objects.bulk_create([UserProfile(
            user_id=_ + 1,
        ) for _ in range(num)])

        start_time = time.time()
        # Create Answers in bulk

        Answer.objects.bulk_create([Answer(
            content=fake.text(max_nb_chars=100),
            correct=fake.boolean(),
            like=(randint(1, users_count - 1) % 100) * randint(-1, 1),
            author_id=fake.random_int(min=0, max=users_count - 1) + 1,
        ) for _ in range(100 * num)], batch_size=1000)
        end_time = time.time()
        print(f"answers took {end_time - start_time} seconds")

        start_time = time.time()
        # Add rated_by relationships in bulk
        rated_by_data = []
        for ans in Answer.objects.all():
            cur = []
            i = 0
            while i < abs(ans.like):
                check = (ans.id, fake.random_int(min=0, max=users_count - 1) + 1)
                if check in cur:
                    continue
                cur.append(check)
                i += 1
            rated_by_data += cur

        Answer.rated_by.through.objects.bulk_create(
            [Answer.rated_by.through(answer_id=ans_id, user_id=user_id) for ans_id, user_id in rated_by_data],
            batch_size=1000
        )

        end_time = time.time()
        print(f"add relations to answers took {end_time - start_time} seconds")

        answers_count = num * 100

        start_time = time.time()
        # Create Questions in bulk
        Question.objects.bulk_create([Question(
            title=fake.job(), content=fake.paragraph(nb_sentences=5),
            like=(randint(0, users_count - 1) % 500) * randint(-1, 1),
            author_id=fake.random_int(min=0, max=users_count - 1) + 1,
        ) for _ in range(10 * num)], batch_size=1000)
        end_time = time.time()
        print(f"questions took {end_time - start_time} seconds")

        start_time = time.time()

        liked_by_data = []
        answers_data = []
        tags_data = []
        for que in Question.objects.all():
            cur = []
            i = 0
            while i < abs(que.like):
                check = (que.id, fake.random_int(min=0, max=users_count - 1) + 1)
                if check in cur:
                    continue
                cur.append(check)
                i += 1
            liked_by_data += cur

            cur = []
            i = 0
            while i < randint(0, 25):
                check = (que.id, fake.random_int(min=0, max=answers_count - 1) + 1)
                if check in cur:
                    continue
                cur.append(check)
                i += 1
            answers_data += cur

            cur = []
            i = 0
            while i < randint(1, 3):
                check = (que.id, fake.random_int(min=0, max=tags_count - 1) + 1)
                if check in cur:
                    continue
                cur.append(check)
                i += 1
            tags_data += cur

        Question.liked_by.through.objects.bulk_create(
            [Question.liked_by.through(question_id=que_id, user_id=user_id) for que_id, user_id in liked_by_data],
            batch_size=1000
        )
        Question.answers.through.objects.bulk_create(
            [Question.answers.through(question_id=que_id, answer_id=ans_id) for que_id, ans_id in answers_data],
            batch_size=1000
        )
        Question.tags.through.objects.bulk_create(
            [Question.tags.through(question_id=que_id, tag_id=tag_id) for que_id, tag_id in tags_data], batch_size=1000
        )

        end_time = time.time()
        print(f"add relations to questions took {end_time - start_time} seconds")
