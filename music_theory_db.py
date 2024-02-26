#TODO: editable named enharmony grouping, guitar tab, piano keys, chords, chord progressions, OOP, 
import string

valid_names = string.ascii_uppercase[:6]
names_order = valid_names[2:] + valid_names[:2]
valid_symbols = {"b": -1, "#": +1}
major_steps = [0, 2, 4, 5, 7, 9, 11]
major_mode_names = ["ionian", "dorian", "phrygian", "lydian", "mixolydian", "aeolian / minor", "locrian"]
steps_names_db = {}
all_existing_notes = set(x.casefold() for x in *steps_names_db.values())
all_major_scales = {}
all_major_scales_raw = {}
all_major_modes = {}

def find_step(note):
    for x in steps_names_db:
        if note in steps_names_db[x]:
            return x

def shrink_name(enh_names, scale_type):
    enh_names = set(enh_names)
    for x in scale_type:
        mod_names = set(scale_type[x])
        if mod_names & enh_names:
            return mod_names & enh_names

for x,y in zip(major_steps, names_order):
    steps_names_db[x] = list(y)
for symbol in valid_symbols:
    symbol_value = valid_symbols[symbol]
    modifier = (12 + symbol_value) % 12 # other solution?
    for name in names_order:
        orig_step = find_step(name)
        new_step = orig_step + modifier
        new_name = name + symbol
        if new_step in steps_names_db:
            steps_names_db[new_step].append(new_name)
        else:
            steps_names_db[new_step] = list(None, new_name) # named solution?

### CIRCLE OF FIFTHS, FOURTHS, SHARPS AND FLATS
all_fifths = []
while not (all_fifths and all_fifths[0] == all_fifths[-1] and len(all_fifths) != 1):
    if not all_fifths:
        first = find_step(names_order[0])
        all_fifths.append(first)
    else:
        last_step = find_step(all_fifths[-1])
        next_step = last_step + 7 # alt ref: one fifth up
        all_fifths.append(steps_names_db[next_step])
circle_of_fifths = [(x[0] or x[2]) for x in all_fifths]
circle_of_sharps = [x[2] for x in all_fifths[6:]]
all_fourths = all_fifths[::-1]
circle_of_fourths = [(x[0] or x[1]) for x in all_fourths]
circle_of_flats = [x[1] for x in all_fourths[2:9]]

### SHARPENED / FLATTENED MAJOR SCALES START / NAME AND SHARP / FLAT MEMBERS
sharp_major_scales = {}
flat_major_scales = {}
for i in range(8):
    key_1 = circle_of_fifths[i+1]
    key_2 = circle_of_fourths[i+1]
    key_2 = key_2 if key_2 != "B" else "Cb" #TODO: make into objs
    values_1 = circle_of_sharps[:i]
    values_2 = circle_of_flats[:i]
    sharp_major_scales[key_1] = values_1
    flat_major_scales[key_2] = values_2

### ALL SCALE NAMES AND ALL THEIR MEMBERS: C MAJOR, SHARPS, FLATS
all_major_scales[names_order[0]] = [x for x in names_order]
for x,y in zip(sharp_major_scales, flat_major_scales):
    key_1 = x
    key_2 = y
    values_1 = []
    values_1_raw = []
    values_2 = []
    values_2_raw = []
    base_1 = find_step(key_1)
    base_2 = find_step(key_2)
    for step in major_steps:
        many_names_1 = steps_names_db[(base_1 + step)%12]
        many_names_2 = steps_names_db[(base_2 + step)%12]
        values_1_raw.append(many_names_1)
        values_2_raw.append(many_names_2)
        values_1.append(shrink_name(many_names_1, sharp_major_scales)
        values_2.append(shrink_name(many_names_2, flat_major_scales))
        all_major_scales_raw[key_1] = values_1_raw
        all_major_scales_raw[key_2] = values_2_raw
        all_major_scales[key_1] = values_1
        all_major_scales[key_2] = values_2

### ALL MAJOR MODES GEN
all_major_modes = {}
for n in range(len(major_mode_names)):
    for z in all_major_scales:
        scale = all_major_scales[z]
        new_scale = scale[n:] + scale[:n]
        name = z + major_mode_names[n]

