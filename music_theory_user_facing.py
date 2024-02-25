import string
from music_theory_db.py import all_major_scales_raw, all_major_scales, all_major_modes, all_existing_notes

user_selection = []
# ENTER FIRST MEMBER
note_selected = False
while not note_selected:
	response = input("Enter starting note: ").casefold()
    if response and response in all_existing_notes:
        if len(response) == 1:
            response_2 = input("Input '#' or 'b' if needed, else skip: ")
            if response + response_2 in all_existing_notes:
                note_selected = True
        else:
            if response in all_existing_notes_
            note_selected = True
    else:
		print("Try something different.")


# ENTER ADDITIONAL MEMBERS
more_notes_selected = False
while not more_notes_selected:
	response_3 = input("enter sharp or flat note(s) you know belongs in the scale: ").casefold()
	response_3 = response_3.split()
	if all(x in response_3 for y in all_notes):
		more_notes_selected = True
	if more_notes_selected:
		user_selection.extend(response_3)	
	else:
		print("Something's incorrect. Try again.")

