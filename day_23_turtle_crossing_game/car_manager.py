from turtle import Turtle
import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
MOVE_DISTANCE = 5

class Car(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color(random.choice(COLORS))
        self.shapesize(1, 2)
        self.penup()
        self.goto(300, random.randint(-250, 250))


class CarManager:
    def __init__(self):
        self.speed = MOVE_DISTANCE
        self._cars = []

    def move_forward(self, player) -> bool:
        for car in self._cars:
            car.goto(car.xcor() - self.speed, car.ycor())
            if player.distance(car) <= 20:
                return True
            if car.xcor() < -320:
                self._cars.remove(car)
        return False

    def increase_speed(self):
        self.speed += MOVE_DISTANCE

    def generate_car(self):
        random_chance = random.randint(1, 6)
        if random_chance == 1:
            self._cars.append(Car())
