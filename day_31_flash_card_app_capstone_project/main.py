"""Day 31. Flash Card App capstone project"""

from tkinter import *
# from tkinter import messagebox
import json

BACKGROUND_COLOR = "#B1DDC6"
WORD_LIST_FILE = "./data/turkish-english-words.json"
FRONT_LANG = "English"
BACK_LANG = "Turkish"
display_after = None

with open(WORD_LIST_FILE, "r", encoding="utf-8") as file:
    word_list = json.load(file)

def display_front_card(word):
    canvas.itemconfig(canvas_img, image=FRONT_IMG)
    canvas.itemconfig(card_title, text=FRONT_LANG, fill="black")
    canvas.itemconfig(card_word, text=word, fill="black")


def display_back_card(word):
    canvas.itemconfig(canvas_img, image=BACK_IMG)
    canvas.itemconfig(card_title, text=BACK_LANG, fill="white")
    canvas.itemconfig(card_word, text=word, fill="white")


def display_word_card(words_list):
    global display_after
    if len(words_list["LEARN"][0]) > 0:
        if display_after:
            window.after_cancel(display_after)
        learning_word = words_list["LEARN"][0]
        display_back_card(learning_word[BACK_LANG])
        display_after = window.after(
            3000, display_front_card, learning_word[FRONT_LANG])


def right_answer(words_list):
    word = words_list["LEARN"].pop(0)
    word_list["KNOW"].append(word)
    # Save changes
    with open(WORD_LIST_FILE, "w", encoding="utf-8") as file:
        json.dump(words_list, file, indent=4, ensure_ascii=False)
    display_word_card(words_list)


def wrong_answer(words_list):
    word = words_list["LEARN"].pop(0)
    word_list["LEARN"].append(word)
    # Save changes
    with open(WORD_LIST_FILE, "w", encoding="utf-8") as file:
        json.dump(words_list, file, indent=4, ensure_ascii=False)
    display_word_card(words_list)

# ------------------------------ TKINTER GUI -------------------------------- #
window = Tk()
window.title("Flash Cards")
window.config(bg=BACKGROUND_COLOR, padx=40, pady=40)

FRONT_IMG = PhotoImage(file="./images/card_front.png")
BACK_IMG = PhotoImage(file="./images/card_back.png")

canvas = Canvas(width=805, height=530, bg=BACKGROUND_COLOR,
                highlightthickness=0)
canvas_img = canvas.create_image(402, 264)
card_title = canvas.create_text(402, 130, font=("Sans Serif", 23, "italic"))
card_word = canvas.create_text(402, 270, font=("Sans Serif", 25, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

right_img = PhotoImage(file="./images/right.png")
right_btn = Button(image=right_img, bg=BACKGROUND_COLOR, border=0,
                    highlightthickness=0,
                    command=lambda: right_answer(word_list))
right_btn.grid(row=1, column=1)

wrong_img = PhotoImage(file="./images/wrong.png")
wrong_btn = Button(image=wrong_img, bg=BACKGROUND_COLOR, border=0,
                    highlightthickness=0,
                    command=lambda: wrong_answer(word_list))
wrong_btn.grid(row=1, column=0)

display_word_card(word_list)

window.mainloop()
