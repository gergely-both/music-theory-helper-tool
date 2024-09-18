# TODO: correct fmt of ninth / eleventh / thirteenth / sus / inversions...

import string
from collections import defaultdict, namedtuple
from typing import List, Dict


MAIN_STEPS = 7
ALL_STEPS = 12
OCTAVES_RANGE = 8


valid_names = string.ascii_uppercase[:MAIN_STEPS]
names_order = valid_names[2:] + valid_names[:2]
valid_symbols = {"b": -1, "#": +1}
Names = namedtuple("Names", "unsigned flat sharp")

major_steps = [0, 2, 4, 5, 7, 9, 11]
major_mode_names = [
    "ionian",
    "dorian",
    "phrygian",
    "lydian",
    "mixolydian",
    "aeolian / minor",
    "locrian",
]

steps_names_db = defaultdict(dict)
steps_notes_db = {}

all_existing_notes = set()
all_existing_scales = set()
all_existing_chords = set()


class MusicalNote:
    """Musical note with its step and names."""

    def __init__(self, step: int, names: Names):
        self.step = step
        self.all_steps : List[int] = [step+(x*ALL_STEPS) for x in range(OCTAVES_RANGE)]      
        self.enharmonics = names

    @staticmethod
    def find_step(name) -> int:
        """Find the step of the note by its name."""
        for step in steps_names_db:
            if name in steps_names_db[step].values():
                return step

    @staticmethod
    def find_note(x):
        """Find the note by its name or step."""
        if isinstance(x, str):
            for note in all_existing_notes:
                if x in note.enharmonics:
                    return note
        elif isinstance(x, int):
            for note in all_existing_notes:
                if x == note.step:
                    return note

    @staticmethod
    def appropriate_name(note, signs):
        """Correct the name of the note by its signs."""
        corrected_nameset = set(note.enharmonics) & set(signs)
        if corrected_nameset:
            for corrected_name in corrected_nameset:
                return corrected_name
        else:
            return note.enharmonics.unsigned


class MusicalScale:
    """Musical scale with its name and notes."""

    def __init__(self, key: str, notes: MusicalNote):
        self.key = key + " major / ionian"
        self.notes = notes
        self.notes_readable : List[str]= []
        self.modes : Dict[str, str] = []


class MusicalChord:
    """Musical chord with its key, degree, and notes."""

    def __init__(self, key: str, degree, notes):
        self.key = key
        self.degree = degree
        self.degree_fmt = None
        self.notes_readable = notes
        self.notes = [MusicalNote.find_note(note) for note in notes]
        self.detect_degree()

    # arabic to roman numerals
    @staticmethod
    def arabic_to_roman(n):
        numerals = ["I", "II", "III", "IV", "V", "VI", "VII"]
        return numerals[n - 1]

    @staticmethod
    def steps_diff(note_low, note_hi):
        """Calculate the difference in steps between two notes."""
        return (12 + note_hi.step - note_low.step) % 12

    def detect_degree(self):
        """Detect the degree of the chord (based on the key)."""
        third_steps = self.steps_diff(self.notes[0], self.notes[1])
        fifth_steps = self.steps_diff(self.notes[0], self.notes[2])
        seventh_steps = self.steps_diff(self.notes[0], self.notes[3])
        degree_roman = (
            self.arabic_to_roman(self.degree).upper()
            if third_steps == 4
            else self.arabic_to_roman(self.degree).lower()
        )
        symbol = ""
        if fifth_steps > 7:
            symbol = "+"
        elif fifth_steps < 7:
            symbol = "°"
        if seventh_steps == 11:
            symbol += "(Maj7)"
        elif seventh_steps == 10:
            symbol += "(min7)"
        self.degree_fmt = degree_roman + symbol if symbol else degree_roman

    @staticmethod
    def generate_chords(scale_notes, key):
        """Generate chords based on scale notes and scale name."""
        for i in range(len(scale_notes)):
            single_chord = [
                scale_notes[(i + j) % len(scale_notes)]
                for j in range(0, 2 * len(scale_notes), 2)
            ]
            degree = i + 1
            all_existing_chords.add(MusicalChord(key, degree, single_chord))


# CREATING MusicalNote OBJECTS 
### first it creates database of int: str
for x, y in zip(major_steps, names_order):
    steps_names_db[x]["unsigned"] = y
