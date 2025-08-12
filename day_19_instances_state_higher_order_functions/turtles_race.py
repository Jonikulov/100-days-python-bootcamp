"""Day 19. Turtles Race Game"""

import turtle
import random

screen = turtle.Screen()
screen.bgcolor("black")

guess = screen.textinput(
    "Make Your Guess", "Who will win the race? Enter a color: ")

turtle_colors = ["red", "green", "blue", "yellow", "orange"]
turtles = []

for t_color, y in zip(turtle_colors, range(200, -201, -100)):
    t = turtle.Turtle("turtle")
    t.color(t_color)
    t.turtlesize(2)
    t.penup()
    t.teleport(-450, y)
    turtles.append(t)

finish_liner = turtle.Turtle()
finish_liner.hideturtle()
finish_liner.color("white")
finish_liner.pensize(2)
finish_liner.teleport(400, -300)
finish_liner.setposition(400, 300)

race_end = False
while not race_end:

    for t in turtles:
        t.forward(random.randint(5, 20))
        if t.position()[0] > 400:
            winner = t.pencolor()
            if guess.strip().lower() == winner:
                print(f"You're Right! The winner is {winner}.")
            else:
                print(f"You're Wrong. The winner is {winner}.")
            race_end = True
            break

turtle.exitonclick()
