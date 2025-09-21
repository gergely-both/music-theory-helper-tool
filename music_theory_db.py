# TODO: custom typing, chords correct naming, chord inversions do, classes attrs correlate, streamline flow

import string
from collections import defaultdict, namedtuple
from typing import List


SCALE_STEPS = 7  # notes in a scale
ALL_STEPS = 12  # notes in an octave
MAJOR_STEPS = [0, 2, 4, 5, 7, 9, 11]  # scale steps reflected on all steps
OCTAVES_RANGE = 8  # number of octaves in db
valid_names = string.ascii_uppercase[:SCALE_STEPS]  # usable note names
names_order = valid_names[2:] + valid_names[:2]  # to start naming from C
valid_symbols = {"b": -1, "#": +1}
Names = namedtuple("Names", "unsigned flat sharp")  # alternate (enharmonic) names
major_mode_names = [
    "ionian",
    "dorian",
    "phrygian",
    "lydian",
    "mixolydian",
    "aeolian / minor",
    "locrian",
]
steps_names_db = defaultdict(dict)  # for intermediate dictionary of steps and note names (str)
steps_notes_db = {}  # for direct dictionary of steps and note objects (MusicalNote)


class MusicalNote:
    """Musical note enumerated into steps with its names, then collected."""

    all_existing_notes = set()

    def __init__(self, step: int, names: Names):
        self.step = step
        self.all_steps: List[int] = [
            step + (x * ALL_STEPS) for x in range(OCTAVES_RANGE)
        ]
        self.enharmonics = names
        MusicalNote.all_existing_notes.add(self)

    @staticmethod
    def find_step(name: str) -> int:
        """Find the step of the note by its name."""
        for step in steps_names_db:
            if name in steps_names_db[step].values():
                return step
        raise ValueError # TODO: make better

    @staticmethod
    def find_note(x: str | int):
        """Find the note by its name or step."""
        if isinstance(x, str):
            for note in MusicalNote.all_existing_notes:
                if x in note.enharmonics:
                    return note
        elif isinstance(x, int):
            for note in MusicalNote.all_existing_notes:
                if x == note.step:
                    return note
        raise TypeError

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
    """Musical scale with its key name and notes."""

    all_existing_scales = set()

    def __init__(self, key: str, notes: List[MusicalNote]):
        self.key = key + " " + major_mode_names[0]
        self.notes = notes
        self.notes_readable: List[str] = []
        MusicalScale.all_existing_scales.add(self)


class MusicalMode:
    """ "Musical mode with its key name and notes."""

    all_existing_modes = set()

    def __init__(self, key: str, notes: List[MusicalNote], notes_readable: List[str]):
        self.key = key
        self.notes = notes
        self.notes_readable = notes_readable
        MusicalMode.all_existing_modes.add(self)


class MusicalChord:
    """Musical chord with its key, degree, and notes."""

    all_existing_chords = set()

    def __init__(self, key: str, degree, notes):
        self.key = key
        self.degree = degree
        self.degree_fmt = None
        self.notes = [MusicalNote.find_note(note) for note in notes]
        self.notes_readable = notes
        self.detect_degree()
        MusicalChord.all_existing_chords.add(self)

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
    def generate_chords(key, scale_notes):
        """Generate chords based on scale notes and scale name."""
        for i in range(len(scale_notes)):
            single_chord = [
                scale_notes[(i + j) % len(scale_notes)]
                for j in range(0, 2 * len(scale_notes), 2)
            ]
            degree = i + 1
            MusicalChord(key, degree, single_chord)


# creating MusicalNote objects
for x, y in zip(MAJOR_STEPS, names_order):
    steps_names_db[x]["unsigned"] = y
for symbol in valid_symbols:
    symbol_value = valid_symbols[symbol]
    modifier = (ALL_STEPS + symbol_value) % ALL_STEPS
    for name in names_order:
        orig_step = MusicalNote.find_step(name)
        new_step = (orig_step + modifier) % ALL_STEPS
        new_name = name + symbol
        steps_names_db[new_step][symbol] = new_name
for step in steps_names_db:
    unsigned = steps_names_db[step].get("unsigned")
    flat = steps_names_db[step].get("b")
    sharp = steps_names_db[step].get("#")
    steps_notes_db[step] = MusicalNote(step, Names(unsigned, flat, sharp))

# creating circles of fifths and fourths, also correlating sharps and flats to them
fifths_steps = []
while not (len(fifths_steps) > 1 and fifths_steps[0] == fifths_steps[-1]):
    if not fifths_steps:
        fifths_steps.append(steps_notes_db[0])
    else:
        previous_step = fifths_steps[-1].step
        next_step = (previous_step + 7) % ALL_STEPS
        fifths_steps.append(MusicalNote.find_note(next_step))
circle_of_fifths = [
    note.enharmonics.unsigned or note.enharmonics.sharp for note in fifths_steps[:-1:]
]
circle_of_sharps = [note.enharmonics.sharp for note in fifths_steps[6:]]
all_fourths = fifths_steps[::-1]
circle_of_fourths = [
    note.enharmonics.unsigned or note.enharmonics.flat for note in all_fourths
]
circle_of_flats = [note.enharmonics.flat for note in all_fourths[2:9]]

# signed notes of all signed keys (sharps for sharps, flats for flats)
sharp_keys_sharp_notes = {}
flat_keys_flat_notes = {}
for i in range(SCALE_STEPS):
    sharp_scale_name = circle_of_fifths[i + 1]
    flat_scale_name = circle_of_fourths[i + 1]
    flat_scale_name = flat_scale_name if flat_scale_name != "B" else "Cb"
    sharp_notes = circle_of_sharps[: i + 1]
    flat_notes = circle_of_flats[: i + 1]
    sharp_keys_sharp_notes[sharp_scale_name] = sharp_notes
    flat_keys_flat_notes[flat_scale_name] = flat_notes

# creating all major scales and collecting them
new_scale_obj = MusicalScale(
    names_order[0], [MusicalNote.find_note(name) for name in names_order]
)
new_scale_obj.notes_readable = [
    note.enharmonics.unsigned for note in new_scale_obj.notes
]
for keys_signs_pairs in [sharp_keys_sharp_notes, flat_keys_flat_notes]:
    for key in keys_signs_pairs:
        keys_notes = []
        corrected_names = []
        base_step = MusicalNote.find_step(key)
        for step in MAJOR_STEPS:
            current_step = (base_step + step) % ALL_STEPS
            note = steps_notes_db[current_step]
            appropriate_name = MusicalNote.appropriate_name(note, keys_signs_pairs[key])
            keys_notes.append(note)
            corrected_names.append(appropriate_name)
        new_scale_obj = MusicalScale(key, keys_notes)
        new_scale_obj.notes_readable = corrected_names

# creating all modes from scales, ionian excluded (equals scale itself)
for scale in MusicalScale.all_existing_scales:
    for i in range(1, len(major_mode_names)):
        mode_notes = scale.notes[i:] + scale.notes[:i]
        mode_notes_readable = scale.notes_readable[i:] + scale.notes_readable[:i]
        mode_name = mode_notes_readable[0] + " " + major_mode_names[i]
        MusicalMode(mode_name, mode_notes, mode_notes_readable)

# creating chord degrees by all scales and modes
for scale in MusicalScale.all_existing_scales:
    MusicalChord.generate_chords(scale.key, scale.notes_readable)
for mode in MusicalMode.all_existing_modes:
    MusicalChord.generate_chords(mode.key, mode.notes_readable)
