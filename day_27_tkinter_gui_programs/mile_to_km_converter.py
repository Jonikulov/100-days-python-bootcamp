from tkinter import *

window = Tk()
window.minsize(width=335, height=150)
window.title("Mile to Km Converter")
window.config(padx=30, pady=30)

def calculate():
    mile = float(mile_entry.get())
    km_result_value["text"] = round(mile * 1.609)


mile_entry = Entry(width=10)
mile_num = DoubleVar()
mile_num.set(0)
mile_entry['textvariable'] = mile_num
mile_entry.grid(row=0, column=1)

miles_label = Label(text="Miles")
miles_label.grid(row=0, column=2, padx=10)

equal_label = Label(text="is equal to")
equal_label.grid(row=1, column=0, pady=10)

km_result_value = Label(text=0)
km_result_value.grid(row=1, column=1, pady=10)

km_label = Label(text="Km")
km_label.grid(row=1, column=2, pady=10)

calculate_btn = Button(text="Calcualte", command=calculate)
calculate_btn.grid(row=2, column=1)

window.mainloop()