for symbol in valid_symbols:
    symbol_value = valid_symbols[symbol]
    modifier = (ALL_STEPS + symbol_value) % ALL_STEPS
    for name in names_order:
        orig_step = MusicalNote.find_step(name)
        new_step = (orig_step + modifier) % ALL_STEPS
        new_name = name + symbol
        steps_names_db[new_step][symbol] = new_name
### then it creates database of int: MusicalNote 
for step in steps_names_db:
    unsigned = steps_names_db[step].get("unsigned")
    flat = steps_names_db[step].get("b")
    sharp = steps_names_db[step].get("#")
    steps_notes_db[step] = MusicalNote(step, Names(unsigned, flat, sharp))
all_existing_notes = set(note for note in steps_notes_db.values())


# CREATING CIRCLES AS LISTS OF STRINGS
### circle of fifths and sharps derived from all fifths
all_fifths = []
while not (all_fifths and all_fifths[0] == all_fifths[-1] and len(all_fifths) > 1):
    if not all_fifths:
        all_fifths.append(steps_notes_db[0])
    else:
        previous_step = all_fifths[-1].step
        next_step = (previous_step + 7) % ALL_STEPS
        all_fifths.append(MusicalNote.find_note(next_step))
circle_of_fifths = [note.enharmonics.unsigned or note.enharmonics.sharp for note in all_fifths[:-1:]]
circle_of_sharps = [note.enharmonics.sharp for note in all_fifths[6:]]
### circle of fourths and flats derived from all fourths derived from all fifths
all_fourths = all_fifths[::-1]
circle_of_fourths = [note.enharmonics.unsigned or note.enharmonics.flat for note in all_fourths]
circle_of_flats = [note.enharmonics.flat for note in all_fourths[2:9]]


# CREATING DICTS FOR SIGNED KEYS WITH APPLICABLE SIGNED NOTES
### a dict for sharp-signed keys with applicable sharp notes
sharp_keys_sharp_notes = {}
### a dict for flat-signed keys with applicable flat notes
flat_keys_flat_notes = {}
for i in range(MAIN_STEPS):
    sharp_scale_name = circle_of_fifths[i + 1]
    flat_scale_name = circle_of_fourths[i + 1]
    flat_scale_name = flat_scale_name if flat_scale_name != "B" else "Cb"
    sharp_notes = circle_of_sharps[: i + 1]
    flat_notes = circle_of_flats[: i + 1]
    sharp_keys_sharp_notes[sharp_scale_name] = sharp_notes
    flat_keys_flat_notes[flat_scale_name] = flat_notes


# CREATING ALL MAJOR SCALES AND COLLECTING THEM
### the unsigned c major scale
new_scale_obj = MusicalScale(names_order[0], [MusicalNote.find_note(name) for name in names_order])
new_scale_obj.notes_readable = [note.enharmonics.unsigned for note in new_scale_obj.notes]
all_existing_scales.add(new_scale_obj)
### sharp and flat major scales
for keys_signs_pairs in [sharp_keys_sharp_notes, flat_keys_flat_notes]:
    for key in keys_signs_pairs:
        keys_notes = []
        corrected_names = []
        base_step = MusicalNote.find_step(key)
        for step in major_steps:
            current_step = (base_step + step) % ALL_STEPS
            note = steps_notes_db[current_step]
            appropriate_name = MusicalNote.appropriate_name(note, keys_signs_pairs[key])
            keys_notes.append(note)
            corrected_names.append(appropriate_name)
        new_scale_obj = MusicalScale(key, keys_notes)
        new_scale_obj.notes_readable = corrected_names
        all_existing_scales.add(new_scale_obj)


# CREATING MODES FOR SCALES AND ATTRIBUTING THEM
for scale in all_existing_scales:
    for i in range(1, len(major_mode_names)):
        mode_notes = scale.notes_readable[i:] + scale.notes_readable[:i]
        mode_name = mode_notes[0] + " " + major_mode_names[i]
        scale.modes.append({mode_name: mode_notes})


# CREATING CHORD DEGREES FOR SCALES AND THEIR MODES
for scale in all_existing_scales:
    MusicalChord.generate_chords(scale.notes_readable, scale.key)
    for mode in scale.modes:
        for subname, subscale in mode.items():
            MusicalChord.generate_chords(subscale, subname)


# print([(chord.key, chord.degree_fmt, chord.notes_readable) for chord in all_existing_chords])
# print([(scale.key, scale.notes_readable, scale.modes) for scale in all_existing_scales])
