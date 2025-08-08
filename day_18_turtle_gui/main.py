"""Day 18. Turtle & GUI"""
import turtle
import random

# HIRST PAINTING PROJECT IN TURTLE

colors = [
    "red", "green", "blue", "gold", "purple", "orange", "brown",
    "black", "gray", "cyan", "dim gray", "slate gray",
    "navy", "teal", "tomato", "indigo"
]
angles = [0, 90, 180, 270]

screen = turtle.Screen()
screen.setup(1920, 1080)
# screen.bgcolor("black")

turtle.colormode(255)
tim = turtle.Turtle()
tim.teleport(-250, 250)
tim.speed(0)
tim.width(2)
tim.hideturtle()

def random_color() -> tuple:
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return r, g, b

dot_size = 25
space_between = 50
for i in range(10):
    next_row_pos = tim.position() + (0, -space_between)
    for j in range(10):
        tim.color(random_color())
        tim.dot(dot_size)
        next_dot_pos = tim.position() + (space_between, 0)
        tim.teleport(*next_dot_pos)
    tim.teleport(*next_row_pos)

screen.exitonclick()
# turtle.done()
