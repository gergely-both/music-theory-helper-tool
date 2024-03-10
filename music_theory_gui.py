import tkinter as tk
from music_theory_db import valid_names, valid_symbols, find_note


class Window:
    def __init__(self, master):
        self.master = master
        self.master.title("Music Theory Helper Tool")
        self.label_guide = tk.Label(master, text="Enter the starting / base note:", height=5)
        self.label_guide.grid(row=0, columnspan=7)
        self.label = tk.Label(master, height=10)
        self.label.grid(row=1, column=0, columnspan=7)
        self.button_c = tk.Button(master, text="C", command=lambda: self.button_input("C"))
        self.button_c.grid(row=2, column=0)
        self.button_d = tk.Button(master, text="D", command=lambda: self.button_input("D"))
        self.button_d.grid(row=2, column=1)
        self.button_e = tk.Button(master, text="E", command=lambda: self.button_input("E"))
        self.button_e.grid(row=2, column=2)
        self.button_f = tk.Button(master, text="F", command=lambda: self.button_input("F"))
        self.button_f.grid(row=2, column=3)
        self.button_g = tk.Button(master, text="G", command=lambda: self.button_input("G"))
        self.button_g.grid(row=2, column=4)
        self.button_a = tk.Button(master, text="A", command=lambda: self.button_input("A"))
        self.button_a.grid(row=2, column=5)
        self.button_b = tk.Button(master, text="B", command=lambda: self.button_input("B"))
        self.button_b.grid(row=2, column=6)
        self.button_sharp = tk.Button(master, text="#", width=0, command=lambda: self.button_input("#"))
        self.button_sharp.grid(row=3, column=4, columnspan=2)
        self.button_flat = tk.Button(master, text="b", width=0, command=lambda: self.button_input("b"))
        self.button_flat.grid(row=3, column=1, columnspan=2)
        self.button_ok = tk.Button(master, text="OK", state="disabled", width=10, command=lambda: self.button_input("OK"))
        self.button_ok.grid(row=4, column=0, columnspan=7, pady=25)
        self.button_next = tk.Button(master, text="next", state="disabled", width=10, command=lambda: self.button_input("NEXT"))
        self.button_next.grid(row=5, column=0, columnspan=7, pady=10)

        self.input = []
        self.queue = []

    #TODO: queue names to notes correl sys solve trace
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
            if self.input:
                new_note = "".join(self.input)
                if new_note not in self.queue:
                    self.queue.append(new_note)
                self.input.clear()
        elif value == "NEXT":
            pass



        if self.input:
            self.button_ok.config(state="normal")
        elif not self.input:
            self.button_ok.config(state="disabled")
        if len(self.queue) >= 2:
            self.button_next.config(state="normal")
        elif len(self.queue) < 2:
            self.button_next.config(state="disabled")
        
        self.update_view()

    def update_view(self):
        to_show = []
        if self.queue:
            self.label_guide.config(text="Enter additional notes that belong together:")
            to_show.extend(self.queue)
        user_input = f'[{"".join(self.input)}]'
        to_show.append("".join(user_input))
        self.label.config(text=" ".join(to_show))


root = tk.Tk()
app = Window(root)
root.mainloop()

