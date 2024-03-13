import tkinter as tk
from music_theory_db import valid_names, valid_symbols, find_note, all_major_scales, all_major_scales_mod, all_major_modes


button_properties = {
"width": 3,
"relief": "raised",
}


class Window:
    def __init__(self, master):
        self.master = master
        self.master.title("Music Theory Helper Tool")
        # self.master.geometry("400x400")
        # self.master.resizable(0, 0)

        self.label_guide = tk.Label(master, text="Enter the starting / base note:", height=5)
        self.label_guide.grid(row=0, columnspan=7)
        self.label = tk.Label(master, height=25)
        self.label.grid(row=1, column=0, columnspan=7)

        self.button_c = tk.Button(master, text="C", command=lambda: self.button_input("C"), **button_properties)
        self.button_c.grid(row=2, column=0)
        self.button_d = tk.Button(master, text="D", command=lambda: self.button_input("D"), **button_properties)
        self.button_d.grid(row=2, column=1)
        self.button_e = tk.Button(master, text="E", command=lambda: self.button_input("E"), **button_properties)
        self.button_e.grid(row=2, column=2)
        self.button_f = tk.Button(master, text="F", command=lambda: self.button_input("F"), **button_properties)
        self.button_f.grid(row=2, column=3)
        self.button_g = tk.Button(master, text="G", command=lambda: self.button_input("G"), **button_properties)
        self.button_g.grid(row=2, column=4)
        self.button_a = tk.Button(master, text="A", command=lambda: self.button_input("A"), **button_properties)
        self.button_a.grid(row=2, column=5)
        self.button_b = tk.Button(master, text="B", command=lambda: self.button_input("B"), **button_properties)
        self.button_b.grid(row=2, column=6)

        self.button_flat = tk.Button(master, text="b", command=lambda: self.button_input("b"), **button_properties)
        self.button_flat.grid(row=3, column=1, columnspan=2)
        self.button_sharp = tk.Button(master, text="#", command=lambda: self.button_input("#"), **button_properties)
        self.button_sharp.grid(row=3, column=4, columnspan=2)

        self.button_ok = tk.Button(master, text="OK", state="disabled", command=lambda: self.button_input("OK"), **button_properties)
        self.button_ok.grid(row=4, column=0, columnspan=7)
        self.button_next = tk.Button(master, text="next", state="disabled", command=lambda: self.button_input("NEXT"), **button_properties)
        self.button_next.grid(row=5, column=0, columnspan=7)


        self.inputs = []
        self.queue = []
        self.found_scales = []
        self.found_modes = []


    # TODO: fix this sys
    def button_input(self, value):
        if value in valid_names:
            self.inputs.clear()
            self.inputs.append(value)
        elif value in valid_symbols:
            if self.inputs:
                if len(self.inputs) == 1:
                    self.inputs.append(value)
                elif len(self.inputs) == 2:
                    if value != self.inputs[1]:
                        self.inputs[1] = value
                    elif value == self.inputs[1]:
                        del self.inputs[1]
        elif value == "OK":
            if self.inputs:
                new_note = "".join(self.inputs)
                if new_note not in self.queue:
                    self.queue.append(new_note)
                self.inputs.clear()
        elif value == "NEXT":
            all_notes = [find_note(element) for element in self.queue]
            self.find_all(all_notes)
            self.queue.clear()

        if self.inputs:
            self.button_ok.config(state="normal")
        elif not self.inputs:
            self.button_ok.config(state="disabled")
        if len(self.queue) >= 2:
            self.button_next.config(state="normal")
        elif len(self.queue) < 2:
            self.button_next.config(state="disabled")
        
        if self.found_scales and self.found_modes:
            self.display_results()
            self.found_scales.clear()
            self.found_modes.clear()
        else:
            self.update_view()


    def update_view(self):
        to_show = []
        if self.queue:
            self.label_guide.config(text="Enter additional notes that belong together:")
            to_show.extend(self.queue)
        if self.inputs:
            user_input = f'[{"".join(self.inputs)}]'
        elif not self.inputs:
            user_input = "[ ]"
        to_show.append("".join(user_input))
        self.label.config(text=" ".join(to_show))


    def display_results(self):
        all_found = self.found_scales + self.found_modes
        if all_found:
            to_output = [key + ", ".join(notes) for key, notes in all_found]
            print("\n".join(to_output))
            self.label.config(text="\n".join(to_output))
            self.label_guide.config(text="The found key scales and modes are:")


    def find_all(self, notes_selection):
        for key_name, scale_notes in all_major_scales.items():
            scale_notes_mod = all_major_scales_mod[key_name]
            if set(notes_selection).issubset(set(scale_notes)):
                found_scale = (f"{key_name} major key: ", scale_notes_mod)
                self.found_scales.append(found_scale)
                for mode_name, mode_notes in all_major_modes.items():
                    if set(scale_notes_mod) == set(mode_notes):
                        if any(name == mode_notes[0] for name in notes_selection[0].names):
                            found_mode = (f"{mode_name} mode: ", mode_notes)
                            self.found_modes.append(found_mode)


root = tk.Tk()
app = Window(root)
root.mainloop()


