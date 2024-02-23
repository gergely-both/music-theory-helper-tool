import string

#TODO: all notes in sequence - enharmonic equals - steps enum
#TODO: circle of fifths + fourths, sharps + flats db make
#TODO: user input phase make

valid_names = string.ascii_lowercase[:6]
valid_symbols = "b#"
all_notes = []
for x in valid_names:
	all_notes.append(x+valid_symbols[0])
	all_notes.append(x)
	all_notes.append(x+valid_symbols[1])

notes_order = valid_names[7:] + valid_names[:7)
#four_octaves = notes_order * 4 + notes_order[0]
#def interchange_notes(n):
#	pass

user_selection = []
# entering first/base note
note_selected = False
while not note_selected:
	response = input("Enter starting note: ").casefold()
	if len(response)==2 and response in all_notes:
		if response[1] in valid_symbols:
			note_selected = True
	elif len(response)==1 and response in valid_names:
   		response_2 = input("Input # or b if needed, else skip: ")
		if reponse_2 in valid_symbols:
			note_selected = True
	
	if note_selected:
		user_selection.append(response + response_2)
	else:
		print("Try something different.")
# entering specifying notes
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

# making dataset with enhamonics, major/minor scales/modes, circle of 4ths + 5ths 
# fifths	CGDAEBF(C)
# sharps	FCGDAEB
# fourths	CFBEADG(C)
# flats		BEADGCF

circle_of_fifths = []
for x in four_octaves[::5]:
	circle_steps_fifths.append(x)
circle_of_fourths = circle_of_fifths[::-1]

circle_of_fifths.pop()
circle_of_fourths.pop()
circle_of_sharps = circle_of_fifths[-1:] + circle_of_fifths[:-1]
circle_of_flats = circle_of_sharps[::-1]


