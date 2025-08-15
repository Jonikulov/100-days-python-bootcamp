from turtle import Turtle

STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]
MOVE_DISTANCE = 20
RIGHT = 0
UP = 90
LEFT = 180
DOWN = 270

class Snake:
    def __init__(self):
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]

    def create_snake(self):
        for position in STARTING_POSITIONS:
            self._add_segment(position)

    def _add_segment(self, position):
        snake_seg = Turtle("square")
        snake_seg.color("white")
        snake_seg.penup()
        snake_seg.teleport(*position)
        self.segments.append(snake_seg)

    def extend(self):
        self._add_segment(self.segments[-1].position())

    def move(self):
        for seg_num in range(len(self.segments) - 1, 0, -1):
            new_pos = self.segments[seg_num - 1].position()
            self.segments[seg_num].teleport(*new_pos)
        self.head.forward(MOVE_DISTANCE)

    def turn_right(self):
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)

    def turn_up(self):
        if self.head.heading() != DOWN:
            self.head.setheading(UP)

    def turn_left(self):
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)

    def turn_down(self):
        if self.head.heading() != UP:
            self.head.setheading(DOWN)
