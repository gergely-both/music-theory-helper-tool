#TODO: enharmony grouping system: namedtuple, simplify, GTR tab, piano keys, chords, chord progressions, aeolian = minor, 
import string

valid_names = string.ascii_uppercase[:6]
names_order = valid_names[2:] + valid_names[:2]
valid_symbols = {"b": -1, "#": +1}
major_steps = [0, 2, 4, 5, 7, 9, 11]
major_mode_names = ["ionian", "dorian", "phrygian", "lydian", "mixolydian", "aeolian", "locrian"]
all_notes_db = {}
all_major_scales = {}
all_major_modes = {}

def find_step(note):
    for x in all_notes_db:
        if note in all_notes_db[x]:
            return x

### C MAJOR SCALE / WHITE KEYS ONLY + ADD TO ALL SCALES, BLACK KEYS PLUS ENHARMONICS
for x,y in zip(major_steps, names_order):
    all_notes_db[x] = list(y)
all_major_scales.update(all_notes_db)
for symbol in valid_symbols:
    symbol_value = valid_symbols[symbol]
    modifier = (12 + symbol_value) % 12 # other solution?
    for name in names_order:
        orig_step = find_step(name)
        new_step = orig_step + modifier
        new_name = name + symbol
        if new_step in all_notes_db:
            all_notes_db[new_step].append(new_name)
        else:
            all_notes_db[new_step] = list(None, new_name) # other solution?

### CIRCLES OF FIFTH, FOURTH, SHARPS, FLATS
all_fifths = []
while not (all_fifths and all_fifths[0] == all_fifths[-1] and len(all_fifths) != 1):
    if not all_fifths:
        all_fifths.append(all_notes_db[0]) # alt: less explicitly
    else:
        last_step = find_step(all_fifths[-1])
        next_step = last_step + 7 # alt ref: one fifth up
        all_fifths.append(all_notes_db[next_step])
circle_of_fifths = [(x[0] or x[2]) for x in all_fifths]
circle_of_sharps = [x[2] for x in all_fifths[6:]]
all_fourths = all_fifths[::-1]
circle_of_fourths = [(x[0] or x[1]) for x in all_fourths]
circle_of_flats = [x[1] for x in all_fourths[2:9]]

### SHARPENED / FLATTENED MAJOR SCALES START / NAME AND SHARP / FLAT MEMBERS
sharp_major_scales = {}
for i in range(len(circle_of_sharps)):
    key = circle_of_fifths[i+1]
    value = circle_of_sharps[:i]
    sharp_major_scales[key] = value

flat_major_scales = {}
for j in range(len(circle_of_flats)):
    key = circle_of_fourths[i+1]
    key = key if key != "B" else "Cb" # make better
    value = circle_of_flats[:i]
    flat_major_scales[key] = value

def find_correct_name(names, scale_type):
        for x in scale_type:
            for y in names:
                for z in scale_type[x]:
                    if y == z:
                        return z

### SHARP AND FLAT SCALES NAMES AND ALL THEIR MEMBERS 
#TODO merge all dicts somehow?
for x in sharp_major_scales: # combine both major types (sharp, flat)?
    key = x
    values = []
    base = find_step(key)
    for step in major_steps:
        many_names = all_notes_db[(base + step)%12]
        values.append(find_correct_name(many_names, sharp_major_scales)
        all_major_scales[key] = values

for y in flat_major_scales:
    key = y
    values = []
    base = find_step(key)
    for step in major_steps:
        many_names = all_notes_db[(base + step)%12]
        values.append(find_correct_name(many_names, flat_major_scales)
        all_major_scales[key] = values

all_major_modes = {}
for n in range(len(major_mode_names)):
    for z in all_major_scales:
        scale = all_major_scales[z]
        new_scale = scale[n:] + scale[:n]
        name = z + major_mode_names[n]



