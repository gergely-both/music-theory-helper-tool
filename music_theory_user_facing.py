# TODO: make input user processing less strict, write unit tests for border cases, upgrade to OOP, 

import string
from music_theory_db import all_existing_notes, all_major_scales, all_major_scales_raw, all_major_modes, steps_names_db, extend_name


def display_results(text, notes):
    scale = ", ".join(notes)
    print(text, scale)


user_selection = []


# ENTER FIRST MEMBER
note_selected = False
while not note_selected:
    response = input("Enter starting note: ").title()
    if response and response in all_existing_notes:
        user_selection.append(response)
        note_selected = True
    else:
        print("Try something different.")
           

# ENTER ADDITIONAL MEMBERS
more_notes_selected = False
while not more_notes_selected:
    response_2 = input("Enter additional notes you know play well alongside (comma-separated): ").title()
    response_2 = set(x.strip() for x in response_2.split(","))
    if response_2.issubset(all_existing_notes):
        user_selection.extend(response_2)
        more_notes_selected = True
    else:
        print("Something's incorrect. Try again.")


# MAJOR SCALE AND MODE SEARCH SYSTEM
user_selection_temp = []
for x in user_selection:
    user_selection_temp.extend(extend_name(x))
user_selection = user_selection_temp

for scale_name in all_major_scales_raw:
    scale_notes_raw = all_major_scales_raw[scale_name]
    scale_notes = all_major_scales[scale_name]
    if (set(user_selection)).issubset(set(scale_notes_raw)):
        display_results(f"{scale_name} major key:", scale_notes)

        for mode_name in all_major_modes:
            mode_notes = all_major_modes[mode_name]
            if (set(scale_notes)) == (set(mode_notes)):
                if any(name == mode_notes[0]for name in extend_name(user_selection[0])):
                    display_results(f"{mode_name} mode:", mode_notes)

