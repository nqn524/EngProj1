import tkinter as tk

# Initialize app
window = tk.Tk()

def nutes():
    print(button_variable.get())

button_variable = tk.IntVar(value = 1)

chck_hi = tk.Checkbutton(window, text = 'Hi', variable = button_variable, command=nutes)

chck_hi.grid(row = 0, column = 0)

print(button_variable.get()) # Prints '1'


window.mainloop()