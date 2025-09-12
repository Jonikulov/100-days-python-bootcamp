"""Day 34. Creating a GUI Quiz App"""

from data import question_data
from question_model import Question
from quiz_brain import QuizBrain
from ui import QuizInterface

if __name__ == "__main__":

    question_bank = []
    for question in question_data:
        question_bank.append(Question(
            q_text=question["question"],
            answer=question["correct_answer"])
        )
    quiz = QuizBrain(question_bank)
    ui_app = QuizInterface(quiz)
    ui_app.mainloop()
