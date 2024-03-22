import string
from music_theory_db import all_scales_raw, all_scales_corrected, all_modes, find_note


scales_found = []
modes_found = []
user_selection = []


def display_results():
    all_found = scales_found + modes_found
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
for scale_key, scale_notes_raw in all_scales_raw.items():
    scale_notes_corrected = all_scales_corrected[scale_key]
    if set(user_selection).issubset(scale_notes_raw):
        found_scale = (f"{scale_key} major key:", scale_notes_corrected)
        scales_found.append(found_scale)
        for mode_name, mode_notes in all_modes.items():
            if set(scale_notes_corrected) == set(mode_notes):
                if any(name == mode_notes[0] for name in user_selection[0].names):
                    found_mode = (f"{mode_name} mode:", mode_notes)
                    modes_found.append(found_mode)

display_results()


