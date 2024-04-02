from music_theory_db import MusicalNote, all_existing_scales
from typing import List


scales_found = []
modes_found = []
user_selection = []


def find_all(notes_selection: List[MusicalNote]) -> None:
    """Finds major scales and modes based on user MusicalNote objects selection."""
    for scale in all_existing_scales:
        if set(notes_selection).issubset(scale.notes):
            found_scale = (f"{scale.name} major key: ", scale.notes_mod)
            scales_found.append(found_scale)
            for mode in scale.modes:
                mode_name = list(mode.keys())[0]
                mode_notes = list(mode.values())[0]
                if set(scale.notes_mod) == set(mode_notes):
                    if any(name == mode_notes[0] for name in notes_selection[0].names):
                        found_mode = (f"{mode_name} mode: ", mode_notes)
                        modes_found.append(found_mode)


def display_results():
    """Displays query results of user interaction."""
    all_found = scales_found + modes_found
    if all_found:
        for key_text, notes in all_found:
            scale = ", ".join(notes)
            print(key_text, scale)


# entering the starting note
note_selected = False
while not note_selected:
    response = input("Enter starting note: ").title()
    note_1 = MusicalNote.find_note(response)
    if note_1:
        user_selection.append(note_1)
        note_selected = True
    else:
        print("Try something different.")


# entering additional notes
more_notes_selected = False
while not more_notes_selected:
    response_2 = input(
        "Enter additional notes you know play well alongside (comma-separated): "
    ).title()
    response_2 = set(x.strip() for x in response_2.split(","))
    more_notes = [MusicalNote.find_note(name) for name in response_2]
    if all(more_notes):
        user_selection.extend(more_notes)
        more_notes_selected = True
    else:
        print("Something's incorrect. Try again.")


if __name__ == "__main__":
    find_all(user_selection)
    display_results()
