import tkinter as tk
from music_theory_db import valid_names, valid_symbols


class Window:
    def __init__(self, master):
        self.master = master
        self.master.title("Music Theory Helper Tool")
        self.label = tk.Label(master, text="Enter base note:")
        self.label.grid(row=0, column=0, columnspan=7)
        self.button_c = tk.Button(master, text="C", command=lambda: self.button_input("C"))
        self.button_c.grid(row=1, column=0)
        self.button_d = tk.Button(master, text="D", command=lambda: self.button_input("D"))
        self.button_d.grid(row=1, column=1)
        self.button_e = tk.Button(master, text="E", command=lambda: self.button_input("E"))
        self.button_e.grid(row=1, column=2)
        self.button_f = tk.Button(master, text="F", command=lambda: self.button_input("F"))
        self.button_f.grid(row=1, column=3)
        self.button_g = tk.Button(master, text="G", command=lambda: self.button_input("G"))
        self.button_g.grid(row=1, column=4)
        self.button_a = tk.Button(master, text="A", command=lambda: self.button_input("A"))
        self.button_a.grid(row=1, column=5)
        self.button_b = tk.Button(master, text="B", command=lambda: self.button_input("B"))
        self.button_b.grid(row=1, column=6)
        self.button_sharp = tk.Button(master, text="#", command=lambda: self.button_input("#"))
        self.button_sharp.grid(row=2, column=5, columnspan=2)
        self.button_flat = tk.Button(master, text="b", command=lambda: self.button_input("b"))
        self.button_flat.grid(row=2, column=0, columnspan=2)
        self.button_ok = tk.Button(master, text="OK", command=lambda: self.button_input("OK"))
        self.button_ok.grid(row=2, column=2, columnspan=3)

        self.input = []
        self.queue = []

    def button_input(self, value):
        if value in valid_names:
            self.input.clear()
            self.input.append(value)
        elif value in valid_symbols:
            if self.input:
                if len(self.input) == 1:
                    self.input.append(value)
                elif len(self.input) == 2:
                    if value != self.input[1]:
                        self.input[1] = value
                    elif value == self.input[1]:
                        del self.input[1]
        elif value == "OK":
            self.queue.append("".join(self.input))
        self.update_view()

    def update_view(self):
        if self.input:
            self.label.config(text="".join(self.input))


root = tk.Tk()
app = Window(root)
root.mainloop()

