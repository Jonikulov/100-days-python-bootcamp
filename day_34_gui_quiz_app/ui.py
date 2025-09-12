import tkinter as tk
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"

class QuizInterface(tk.Tk):
    print("Initializing UI...")

    def __init__(self, quiz_brain: QuizBrain):
        super().__init__()
        self.title("Quizzler")
        self.config(padx=35, pady=35, bg=THEME_COLOR)
        self.quiz = quiz_brain
        # Build UI app components
        self.build_score_label()
        self.build_quest_num_label()
        self.build_question_canvas()
        self.build_true_button()
        self.build_false_button()
        # Start the quiz
        self.next_question()


    def build_score_label(self):
        self.score_label = tk.Label(
            text=f"Score: {self.quiz.score}",
            fg="white",
            bg=THEME_COLOR,
            font=("Arial", 12, "bold"),
        )
        self.score_label.grid(row=0, column=1)


    def build_quest_num_label(self):
        self.q_num_lable = tk.Label(
            text=f"Q: {self.quiz.question_number}",
            fg="white",
            bg=THEME_COLOR,
            font=("Arial", 12, "bold"),
        )
        self.q_num_lable.grid(row=0, column=0)


    def build_question_canvas(self):
        self.q_canvas = tk.Canvas(width=400, height=400, bg="white")
        self.canvas_text = self.q_canvas.create_text(
            200, 200,
            width=250,
            font=("Arial", 15, "italic"),
        )
        self.q_canvas.grid(row=1, column=0, columnspan=2, pady=35)


    def build_true_button(self):
        self.true_img = tk.PhotoImage(file="images/true.png")
        self.true_btn = tk.Button(
            image=self.true_img,
            command=self.click_true,
            border=0,
            highlightthickness=0,
            bg=THEME_COLOR,
        )
        self.true_btn.grid(row=2, column=0)


    def build_false_button(self):
        self.false_img = tk.PhotoImage(file="images/false.png")
        self.false_btn = tk.Button(
            image=self.false_img,
            command=self.click_false,
            border=0,
            highlightthickness=0,
            bg=THEME_COLOR,
        )
        self.false_btn.grid(row=2, column=1)


    def click_true(self):
        self.q_num_lable.config(text=f"Q: {self.quiz.question_number}")
        if self.quiz.is_answer_correct("True"):
            self.give_feedback(True)
        else:
            self.give_feedback(False)


    def click_false(self):
        self.q_num_lable.config(text=f"Q: {self.quiz.question_number}")
        if self.quiz.is_answer_correct("False"):
            self.give_feedback(True)
        else:
            self.give_feedback(False)


    def next_question(self):
        self.q_canvas.config(bg="white")
        self.score_label.config(text=f"Score: {self.quiz.score}")
        if self.quiz.still_has_questions():
            quest = self.quiz.next_quiz()
            self.q_canvas.itemconfig(self.canvas_text, text=quest)
        else:
            self.q_canvas.itemconfig(
                self.canvas_text,
                text="You've reached the end of the quiz!"
            )
            self.true_btn.config(state="disabled")
            self.false_btn.config(state="disabled")


    def give_feedback(self, is_right):
        if is_right:
            color = "green"
        else:
            color = "red"
        self.q_canvas.config(bg=color)
        self.after(1000, self.next_question)
