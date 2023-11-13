from app.models import Question
import time
start_time = time.time()
QUESTIONS = Question.objects.sort_new().all()
end_time = time.time()
print(f"QUESTIONS took {end_time - start_time} seconds")