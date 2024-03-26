# TODO: custom typing, inheritance (multiple perhaps), inversions def, name in progression for augmented and diminished chords, 

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


class MusicalScale:
    def __init__(self, name, notes):
        self.name = name
        self.notes = notes
        self.notes_mod = []
        self.modes = []

    def __repr__(self):
        return self.name + " major scale"

class MusicalNote:
    def __init__(self, step, names):
        self.step = step
        self.names = names

    @staticmethod
    def find_step(name):
        for step in steps_names_db:
            if name in steps_names_db[step].values():
                return step
    
    @staticmethod
    def find_note(x):
        if isinstance(x, str):
            for note in all_existing_notes:
                if x in note.names:
                    return note
        elif isinstance(x, int):
            for note in all_existing_notes:
                if x == note.step:
                    return note

    # @staticmethod
    # def extend_name(name):
    #     for note in all_existing_notes:
    #         if name in note.names:
    #             return note.names

    @staticmethod
    def correct_name(note, signs):
        corrected_nameset = set(note.names) & set(signs)
        if corrected_nameset:
            for corrected_name in corrected_nameset:
                return corrected_name
        else:
            return note.names.unsigned

class MusicalChord:
    def __init__(self, key, degree, notes):
        self.key = key
        self.degree = degree
        self.notes_mod = notes
        self.notes = [MusicalNote.find_note(note) for note in notes]
    
    @classmethod
    def steps_diff(cls, note_low, note_hi):
        return (12 + note_hi.step - note_low.step) % 12

    def name_chord(self):
        pass

    def number_chord(self):
        pass

    def name_inversion(self):
        pass



### making steps_names_db: all 12 half-steps with enharmonic names
for x, y in zip(major_steps, names_order):
    steps_names_db[x]["unsigned"] = y
for symbol in valid_symbols:
    symbol_value = valid_symbols[symbol]
    modifier = (HALF_STEPS + symbol_value) % HALF_STEPS
    for name in names_order:
        orig_step = MusicalNote.find_step(name)
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
        all_fifths.append(MusicalNote.find_note(next_step))
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
new_scale_obj = MusicalScale(names_order[0], [MusicalNote.find_note(name) for name in names_order])
new_scale_obj.notes_mod = [note.names.unsigned for note in new_scale_obj.notes]
all_existing_scales.add(new_scale_obj)   
for keys_signs_pairs in [sharp_keys_sharps, flat_keys_flats]:
    for key in keys_signs_pairs:
        key_notes = []
        corrected_names = []
        base_step = MusicalNote.find_step(key)
        for step in major_steps:
            current_step = (base_step + step) % HALF_STEPS
            note = steps_notes_db[current_step]
            corrected_name = MusicalNote.correct_name(note, keys_signs_pairs[key])
            key_notes.append(note)
            corrected_names.append(corrected_name)
        new_scale_obj = MusicalScale(key, key_notes)
        new_scale_obj.notes_mod = corrected_names
        all_existing_scales.add(new_scale_obj)


### all major modes, omitting ionian (equals basic major scale)
for i in range(1, len(major_mode_names)):
    for scale in all_existing_scales:
        mode_notes = scale.notes_mod[i:] + scale.notes_mod[:i]
        mode_name = mode_notes[0] + " " + major_mode_names[i]
        scale.modes.append({mode_name: mode_notes})

# arabic to roman numerals
def arabic_to_roman(n):
    numerals = ["I", "II", "III", "IV", "V", "VI", "VII"]
    return numerals[n-1]

def generate_chords(scale_notes, scale_name):
    """Generate chords based on scale notes and scale name."""
    for i in range(len(scale_notes)):
        single_chord = [scale_notes[(i+j) % len(scale_notes)] for j in range(0, 2*len(scale_notes), 2)]
        single_chord_objs = [MusicalNote.find_note(note) for note in single_chord]
        degree = (arabic_to_roman(i+1)).lower() if MusicalChord.steps_diff(single_chord_objs[0], single_chord_objs[1]) == 3 else arabic_to_roman(i+1).upper()
        all_existing_chords.add(MusicalChord(scale_name, degree, single_chord))

# Iterate over all major and mode chord scales with names and degrees
for scale in all_existing_scales:
    # Generate chords for the main scale
    generate_chords(scale.notes_mod, scale.name)
    
    # Generate chords for each mode in the scale
    for mode in scale.modes:
        for subname, subscale in mode.items():
            generate_chords(subscale, subname)

# Print all existing chords
print([(chord.key, chord.degree, chord.notes_mod) for chord in all_existing_chords])

