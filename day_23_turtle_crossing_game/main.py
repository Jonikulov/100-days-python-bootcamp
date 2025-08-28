"""Day 23. Turtle Crossing Game"""

import time
from turtle import Screen
from player import Player, STARTING_POSITION, FINISH_LINE_Y
from car_manager import CarManager
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width=600, height=600)
screen.title("Turtle Crossing Game")
screen.tracer(0)

player = Player()
cars = CarManager()
score = Scoreboard()

screen.listen()
screen.onkey(player.move, "Up")

game_is_on = True
while game_is_on:
    screen.update()
    time.sleep(0.05)

    cars.generate_car()
    collision = cars.move_forward(player)
    if collision:
        score.game_over()
        break

    if player.ycor() > FINISH_LINE_Y:
        cars.increase_speed()
        score.increase_score()
        player.goto(STARTING_POSITION)

screen.exitonclick()
