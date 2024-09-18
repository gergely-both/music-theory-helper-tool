import tkinter as tk
from typing import List
from music_theory_db import MusicalNote, valid_names, valid_symbols, all_existing_scales


# tkinter button properties for the window object
button_properties = {
    "width": 3,
    "relief": "raised",
}


# NOTE: make window centered on the screen, make window resizable, if possible
class Window:
    """Tkinter window with buttons for user interaction and display for results."""

    def __init__(self, master):
        self.master = master
        self.master.title("Music Theory Helper Tool")

        # below tries to center the window on the screen:
        # self.master.geometry("400x400")
        # self.master.resizable(0, 0)
        # self.screenwidth = master.winfo_screenwidth()
        # self.screenheight = master.winfo_screenheight()
        # self.master.geometry(f"{int(self.screenwidth/4)}x{int(self.screenheight/2)}")
        # master.eval("tk::PlaceWindow . center")

        self.guiding_label = tk.Label(
            master, text="Enter the starting / base note:", height=5
        )
        self.guiding_label.grid(row=0, columnspan=7)
        self.interaction_label = tk.Label(master, height=25)
        self.interaction_label.grid(row=1, column=0, columnspan=7)
        self.button_c = tk.Button(
            master,
            text="C",
            command=lambda: self.button_input("C"),
            **button_properties,
        )
        self.button_c.grid(row=2, column=0)
        self.button_d = tk.Button(
            master,
            text="D",
            command=lambda: self.button_input("D"),
            **button_properties,
        )
        self.button_d.grid(row=2, column=1)
        self.button_e = tk.Button(
            master,
            text="E",
            command=lambda: self.button_input("E"),
            **button_properties,
        )
        self.button_e.grid(row=2, column=2)
        self.button_f = tk.Button(
            master,
            text="F",
            command=lambda: self.button_input("F"),
            **button_properties,
        )
        self.button_f.grid(row=2, column=3)
        self.button_g = tk.Button(
            master,
            text="G",
            command=lambda: self.button_input("G"),
            **button_properties,
        )
        self.button_g.grid(row=2, column=4)
        self.button_a = tk.Button(
            master,
            text="A",
            command=lambda: self.button_input("A"),
            **button_properties,
        )
        self.button_a.grid(row=2, column=5)
        self.button_b = tk.Button(
            master,
            text="B",
            command=lambda: self.button_input("B"),
            **button_properties,
        )
        self.button_b.grid(row=2, column=6)
        self.button_flat = tk.Button(
            master,
            text="b",
            command=lambda: self.button_input("b"),
            **button_properties,
        )
        self.button_flat.grid(row=3, column=1, columnspan=2)
        self.button_sharp = tk.Button(
            master,
            text="#",
            command=lambda: self.button_input("#"),
            **button_properties,
        )
        self.button_sharp.grid(row=3, column=4, columnspan=2)
        self.button_ok = tk.Button(
            master,
            text="OK",
            state="disabled",
            command=lambda: self.button_input("OK"),
            **button_properties,
        )
        self.button_ok.grid(row=4, column=0, columnspan=7)
        self.button_next = tk.Button(
            master,
            text="next",
            state="disabled",
            command=lambda: self.button_input("NEXT"),
            **button_properties,
        )
        self.button_next.grid(row=5, column=0, columnspan=7)
        self.button_del = tk.Button(
            master,
            text="del",
            state="disabled",
            command=lambda: self.button_input("del"),
            **button_properties,
        )
        self.button_del.grid(row=6, column=0, columnspan=3)
        self.button_clear = tk.Button(
            master,
            text="clear",
            state="disabled",
            command=lambda: self.button_input("clear"),
            **button_properties,
        )
        self.button_clear.grid(row=6, column=4, columnspan=3)
        self.button_restart = tk.Button(
            master,
            text="restart",
            state="normal",
            command=lambda: self.button_input("restart"),
            **button_properties,
        )
        self.button_restart.grid(row=7, column=0, columnspan=7)

        # instance attributes for user inputs and query results
        self.inputs = []
        self.queue = []
        self.scales_found = []
        self.modes_found = []

    def button_input(self, value: str) -> None:
        """Main control cycle and button input handling."""
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
            note_name = "".join(self.inputs)
            if note_name not in self.queue:
                self.queue.append(note_name)
            self.inputs.clear()
        elif value == "NEXT":
            notes_selection = [
                MusicalNote.find_note(note_name) for note_name in self.queue
            ]
            self.find_all(notes_selection)
        elif value == "del" and self.queue:
            del self.queue[-1]
        elif value == "clear" and self.inputs:
            self.inputs.clear()
        elif value == "restart":
            self.inputs.clear()
            self.queue.clear()

        self.display_dispatch(value)
        self.buttons_flip()

    def display_dispatch(self, value: str) -> None:
        """Dispatches to display functions for user interaction xor query results."""
        if value == "NEXT":
            self.display_result()
            self.queue.clear()
            self.scales_found.clear()
            self.modes_found.clear()
        else:
            self.display_interaction()

    def buttons_flip(self) -> None:
        """Changes button states based on user inputs and queue state."""
        if self.inputs:
            self.button_ok.config(state="normal")
            self.button_clear.config(state="normal")
        else:
            self.button_ok.config(state="disabled")
            self.button_clear.config(state="disabled")
        if self.queue:
            if len(self.queue) >= 2 and not self.inputs:
                self.button_next.config(state="normal")
            else:
                self.button_next.config(state="disabled")
                self.button_del.config(state="normal")
        else:
            self.button_next.config(state="disabled")
            self.button_del.config(state="disabled")

    def display_interaction(self) -> None:
        """Displays user interaction based on inputs and queue state"""
        to_show = []
        user_selection = ""
        if self.queue:
            self.guiding_label.config(
                text="Enter additional notes that belong together:"
            )
            to_show.extend(self.queue)
        else:
            self.guiding_label.config(text="Enter the starting / base note:")

        if self.inputs:
            user_selection = f'[{"".join(self.inputs)}]'
        else:
            user_selection = "[ ]"

        to_show.append(user_selection)
        self.interaction_label.config(text=" ".join(to_show))

    def display_result(self) -> None:
        """Displays query results of user interaction."""
        all_found = self.scales_found + self.modes_found
        self.guiding_label.config(
            text=f'The key scales and modes for {"|".join(self.queue)} are:'
        )
        if all_found:
            to_output = [key + ", ".join(notes) for key, notes in all_found]
            self.interaction_label.config(text="\n".join(to_output))
        else:
            self.interaction_label.config(text="Nothing found...")

    def find_all(self, notes_selection: List[MusicalNote]) -> None:
        """Finds major scales and modes based on user MusicalNote objects selection."""
        for scale in all_existing_scales:
            if set(notes_selection).issubset(scale.notes):
                found_scale = (f"{scale.key}: ", scale.notes_readable)
                self.scales_found.append(found_scale)
                for mode in scale.modes:
                    mode_name = list(mode.keys())[0]
                    mode_notes = list(mode.values())[0]
                    if set(scale.notes_readable) == set(mode_notes):
                        if any(
                            name == mode_notes[0] for name in notes_selection[0].enharmonics
                        ):
                            found_mode = (f"{mode_name}: ", mode_notes)
                            self.modes_found.append(found_mode)


if __name__ == "__main__":
    root = tk.Tk()
    app = Window(root)
    root.mainloop()
