import string
from music_theory_db.py import all_major_scales, all_major_scales_raw, all_major_modes, all_existing_notes

user_selection = []

def extend_name(name):
    for i in all_notes_db:
        if name in all_notes_db[i]:
            return all_notes_db[i]


# ENTER FIRST MEMBER
note_selected = False
while not note_selected:
    response = input("Enter starting note: ").casefold()
    if response and response in all_existing_notes:
        user_selection.append(response)
        note_selected = True
    else:
        print("Try something different.")
           
# ENTER ADDITIONAL MEMBERS
more_notes_selected = False
while not more_notes_selected:
	response_2 = input("enter sharp or flat note(s) you know play well along it (comma-separated): ").casefold()
	response_2 = [x.strip() for x in response_2.split(",")]
	if response_2.issubset(all_existing_notes):
		user_selection.extend(response_3)
		more_notes_selected = True
	else:
		print("Something's incorrect. Try again.")

# QUERY SYSTEM BEGINS
# TODO: find scale, find mode, find first note in correct db, filter repeating inputs!, 
user_selection = [extend_name(x) for x in user_selection]
for scale in all_major_scales_raw:
    if set(user_selection).issubset(set(all_major_scales_raw[scale])):

        print(f"{scale} Major scale: ", all_major_scales[scale])
        
        for mode in all_major_modes:

