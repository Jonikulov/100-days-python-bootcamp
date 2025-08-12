"""Day 19. Etch-A-Sketch App"""

import turtle

screen = turtle.Screen()
tim = turtle.Turtle()
tim.speed(0)

def move_right():
    tim.setheading(0)
    tim.forward(10)

def move_up():
    tim.setheading(90)
    tim.forward(10)

def move_left():
    tim.setheading(180)
    tim.forward(10)

def move_down():
    tim.setheading(270)
    tim.forward(10)

def move_forward():
    tim.forward(15)

def move_backward():
    tim.backward(15)

def turn_left():
    tim.left(10)

def turn_right():
    tim.right(10)

def clear_reset():
    tim.clear()
    tim.reset()

screen.listen()

screen.onkey(move_right, "Right")
screen.onkey(move_up, "Up")
screen.onkey(move_left, "Left")
screen.onkey(move_down, "Down")
screen.onkey(move_forward, "w")
screen.onkey(move_backward, "s")
screen.onkey(turn_left, "a")
screen.onkey(turn_right, "d")
screen.onkey(clear_reset, "c")
screen.onkey(exit, "Q")

turtle.done()
