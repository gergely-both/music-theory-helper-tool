import string
from music_theory_db import all_major_scales, all_major_scales_mod, all_major_modes, find_note

found_scales = []
found_modes = []
user_selection = []


def display_results():
    all_found = found_scales + found_modes
    if all_found:
        for key_text, notes in all_found:
            scale = ", ".join(notes)
            print(key_text, scale)


# ENTER FIRST MEMBER
note_selected = False
while not note_selected:
    response = input("Enter starting note: ").title()
    note_1 = find_note(response)
    if note_1:
        user_selection.append(note_1)
        note_selected = True
    else:
        print("Try something different.")
           

# ENTER ADDITIONAL MEMBERS
more_notes_selected = False
while not more_notes_selected:
    response_2 = input("Enter additional notes you know play well alongside (comma-separated): ").title()
    response_2 = set(x.strip() for x in response_2.split(","))
    more_notes = [find_note(name) for name in response_2]
    if all(more_notes):
        user_selection.extend(more_notes)
        more_notes_selected = True
    else:
        print("Something's incorrect. Try again.")


# MAJOR SCALE AND MODE SEARCH SYSTEM
for key_name, scale_notes in all_major_scales.items():
    scale_notes_mod = all_major_scales_mod[key_name]
    if set(user_selection).issubset(set(scale_notes)):
        found_scale = (f"{key_name} major key:", scale_notes_mod)
        found_scales.append(found_scale)
        for mode_name, mode_notes in all_major_modes.items():
            if set(scale_notes_mod) == set(mode_notes):
                if any(name == mode_notes[0] for name in user_selection[0].names):
                    found_mode = (f"{mode_name} mode:", mode_notes)
                    found_modes.append(found_mode)

display_results()

