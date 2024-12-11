from music_theory_db import MusicalNote, MusicalScale, MusicalMode, MusicalChord
from typing import List


user_selection = []
scales_found = []
modes_found = []
chords_found = []


# NOTE: is len(scales_found) always == 1 info
def find_all(notes_selection: List[MusicalNote]) -> None:
    """Finds scales and modes by user MusicalNote objects selection."""
    # finding exact scale matches for first note exactly and others' subset
    for scale in MusicalScale.all_existing_scales:
        if (
            set(notes_selection).issubset(scale.notes)
            and notes_selection[0] is scale.notes[0]
        ):
            scales_found.append(scale)
            # print(scale.key)

    # finding modes by first note matches and others' subsets
    for mode in MusicalMode.all_existing_modes:
        if set(notes_selection).issubset(mode.notes):
            if any(
                name == mode.notes_readable[0] for name in user_selection[0].enharmonics
            ):
                modes_found.append(mode)
                # print(mode.key)

    # finding chords of same key among found scales
    for scale in scales_found:
        for chord in MusicalChord.all_existing_chords:
            if chord.key == scale.key:
                chords_found.append(chord)

    # finding chords of same key among found modes
    for mode in modes_found:
        for chord in MusicalChord.all_existing_chords:
            if chord.key == mode.key:
                chords_found.append(chord)


# TODO: output formatting improvements
def display_results():
    """Displays query results of user interaction."""
    if scales_found:
        print("\nProper scales correlated:")
        for scale in scales_found:
            print(scale.key + ": " + ", ".join(scale.notes_readable))
    if modes_found:
        print("\nThe following modes are available:")
        for mode in modes_found:
            print(mode.key + ": " + ", ".join(mode.notes_readable))
    if chords_found:
        print("\nThe following chords are available:")
        for chord in chords_found:
            print(
                chord.key
                + " - "
                + chord.degree_fmt
                + ": "
                + ", ".join(chord.notes_readable)
            )


def notes_input_mode():
    # entering the starting note
    note_selected = False
    while not note_selected:
        response = input("Enter starting note: ").title()
        starting_note = MusicalNote.find_note(response)
        if starting_note:
            user_selection.append(starting_note)
            note_selected = True
        else:
            print("Try something different.")

    # TODO: revise
    # entering additional notes
    more_notes_selected = False
    while not more_notes_selected:
        response_2 = input(
            "Enter additional notes you know play well alongside (comma-separated): "
        ).title()
        other_notes = set(x.strip() for x in response_2.split(","))
        more_notes = [MusicalNote.find_note(name) for name in other_notes]
        if all(more_notes):
            user_selection.extend(more_notes)
            more_notes_selected = True
        else:
            print("Something's incorrect. Try again.")
    return True


if __name__ == "__main__":
    notes_input_mode()
    find_all(user_selection)
    display_results()
