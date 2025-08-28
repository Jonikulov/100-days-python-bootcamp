from turtle import Turtle

ALIGNMENT = "center"
FONT = ("Courier", 55, "bold")

class ScoreBoard(Turtle):
    def __init__(self, position):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.color("white")
        self.goto(position)
        self.score = 0
        self.update_score()

    def update_score(self):
        self.write(self.score, align=ALIGNMENT, font=FONT)

    def increase_score(self):
        self.score += 1
        self.clear()
        self.update_score()
