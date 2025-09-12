from question_model import Question

class QuizBrain:
    """Quiz brain data model"""

    def __init__(self, questions_list):
        self.score = 0
        self.question_number = 1
        self.questions_list = questions_list

    def next_quiz(self):
        """Gets and asks the next question from the questions list."""
        self.crnt_quiz = Question()
        self.crnt_quiz = self.questions_list[self.question_number]
        self.question_number += 1
        return self.crnt_quiz.q_text

    def still_has_questions(self) -> bool:
        """Confirms whether there is a question left."""
        return self.question_number < len(self.questions_list)

    def is_answer_correct(self, user_answer):
        """Checks & compares user answer with the correct answer."""
        if user_answer == self.crnt_quiz.answer:
            self.score += 1
            return True
        return False
