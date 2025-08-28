"""Day 22. The Pong Game"""

from turtle import Screen, Turtle, Vec2D
import random
import time

ALIGNMENT = "center"
FONT = ("Hack", 55, "bold")

screen = Screen()
screen.setup(900, 700)
screen.bgcolor("black")
screen.title("PONG")
# screen.tracer(0)

"""     TASKS & PSEUDOCODE:
* [] Setup screen size.
* [] Draw central border (dashed line).

* [] Define Paddle class.
    * [] left_paddle = PaddleClass()
    * [] right_paddle = PaddleClass()
    * [] Controlling & Moving the Paddle.

* [] Define Ball class OR ball object.
    * [] First build Easy version: square ball, then circle ball.
    * [] Ball throws to random player && random direction.
    * [] Detect collision with wall and bounce.
    * [] Detect collision with paddle.
    * [] Detect when paddle misses the ball.

* [] Define Score class.
    * [] left_score = Score()
    * [] right_score = Score()
    * [] Keep updating the score.
"""

central_border = Turtle()
central_border.hideturtle()
central_border.speed(0)
central_border.color("white")
central_border.pensize(9)
central_border.teleport(0, -355)
central_border.setheading(90)
# Draw the central border
for _ in range(19):
    central_border.goto(0, central_border.ycor() + 15)
    central_border.teleport(0, central_border.ycor() + 25)

class Paddle(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.penup()
        self.shapesize(5, 1, 1)

    def move_up(self):
        if self.ycor() <= 240:
            self.teleport(self.xcor(), self.ycor() + 80)

    def move_down(self):
        if self.ycor() >= -240:
            self.teleport(self.xcor(), self.ycor() - 80)


class Score(Turtle):
    def __init__(self, xcor=0, ycor=0):
        super().__init__()
        self.hideturtle()
        self.color("white")
        self.teleport(xcor, ycor)
        self.score = 0
        self.update_scoreboard()

    def update_scoreboard(self):
        self.write(self.score, align=ALIGNMENT, font=FONT)

    def increase_score(self):
        self.score += 1
        self.clear()
        self.update_scoreboard()

    # def game_over(self):
    #     self.teleport(0, 0)
    #     self.write("GAME OVER", align=ALIGNMENT, font=FONT)

left_score = Score(-100, 200)
right_score = Score(100, 200)

right_paddle = Paddle()
right_paddle.teleport(410, 0)
left_paddle = Paddle()
left_paddle.teleport(-415, 0)

screen.listen()
screen.onkey(right_paddle.move_up, "p")
screen.onkey(right_paddle.move_down, "l")
screen.onkey(left_paddle.move_up, "q")
screen.onkey(left_paddle.move_down, "a")

ball = Turtle("circle")
ball.penup()
ball.speed(2)
ball.color("white")

def initial_random_positions():
    # Initial Random Coordinates
    coord = [
        (random.choice([-435, 430]), random.randint(-332, 339)),
        (random.randint(-435, 430), random.choice([-332, 339]))
    ]
    xcor, ycor = random.choice(coord)
    # avoiding ball go and back again and again to top & down
    if -50 < xcor < 50:
        xcor = 50 if xcor > 0 else -50
    return xcor, ycor

def restart_game() -> Vec2D:
    # Start the game by going to a random position
    x, y = initial_random_positions()
    pos = ball.position()
    ball.setposition(x, y)
    return pos

prev_pos = restart_game()
while True:

    # If ball hits up/down border - it will change its direction (to certain angle).
    if ball.ycor() > 330 or ball.ycor() < -330:
    # if  ball.ycor() > 339 or ball.ycor() < -332:
        print("HIT BORDER!")  # TODO: fix behaviour
        angle = ball.towards(prev_pos)
        ball.setheading(180 - angle)
        prev_pos = ball.position()

    # If ball hits left/right paddle - it will change its direction accordingly.
    if ball.distance(left_paddle) < 15 or ball.distance(right_paddle) < 15:
        print("HIT PADDLE!")  # TODO: fix behaviour
        angle = ball.towards(prev_pos)
        ball.setheading(angle + 135)
        prev_pos = ball.position()

    # If ball hits left/right border - that paddle/player loses &&
    # update score && restart.
    if ball.xcor() > 430 or ball.xcor() < -435:
        if ball.xcor() > 0:
            left_score.increase_score()
        else:
            right_score.increase_score()
        ball.home()
        prev_pos = restart_game()

    # Ball goes 1 pace at a time forever.
    ball.forward(5)




'''turtle = Turtle("turtle")

# screen.delay(10)
# screen.tracer(n=1, delay=10)
# screen.tracer(n=2, delay=10)
# screen.tracer(n=3, delay=10)
# screen.tracer(n=5, delay=10)
# screen.tracer(n=100, delay=10)
# screen.tracer(n=1000, delay=10)

dist = 0.1
for i in range(1000):
    turtle.forward(dist)
    turtle.right(90)
    dist += 0.8

    screen.update()
    time.sleep(0.01)'''








screen.exitonclick()


















