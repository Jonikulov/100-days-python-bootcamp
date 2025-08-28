"""Day 22. The Pong Game"""

from turtle import Screen
import time
from paddle import Paddle
from ball import Ball
from scoreboard import ScoreBoard

screen = Screen()
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("PONG")
screen.tracer(0)

right_paddle = Paddle((350, 0))
left_paddle = Paddle((-350, 0))
ball = Ball()
right_score = ScoreBoard((100, 200))
left_score = ScoreBoard((-100, 200))

screen.listen()
screen.onkey(right_paddle.move_up, "Up")
screen.onkey(right_paddle.move_down, "Down")
screen.onkey(left_paddle.move_up, "w")
screen.onkey(left_paddle.move_down, "s")

game_on = True
while game_on:

    screen.update()
    time.sleep(ball.move_speed)
    ball.move()

    # Ball collision with top/bottom
    if ball.ycor() > 290 or ball.ycor() <= -290:
        ball.bounce_y()

    # Ball collision with right paddle
    elif ball.distance(right_paddle) < 50 and ball.xcor() > 320:
        ball.bounce_x_r_paddle()

    # Ball collision with left paddle
    elif ball.distance(left_paddle) < 50 and ball.xcor() < -320:
        ball.bounce_x_l_paddle()

    # Detect right paddle misses the ball
    elif ball.xcor() > 390:
        ball.reset_position()
        left_score.increase_score()

    # Detect left paddle misses the ball
    elif ball.xcor() < -390:
        ball.reset_position()
        right_score.increase_score()

screen.exitonclick()
