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
circle_of_fifths = []
while not (circle_of_fifths and circle_of_fifths[0] == circle_of_fifths[-1] and len(circle_of_fifths) != 1):
    if not circle_of_fifths:
        circle_of_fifths.append(all_notes_db[0]) # alt: less explicitly
    else:
        last_step = find_step(circle_of_fifths[-1])
        next_step = last_step + 7 # alt ref: one fifth up
        circle_of_fifths.append(all_notes_db[next_step])
circle_of_sharps = circle_of_fifths[6:]
circle_of_fourths = circle_of_fifths[::-1]
circle_of_flats = circle_of_fourths[2:9]

### SHARP AND FLAT SCALES, ALL MODES GEN
sharp_major_scales = {}
for i in range(len(circle_of_sharps)):
    key = circle_of_fifths[i+1][0] or circle_of_fifths[i+1][2]
    value = circle_of_sharps[:i][0] or circle_of_sharps[:i][2]
    sharp_major_scales[key] = value

flat_major_scales = {}
for j in range(len(circle_of_flats)):
    key = circle_of_fourths[i+1][0] or circle_of_fourths[i+1][1]
    key = key if key != "B" else "Cb" # make better
    value = circle_of_flats[:i][0] or circle_of_flats[:i][1]
    flat_major_scales[key] = value

for i in sharp_major_scales:
    key = i
    value = []
    base_step = find_step(i)
    for k in major_steps:
        many_names = all_notes_db[(j+k)%12]

#    for j in all_notes_db:
#        if i in all_notes_db[j]:
#            for k in major_steps:
#                names = all_notes_db[(j+k)%12]
#                for x in sharp_major_scales:
#                    if sharp_major_scales[x] in names:
#                        value.append(sharp_major_scales[x])
#    all_major_scales[key] = value

for l in flat_major_scales:
    key = l
    value = []
    for m in all_notes_db:
        if l in all_major_modes[m]:
            for n in major_steps:
                names = all_notes_db[(m+n)%12]
                for y in flat_major_scales:
                    if flat_major_scales[y] in names:
                        value.append(flat_major_scales[y])
    all_major_scales[key] = value

all_major_modes = {}
for n in range(len(major_mode_names)):
    for z in all_major_scales:
        scale = all_major_scales[z]
        new_scale = scale[n:] + scale[:n]
        name = z + major_mode_names[n]



