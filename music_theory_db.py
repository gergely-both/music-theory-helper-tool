import string

valid_names = string.ascii_lowercase[:6]
names_order = valid_names[2:] + valid_names[:2]
valid_symbols = "b#"
major_steps = [0, 2, 4, 5, 7, 9, 11]
major_mode_names = ["ionian", "dorian", "phrygian", "lydian", "mixolydian", "aeolian", "locrian"]
major_mode_starts = {k:v for (k,v) in zip(major_steps, major_mode_names)}

#TODO: enharmony grouping system fix: namedtuple?
all_notes_db = {}
#### unmarked notes add to db (C Major scale)
for i in range(len(names_order)):
    all_notes_db[major_steps[i]] = list(names_order[i])
#### all marked notes add to db (plus enharmonics)
for symbol in valid_symbols:
    symbol_value = -1 if symbol == "b" else +1
    modifier = (12 + symbol_value) % 12
    for name in valid_names:
        for steps in all_notes_db:
            if note_order[steps] == name:
                if steps + modifier in all_notes_db:
                    all_notes_db[steps + modifier] = notes_order[steps + modifier].append(name + symbol)
                elif steps + modifier not in all_notes_db:
                    all_notes_db[steps + modifier] = list(None, name + symbol)

#TODO correct # or b display
circle_of_fifths = []
while not (circle_of_fifths[0] == circle_of_fifths[-1] and len(circle_of_fifths) > 1):
    if not circle_of_fifths:
        circle_of_fifths.append(all_notes_db[0])
    else:
        for x in all_notes_db:
            if all_notes_db[x] == circle_of_fifths[-1]:
                circle_of_fifths.append(all_notes_db[x+7])
circle_of_fourths = circle_of_fifths[::-1]
circle_of_sharps = circle_of_fifths[6:]
circle_of_flats = circle_of_fourths[2:9]

sharp_major_scales = {}
for i in len(circle_of_sharps):
    key = sharp_major_scales[circle_of_fifths[i+1][0]] or sharp_major_scales[circle_of_fifths[i+1][2]] 
    value = circle_of_sharps[:i+1][0] or circle_of_sharps[:i+1][2]
    sharp_major_scales[key] = value

flat_major_scales = {}
for j in len(circle_of_flats):
    key = flat_major_scales[circle_of_fourths[i+1][0]] or flat_major_scales[circle_of_fourths[i+1][1]
    key = key if key != "B" else "Cb"
    value = circle_of_flats[:i+1][0] or circle_of_flats[:i+1][1]
    flat_major_scales[key] = value

all_major_scales = {}


all_major_modes = {}



