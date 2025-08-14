"""Day 20. Snake Game"""

import turtle
import random

turtle.title("SNAKE GAME")

screen = turtle.Screen()
screen.bgcolor("black")

colors = [
    "red", "green", "blue", "gold", "purple", "orange", "brown",
    "white", "gray", "cyan", "dim gray", "slate gray",
    "navy", "teal", "tomato", "indigo"
]
class Snake(turtle.Turtle):
    def __init__(self, prev_segment=None, head=None):
        super().__init__()
        self.shape("square")
        self.penup()
        self.speed(0)
        self.segments = []

        # if prev_segment:
        #     print(head.heading(), prev_segment.position())
        #     x, y = prev_segment.position()
        #     # Move the snake head & segment
        #     if head.heading() == 0:
        #         x -= 25
        #     elif head.heading() == 90:
        #         y -= 25
        #     elif head.heading() == 180:
        #         x += 25
        #     elif head.heading() == 270:
        #         y += 25
        #     self.teleport(x, y)

        self.color("white")
        # self.color(random.choice(colors))

# TODO debug: each snake (turtle) object creation is visible at the center - annoying.

snake = Snake()
snake.segments.append(Snake())

score = 0
score_text = turtle.Turtle()
score_text.hideturtle()
score_text.color("white")
score_text.teleport(0, 350)
score_text.write(f"Score: {score}", align="center", font=("Arial", 19, "bold"))

food = turtle.Turtle("circle")
food.turtlesize(0.7)
food.color("red")

def turn_right():
    if snake.heading() != 180:
        snake.setheading(0)

def turn_up():
    if snake.heading() != 270:
        snake.setheading(90)

def turn_left():
    if snake.heading() != 0:
        snake.setheading(180)

def turn_down():
    if snake.heading() != 90:
        snake.setheading(270)

def make_new_food():
    food.teleport(
        x = random.randint(-440, 440),
        y = random.randint(-360, 340)
    )

make_new_food()

screen.listen()

screen.onkey(turn_right, "Right")
screen.onkey(turn_up, "Up")
screen.onkey(turn_left, "Left")
screen.onkey(turn_down, "Down")
screen.onkey(exit, "q")

game_end = False
while not game_end:
    for segment in snake.segments:
        if game_end:
            break

        head_x, head_y = snake.position()
        snake.forward(5)
        segment.teleport(head_x, head_y)

        # Detect snake collision with food
        diff_x, diff_y = snake.position() - food.position()
        if -15 <= diff_x <= 15 and -15 <= diff_y <= 15:

            # Create new food
            make_new_food()
            # Update snake segment
            snake.segments.append(Snake())

            # Update score text
            score += 1
            score_text.clear()
            score_text.write(
                f"Score: {score}",
                align="center",
                font=("Arial", 19, "bold")
            )

        # Detect snake collision with borders
        if snake.xcor() < -465 or snake.xcor() > 459 or \
            snake.ycor() < -384 or snake.ycor() > 390:
            print("Collision with border detected!")
            game_end = True

        # Snake collision with itself
        for s in snake.segments:
            diff_x, diff_y = snake.position() - s.position()
            if -3 <= diff_x <= 3 and -3 <= diff_y <= 3 and score > 1:
                print("Collision with itself detected!")
                game_end = True
                break


# turtle.bye()
turtle.mainloop()



























