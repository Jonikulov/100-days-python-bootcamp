"""Day 20. Snake Game"""

from turtle import Screen
from snake import Snake
from food import Food
from scoreboard import ScoreBoard
import time

screen = Screen()
screen.setup(600, 600)
screen.bgcolor("black")
screen.title("Snake Game")
screen.tracer(0)

snake = Snake()
food = Food()
score_board = ScoreBoard()

screen.listen()
screen.onkey(snake.turn_right, "Right")
screen.onkey(snake.turn_up, "Up")
screen.onkey(snake.turn_left, "Left")
screen.onkey(snake.turn_down, "Down")

game_on = True
while game_on:
    screen.update()
    time.sleep(0.1)
    snake.move()

    # Detect collision with food
    if snake.head.distance(food) < 15:
        food.refresh()
        score_board.increase_score()
        snake.extend()

    # Detect collision with wall
    if snake.head.xcor() < -280 or snake.head.xcor() > 280 or \
        snake.head.ycor() < -280 or snake.head.ycor() > 280:
        score_board.game_over()
        game_on = False

    # Detect collision with itself
    for segment in snake.segments[1:]:
        if snake.head.distance(segment) <= 5:
            score_board.game_over()
            game_on = False


screen.exitonclick()
