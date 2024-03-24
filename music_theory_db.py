# TODO: custom typing, inheritance (multiple perhaps), roman numbers, inversions, name in progression, 

import string
from collections import defaultdict, namedtuple

FULL_STEPS = 7
HALF_STEPS = 12
Names = namedtuple("Names", "unsigned flat sharp")

valid_names = string.ascii_uppercase[:FULL_STEPS]
names_order = valid_names[2:] + valid_names[:2]
valid_symbols = {"b": -1, "#": +1}
major_steps = [0, 2, 4, 5, 7, 9, 11]
major_mode_names = ["ionian", "dorian", "phrygian", "lydian", "mixolydian", "aeolian / minor", "locrian"]

steps_names_db = defaultdict(dict)
steps_notes_db = {}

all_existing_notes = set()
all_existing_scales = set()
all_existing_chords = set()

all_scales_raw = {}
all_scales_corrected = {}
all_modes = {}


def find_step(name):
    for step in steps_names_db:
        if name in steps_names_db[step].values():
            return step

class MusicalScale:
    def __init__(self, name, notes):
        self.name = name
        self.notes = notes
        
class MusicalNote:
    def __init__(self, step, names):
        self.step = step
        self.names = names


class MusicalChord:
    def __init__(self, key, stage, notes):
        self.key = key
        self.stage = stage
        self.notes = notes

    def name_chord(self):
        pass

    def number_chord(self):
        pass

    def name_inversion(self):
        pass

    
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


### making steps_names_db: all 12 half-steps with enharmonic names
for x, y in zip(major_steps, names_order):
    steps_names_db[x]["unsigned"] = y
for symbol in valid_symbols:
    symbol_value = valid_symbols[symbol]
    modifier = (HALF_STEPS + symbol_value) % HALF_STEPS
    for name in names_order:
        orig_step = find_step(name)
        new_step = (orig_step + modifier) % HALF_STEPS
        new_name = name + symbol
        steps_names_db[new_step][symbol] = new_name

for step in steps_names_db:
    unsigned = steps_names_db[step].get("unsigned")
    flat = steps_names_db[step].get("b")
    sharp = steps_names_db[step].get("#")
    steps_notes_db[step] = MusicalNote(step, Names(unsigned, flat, sharp))

all_existing_notes = set(note for note in steps_notes_db.values())


### circles of fifths, fourths, sharps and flats
all_fifths = []
while not (all_fifths and all_fifths[0] == all_fifths[-1] and len(all_fifths) > 1):
    if not all_fifths:
        all_fifths.append(steps_notes_db[0])
    else:
        previous_step = all_fifths[-1].step
        next_step = (previous_step + 7) % HALF_STEPS
        all_fifths.append(find_note(next_step))
circle_of_fifths = [note.names.unsigned or note.names.sharp for note in all_fifths[:-1:]]
circle_of_sharps = [note.names.sharp for note in all_fifths[6:]]
all_fourths = all_fifths[::-1]
circle_of_fourths = [note.names.unsigned or note.names.flat for note in all_fourths]
circle_of_flats = [note.names.flat for note in all_fourths[2:9]]


### all sharp and flat scales and their signed members
sharp_keys_sharps = {}
flat_keys_flats = {}
for i in range(FULL_STEPS):
    sharp_scale_name = circle_of_fifths[i+1]
    flat_scale_name = circle_of_fourths[i+1] 
    flat_scale_name = flat_scale_name if flat_scale_name != "B" else "Cb" 
    sharp_notes = circle_of_sharps[:i+1]
    flat_notes = circle_of_flats[:i+1]
    sharp_keys_sharps[sharp_scale_name] = sharp_notes
    flat_keys_flats[flat_scale_name] = flat_notes


### all basic keys and their members, corrected names, beginning with c major
all_scales_raw[names_order[0]] = [find_note(name) for name in names_order]
for key, notes in all_scales_raw.items():
   all_scales_corrected[key] = [note.names.unsigned for note in notes]

for keys_signs_pairs in [sharp_keys_sharps, flat_keys_flats]:
    for key in keys_signs_pairs:
        key_notes = []
        corrected_names = []
        base_step = find_step(key)
        for step in major_steps:
            current_step = (base_step + step) % HALF_STEPS
            note = steps_notes_db[current_step]
            corrected_name = correct_name(note, keys_signs_pairs[key])
            key_notes.append(note)
            corrected_names.append(corrected_name)
        all_scales_raw[key] = key_notes
        all_scales_corrected[key] = corrected_names
        # all_existing_scales.add(MusicalScale(key + " major scale: ", key_notes))


### all major modes, omitting ionian (is major scale)
for i in range(1, len(major_mode_names)):
    for key_name, scale in all_scales_corrected.items():
        new_scale = scale[i:] + scale[:i]
        key_name = new_scale[0] + " " + major_mode_names[i]
        all_modes[key_name] = new_scale


### all major and mode chord notes with name and stage
all_thirds = {}
all_mode_thirds = {}
for scale, result_dict in [(all_scales_corrected, all_thirds), (all_modes, all_mode_thirds)]:
    for key, notes in scale.items():
        all_chords = []
        for i in range(len(notes)):
            single_chord = []
            for j in range(0, 2*len(notes), 2):
                chord_note = notes[(i+j) % len(notes)]
                single_chord.append(chord_note)
            all_chords.append(tuple(single_chord))
            all_existing_chords.add(MusicalChord(key, i+1, single_chord))
        result_dict[key] = all_chords

print([(chord.key, chord.stage, chord.notes) for chord in all_existing_chords])


