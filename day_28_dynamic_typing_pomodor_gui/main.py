from tkinter import *

# ---------------------------- CONSTANTS ------------------------------------ #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

repetitions = 0
timer = None
# ---------------------------- TIMER RESET ---------------------------------- #
def reset_cmd():
    global timer
    global repetitions
    if timer:
        window.after_cancel(timer)
    canvas.itemconfigure(timer_text, text="00:00")
    header_label.config(text="Timer", fg=GREEN)
    pomo_ticks["text"] = ""
    timer = None
    repetitions = 0

# ---------------------------- TIMER MECHANISM ------------------------------ #
def start_timer():
    global timer
    if timer:
        return
    global repetitions
    repetitions += 1

    if repetitions % 8 == 0:
        window.attributes("-topmost", True)
        header_label.config(text="Break", fg=RED)
        timer_sec = LONG_BREAK_MIN * 60
    elif repetitions % 2 == 0:
        window.attributes("-topmost", True)
        header_label.config(text="Break", fg=PINK)
        timer_sec = SHORT_BREAK_MIN * 60
    else:
        header_label.config(text="Work", fg=GREEN)
        timer_sec = WORK_MIN * 60
        window.attributes("-topmost", False)

    count_down(timer_sec)
    pomo_ticks.config(text = "✓" * (repetitions // 2))

# ---------------------------- COUNTDOWN MECHANSIM -------------------------- #
def count_down(count):
    global timer
    minute = count // 60
    second = count % 60
    text = f"{minute}:{second:02d}"
    canvas.itemconfigure(timer_text, text=text)
    if count > 0:
        timer = window.after(1, count_down, count - 1)
    else:
        timer = None
        start_timer()

# ---------------------------- UI SETUP ------------------------------------- #
window = Tk()
window.config(padx=100, pady=50, bg=YELLOW)
window.title("Pomodoro")

canvas = Canvas(width=205, height=230, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(103, 115, image=tomato_img)
timer_text = canvas.create_text(
    105, 135, text="00:00", fill="white", font=("Arial", 25, "bold"))
canvas.grid(row=1, column=1)

header_label = Label(
    text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 35, "bold"))
header_label.grid(row=0, column=1)

start_btn = Button(
    text="Start", command=start_timer, bg="white", highlightthickness=0)
start_btn.grid(row=2, column=0)

reset_btn = Button(
    text="Reset", command=reset_cmd, bg="white", highlightthickness=0)
reset_btn.grid(row=2, column=2)

pomo_ticks = Label(bg=YELLOW)
pomo_ticks.grid(row=3, column=1)

window.mainloop()
