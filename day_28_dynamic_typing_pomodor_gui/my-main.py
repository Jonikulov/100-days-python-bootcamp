"""Day 28. Tkinter, Dynamic Typing & Pomodoro GUI app"""

from tkinter import *
import time
from threading import Thread

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

is_pomo_reset = False
pomo_thread = None

def start_timer(minutes: int):
    global is_pomo_reset
    second = 0
    while minutes > -1 and not is_pomo_reset:
        timer_label["text"] = f"{minutes}:{second:02d}"
        time.sleep(0.001) # ; time.sleep(0.9)
        second -= 1
        if second < 0:
            minutes -= 1
            second = 59
    timer_label["text"] = "00:00"


def write_pomo_ticks(pomo_count):
    global is_pomo_reset
    if is_pomo_reset:
        return
    pomo_label = ["✔️"] * pomo_count
    for i in range(0, pomo_count + 6, 5):
        pomo_label.insert(i, "\n")
    pomo_ticks_label.config(text="".join(pomo_label), fg=GREEN)


def run_pomo():
    global is_pomo_reset
    pomodoro_count = 0
    while not is_pomo_reset:
        window.attributes("-topmost", False)
        header_label.config(text="Work", fg=GREEN)
        start_timer(WORK_MIN)
        pomodoro_count += 1
        write_pomo_ticks(pomodoro_count)
        window.attributes("-topmost", True)

        if pomodoro_count % 4 == 0:
            header_label.config(text="Long Break", fg=RED)
            start_timer(LONG_BREAK_MIN)
        else:
            header_label.config(text="Short Break", fg=RED)
            start_timer(SHORT_BREAK_MIN)
    header_label.config(text="Timer", fg=GREEN)


def run_pomo_worker():
    global is_pomo_reset
    global pomo_thread
    is_pomo_reset = False

    if pomo_thread and pomo_thread.is_alive():
        # Pomodoro already running, ignoring new click
        return
    pomo_thread = Thread(target=run_pomo, daemon=True)
    pomo_thread.start()


def reset():
    global is_pomo_reset
    is_pomo_reset = True
    pomo_ticks_label["text"] = ""


# ------------------------- TKINTER GUI ------------------------------------ #
window = Tk()
window.config(width=500, height=500, background=YELLOW)
window.title("Pomodoro")

# Setup background image
tomato_img = PhotoImage(file="tomato.png")
bg_img_label = Label(image=tomato_img, bg=YELLOW)
bg_img_label.place(relx=0.5, rely=0.45, anchor=CENTER)

header_label = Label(
    text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 40, "bold")
)
header_label.place(relx=0.5, y=70, anchor=CENTER)

start_btn = Button(text="Start", background="white", command=run_pomo_worker)
start_btn.place(relx=0.2, y=350, anchor="w")

reset_btn = Button(text="Reset", background="white", command=reset)
reset_btn.place(relx=0.8, y=350, anchor="e")

# timer_label = Label(text="00:00", fg="white", bg=bg_img_label["bg"], font=(FONT_NAME, 20, "bold"))
timer_label = Label(text="00:00", fg="white", bg="#ef7753", font=(FONT_NAME, 25, "bold"))
timer_label.place(relx=0.5, rely=0.5, anchor=CENTER, y=15)

pomo_ticks_label = Label(bg=YELLOW)
pomo_ticks_label.place(relx=0.5, y=370, anchor="n")

window.mainloop()
