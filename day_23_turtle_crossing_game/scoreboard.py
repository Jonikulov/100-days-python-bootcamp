from turtle import Turtle

level_font = ("Courier", 14, "normal")
game_over_font = ("Courier", 20, "normal")

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.goto(-280, 260)
        self.score = 1
        self.update_score()

    def update_score(self):
        self.write(f"Level: {self.score}", font=level_font)

    def increase_score(self):
        self.score += 1
        self.clear()
        self.update_score()

    def game_over(self):
        self.home()
        self.write("GAME OVER", font=game_over_font, align="center")
