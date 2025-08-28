import turtle
import pandas as pd
import time

turtle.bgpic("blank_states_img.gif")
turtle.setup(730, 495)
text_writer = turtle.Turtle()
text_writer.hideturtle()

# # Getting coordinates of the screen/image
# def get_mouse_click_coor(x, y):
#     print(x, y)
# turtle.onscreenclick(get_mouse_click_coor)
# turtle.mainloop()

df = pd.read_csv("50_states.csv")
us_states = df["state"].to_list()

def write_state_name(state: str) -> None:
    row = df[df["state"]==state]
    x, y = row["x"].item(), row["y"].item()
    text_writer.teleport(x, y)
    text_writer.write(state, align="center")


correct_states = 0
while correct_states != 50:
    time.sleep(1)

    user_input = turtle.textinput(
        f"{correct_states}/50 States Correct",
        "What's another state name?"
    ).strip().title()

    if user_input == "Exit":
        break
    if user_input in us_states:
        write_state_name(user_input)
        correct_states += 1
        us_states.remove(user_input)


pd.DataFrame({"States": us_states}).to_csv("states_to_learn.csv")
