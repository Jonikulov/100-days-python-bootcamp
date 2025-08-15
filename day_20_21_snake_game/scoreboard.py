from turtle import Turtle

ALIGNMENT = "center"
FONT = ("Courier", 19, "bold")

class ScoreBoard(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.color("white")
        self.teleport(0, 260)
        self.score = 0
        self.update_scoreboard()

    def update_scoreboard(self):
        self.write(f"Score: {self.score}", align=ALIGNMENT, font=FONT)

    def increase_score(self):
        self.score += 1
        self.clear()
        self.update_scoreboard()

    def game_over(self):
        self.teleport(0, 0)
        self.write("GAME OVER", align=ALIGNMENT, font=FONT)
