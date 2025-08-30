"""Day 27. Tkinter. GUI Programs"""

import tkinter as tk

window = tk.Tk()
window.title("My First GUI Program")
window.minsize(width=500, height=300)
window.config(padx=20, pady=20)

# Label component
my_label = tk.Label(text="This is a Label", font=("Arial", 15, "bold"))
my_label.pack()  # expand=True, side="right"

my_label["text"] = "Text Updated"
# my_label.config(text="New Text", font=("Times New Roman", 25))
my_label.config(padx=150, pady=15)


def button_clicked():
    print("I got clicked")
    my_label["text"] = input_entry.get()

# Button
my_button = tk.Button(text="Click Me", command=button_clicked)
# my_button.pack()


# Entry
input_entry = tk.Entry(width=10)


# Layout Managers: pack, place, grid
my_label.place(x=100, y=200)
my_button.grid(column=0, row=0)
input_entry.grid(column=1, row=1)
# Note: you can't mix/use pack & grid together.




window.mainloop()
