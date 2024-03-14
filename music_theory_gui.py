import tkinter as tk
from music_theory_db import find_note, valid_names, valid_symbols, all_scales_raw, all_scales_corrected, all_modes


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

        self.guiding_label = tk.Label(master, text="Enter the starting / base note:", height=5)
        self.guiding_label.grid(row=0, columnspan=7)
        self.interaction_label = tk.Label(master, height=25)
        self.interaction_label.grid(row=1, column=0, columnspan=7)

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
        self.scales_found = []
        self.modes_found = []


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
                note_name = "".join(self.inputs)
                if note_name not in self.queue:
                    self.queue.append(note_name)
                self.inputs.clear()
        elif value == "NEXT":
            notes_selection = [find_note(note_name) for note_name in self.queue]
            self.find_all(notes_selection)
       
        if self.scales_found and self.modes_found:
            self.display_results()
            self.queue.clear()
            self.scales_found.clear()
            self.modes_found.clear()
        else:
            self.update_view()

        if self.inputs:
            self.button_ok.config(state="normal")
        else:
            self.button_ok.config(state="disabled")
        if len(self.queue) >= 2 and not self.inputs:
            self.button_next.config(state="normal")
        else:
            self.button_next.config(state="disabled")
 

    def update_view(self):
        to_show = []
        user_selection = ""
        if self.queue:
            self.guiding_label.config(text="Enter additional notes that belong together:")
            to_show.extend(self.queue)
        if self.inputs:
            user_selection = f'[{"".join(self.inputs)}]'
        else:
            user_selection = "[ ]"
        to_show.append(user_selection)
        self.interaction_label.config(text=" ".join(to_show))


    def display_results(self):
        all_found = self.scales_found + self.modes_found
        if all_found:
            to_output = [key + ", ".join(notes) for key, notes in all_found]
            # print("\n".join(to_output))
            self.interaction_label.config(text="\n".join(to_output))
            self.guiding_label.config(text=f'The key scales and modes for {"|".join(self.queue)} are:')


    def find_all(self, notes_selection):
        for scale_key, scale_notes_raw in all_scales_raw.items():
            scale_notes_corrected = all_scales_corrected[scale_key]
            if set(notes_selection).issubset(set(scale_notes_raw)):
                found_scale = (f"{scale_key} major key: ", scale_notes_corrected)
                self.scales_found.append(found_scale)
                for mode_name, mode_notes in all_modes.items():
                    if set(scale_notes_corrected) == set(mode_notes):
                        if any(name == mode_notes[0] for name in notes_selection[0].names):
                            found_mode = (f"{mode_name} mode: ", mode_notes)
                            self.modes_found.append(found_mode)


root = tk.Tk()
app = Window(root)
root.mainloop()


