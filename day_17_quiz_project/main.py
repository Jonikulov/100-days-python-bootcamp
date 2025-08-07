"""Day 17. The Quiz Project."""

from data import question_data
from question_model import Question
from quiz_brain import QuizBrain

question_bank = []
for question in question_data:
    question_bank.append(
        Question(
            q_text=question["question"], answer=question["correct_answer"])
    )

quiz = QuizBrain(question_bank)
while quiz.still_has_questions():
    quiz.next_question()

print(f"You've completed the quiz.\n"
      f"Final Score: {quiz.score}/{quiz.question_number}")
