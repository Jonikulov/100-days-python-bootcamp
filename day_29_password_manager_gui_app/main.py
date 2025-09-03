# ---------------------------- PASSWORD GENERATOR --------------------------- #
def generate_pass():
    password = []
    password += sample(string.ascii_letters, k=randint(8, 9))
    password += sample(string.digits, k=randint(2, 4))
    password += sample(string.punctuation, k=randint(2, 4))
    shuffle(password)
    password = "".join(password)
    password_input.delete(0, END)
    password_input.insert(0, password)
    window.clipboard_clear()
    window.clipboard_append(password)

# ---------------------------- SAVE PASSWORD -------------------------------- #
def save_data():
    website = website_input.get().strip()
    username = email_input.get().strip()
    password = password_input.get().strip()
    if not all([website, username, password]):
        messagebox.showwarning(
            title="Warning",
            message="Please don't leave any fields empty."
        )
        return
    is_ok = messagebox.askokcancel(
        title="Confirmation",
        message=f"Email: {username}\nPassword: {password}\nIs it ok to save?"
    )
    if is_ok:
        with open("data.txt", 'a') as file:
            file.write(f"{website} | {username} | {password}\n")
        website_input.delete(0, END)
        password_input.delete(0, END)
        website_input.focus()

# ---------------------------- UI SETUP ------------------------------------- #

from tkinter import *
from tkinter import messagebox
from random import randint, sample, shuffle
import string

window = Tk()
window.title("Password Manager")
window.config(padx=35, pady=35)

canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0, padx=15)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

website_input = Entry(width=37)
website_input.grid(row=1, column=1, columnspan=2)
website_input.focus()

email_input = Entry(width=37)
email_input.grid(row=2, column=1, columnspan=2)
email_input.insert(0, "example@email.com")

password_input = Entry(width=20)
password_input.grid(row=3, column=1, sticky="w")

gen_pass_btn = Button(text="Generate Password", width=13, command=generate_pass)
gen_pass_btn.grid(row=3, column=2, sticky="e")

add_button = Button(text="Add", width=35, bg="blue", fg="white", font=("", 10, "bold"), command=save_data)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
