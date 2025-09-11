from tkinter import *
import requests

def get_quote() -> str:
    resp = requests.get(url="https://api.kanye.rest")
    resp.raise_for_status()
    quote = resp.json()["quote"]
    quote_canvas.itemconfig(quote_text, text=quote)


window = Tk()
window.title("Kanye Says...")
window.config(padx=35, pady=35)

quote_canvas = Canvas(width=305, height=415)  # highlightthickness=0
quote_img = PhotoImage(file="background.png")
quote_canvas.create_image(152, 207, image=quote_img)
quote_text = quote_canvas.create_text(
    150, 200, width=250, fill="white", font=("Arial", 19, "bold"))
quote_canvas.grid(row=0, column=0)

kanye_img = PhotoImage(file="kanye.png")
kanye_btn = Button(image=kanye_img, border=0, command=get_quote)
kanye_btn.grid(row=1, column=0)

window.mainloop()
