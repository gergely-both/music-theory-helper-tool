# key or scale (terminology), 
import string
from collections import defaultdict

valid_names = string.ascii_lowercase[:7]
names_order = valid_names[2:] + valid_names[:2]
valid_symbols = {"b": -1, "#": +1}
major_steps = [0, 2, 4, 5, 7, 9, 11]
major_mode_names = ["ionian", "dorian", "phrygian", "lydian", "mixolydian", "aeolian / minor", "locrian"]
steps_names_db = defaultdict(dict)
all_existing_notes = set()
all_major_scales = {}
all_major_scales_raw = {}
all_major_modes = {}

def find_step(note):
    for x in steps_names_db:
        if note in steps_names_db[x].values():
            return x

def extend_name(name):
    for x in steps_names_db:
        many_names = list(steps_names_db[x].values())
        if name in many_names:
            return many_names


def correct_name(current_step, sharps_or_flats=False):
    all_names = steps_names_db[current_step]
    if sharps_or_flats:
        return set(all_names.values()) & set(sharps_or_flats) or all_names["unsigned"]
    else:
        return list(all_names.values())


for x, y in zip(major_steps, names_order):
    steps_names_db[x]["unsigned"] = y
for symbol in valid_symbols:
    symbol_value = valid_symbols[symbol]
    modifier = (12 + symbol_value) %12
    for name in names_order:
        orig_step = find_step(name)
        new_step = (orig_step + modifier) %12
        new_name = name + symbol
        steps_names_db[new_step][symbol] = new_name
for x in steps_names_db:
    notes = list(steps_names_db[x].values())
    for note in notes:
        all_existing_notes.add(note)


### CIRCLE OF FIFTHS, FOURTHS, SHARPS AND FLATS
all_fifths = []
while not (all_fifths and all_fifths[0] == all_fifths[-1] and len(all_fifths) != 1):
    if not all_fifths:
        all_fifths.append(steps_names_db[0])
    else:
        previous_step = find_step(all_fifths[-1].get("unsigned") or all_fifths[-1].get("#") or all_fifths[-1]("b"))
        next_step = (previous_step + 7) % 12
        all_fifths.append(steps_names_db[next_step])
circle_of_fifths = [x.get("unsigned") or x.get("#") for x in all_fifths]
circle_of_sharps = [x.get("#") for x in all_fifths[6:]]
all_fourths = all_fifths[::-1]
circle_of_fourths = [x.get("unsigned") or x.get("b") for x in all_fourths]
circle_of_flats = [x.get("b") for x in all_fourths[2:9]]


### SHARPENED / FLATTENED MAJOR SCALES START / NAME AND SHARP / FLAT MEMBERS
sharp_major_scales = {}
flat_major_scales = {}
for i in range(7):
    sharp_scale_name = circle_of_fifths[i+1]
    flat_scale_name = circle_of_fourths[i+1]
    flat_scale_name = flat_scale_name if flat_scale_name != "B" else "Cb"
    sharp_notes = circle_of_sharps[:i+1]
    flat_notes = circle_of_flats[:i+1]
    sharp_major_scales[sharp_scale_name] = sharp_notes
    flat_major_scales[flat_scale_name] = flat_notes


### ALL SCALE NAMES AND ALL THEIR MEMBERS: C MAJOR, SHARPS, FLATS
all_major_scales[names_order[0]] = [x for x in names_order]
all_major_scales_raw[names_order[0]] = []
raw_scale_notes = [extend_name(x) for x in names_order]
for notes in raw_scale_notes:
    for note in notes:
        all_major_scales_raw[names_order[0]].append(note)

    
for x, y in zip(sharp_major_scales, flat_major_scales):
    key_1 = x
    key_2 = y
    values_1 = []
    values_1_raw = []
    values_2 = []
    values_2_raw = []
    base_1 = find_step(key_1)
    base_2 = find_step(key_2)
    for step in major_steps:
        current_step_1 = (base_1 + step) % 12
        current_step_2 = (base_2 + step) % 12
        all_names_1 = correct_name(current_step_1)
        all_names_2 = correct_name(current_step_2)
        correct_name_1 = correct_name(current_step_1, sharp_major_scales[key_1])
        correct_name_2 = correct_name(current_step_2, flat_major_scales[key_2])
        values_1_raw.extend(all_names_1)
        values_2_raw.extend(all_names_2)
        values_1.append(correct_name_1)
        values_2.append(correct_name_2)
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
