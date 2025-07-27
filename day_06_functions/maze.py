# PROBLEM: https://reeborg.ca/reeborg.html?lang=en&mode=python&menu=worlds%2Fmenus%2Freeborg_intro_en.json&name=Maze&url=worlds%2Ftutorial_en%2Fmaze1.json

def turn_right():
    for _ in range(3):
        turn_left()

infin_loop = 0
while not at_goal():
    if right_is_clear() and infin_loop < 4:
        turn_right()
        move()
        infin_loop += 1
    elif front_is_clear():
        move()
        infin_loop = 0
    else:
        turn_left()
        infin_loop = 0
