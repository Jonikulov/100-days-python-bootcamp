"""Quiz Brain model of the Quiz Project"""

class QuizBrain:
    """Quiz brain data model"""

    def __init__(self, questions_list):
        self.question_number = 0
        self.questions_list = questions_list
        self.score = 0

    def next_question(self):
        """Gets and asks the next question from the questions list."""
        crnt_quest = self.questions_list[self.question_number]
        self.question_number += 1
        user_answer = input(
            f"Q.{self.question_number}: {crnt_quest.q_text} (True/False): "
        )
        self.check_answer(user_answer, crnt_quest.answer)

    def still_has_questions(self) -> bool:
        """Confirms whether there is a question left."""
        return self.question_number < len(self.questions_list)

    def check_answer(self, user_answer, correct_answer):
        """Checks & compares user answer with the correct answer."""
        if user_answer.strip().lower() == correct_answer.lower():
            self.score += 1
            print("CORRECT! ", end="")
        else:
            print("INCORRECT! ", end="")
        print(f"Current score: {self.score}/{self.question_number}\n")
