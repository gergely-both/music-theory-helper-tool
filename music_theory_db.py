import string
from collections import defaultdict, namedtuple

Names = namedtuple("Names", "unsigned flat sharp")

valid_names = string.ascii_uppercase[:7]
names_order = valid_names[2:] + valid_names[:2]
valid_symbols = {"b": -1, "#": +1}
major_steps = [0, 2, 4, 5, 7, 9, 11]
major_mode_names = ["ionian", "dorian", "phrygian", "lydian", "mixolydian", "aeolian / minor", "locrian"]

steps_names_db = defaultdict(dict)
steps_notes_db = {}
all_existing_notes = set()
all_major_scales = {}
all_major_scales_mod = {}
all_major_modes = {}


def find_step(name):
    for step in steps_names_db:
        if name in steps_names_db[step].values():
            return step


class MusicalNote:
    def __init__(self, step, names):
        self.step = step
        self.names = names


def find_note(x):
    if isinstance(x, str):
        for note in all_existing_notes:
            if x in note.names:
                return note
    elif isinstance(x, int):
        for note in all_existing_notes:
            if x == note.step:
                return note


def extend_name(name):
    for note in all_existing_notes:
        if name in note.names:
            return note.names


def correct_name(note, signs):
    corrected_nameset = set(note.names) & set(signs)
    if corrected_nameset:
        for corrected_name in corrected_nameset:
            return corrected_name
    else:
        return note.names.unsigned


# MAKING steps_names_db: 12 STEPS, ALL ENHARMONIC NAMES
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

for step in steps_names_db:
    unsigned = steps_names_db[step].get("unsigned")
    flat = steps_names_db[step].get("b")
    sharp = steps_names_db[step].get("#")
    steps_notes_db[step] = MusicalNote(step, Names(unsigned, flat, sharp))

all_existing_notes = set(note for note in steps_notes_db.values())


### CIRCLE OF FIFTHS, FOURTHS, SHARPS AND FLATS
all_fifths = []
while not (all_fifths and all_fifths[0] == all_fifths[-1] and len(all_fifths) != 1):
    if not all_fifths:
        all_fifths.append(steps_notes_db[0])
    else:
        previous_step = all_fifths[-1].step
        next_step = (previous_step + 7) % 12
        all_fifths.append(find_note(next_step))
circle_of_fifths = [note.names.unsigned or note.names.sharp for note in all_fifths]
circle_of_sharps = [note.names.sharp for note in all_fifths[6:]]
all_fourths = all_fifths[::-1]
circle_of_fourths = [note.names.unsigned or note.names.flat for note in all_fourths]
circle_of_flats = [note.names.flat for note in all_fourths[2:9]]


### SHARPENED / FLATTENED MAJOR SCALES START / NAME AND SHARP / FLAT MEMBERS
sharp_keys_sharps = {}
flat_keys_flats = {}
for i in range(7):
    sharp_scale_name = circle_of_fifths[i+1]
    flat_scale_name = flat_scale_name := circle_of_fourths[i+1] if flat_scale_name != "B" else "Cb"
    sharp_notes = circle_of_sharps[:i+1]
    flat_notes = circle_of_flats[:i+1]
    sharp_keys_sharps[sharp_scale_name] = sharp_notes
    flat_keys_flats[flat_scale_name] = flat_notes


### ALL KEY NAMES AND ALL THEIR MEMBERS GEN, with objects + with correct naming system
all_major_scales[names_order[0]] = [find_note(name) for name in names_order]
for signed_keys_signs in sharp_keys_sharps, flat_keys_flats:
    for signed_key in signed_keys_signs:
        signed_key_notes = []
        signed_key_corrected_names = []
        signed_key_base_step = find_step(signed_key)
        for step in major_steps:
            signed_current_step = (signed_key_base_step + step) % 12
            signed_key_note = steps_notes_db[signed_current_step]
            signed_corrected_name = correct_name(signed_key_note, signed_keys_signs[signed_key])
            signed_key_notes.append(signed_key_note)
            signed_key_corrected_names.append(signed_corrected_name)
        all_major_scales[signed_key] = signed_key_notes
        all_major_scales_mod[signed_key] = signed_key_corrected_names


### ALL MAJOR MODES GEN: skipping ionian with 1 in range (reason: equals basic major scale)
for i in range(1, len(major_mode_names)):
    for key_name, scale in all_major_scales_mod.items():
        new_scale = scale[i:] + scale[:i]
        key_name = new_scale[0] + " " + major_mode_names[i]
        all_major_modes[key_name] = new_scale

