from music_theory_db import MusicalNote, MusicalScale, MusicalMode, MusicalChord
from typing import List


user_selection = []
scales_found = []
modes_found = []
chords_found = []


def interface_user():
    """Interacts with user, understanding their input."""
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

    # entering additional notes
    more_notes_selected = False
    while not more_notes_selected:
        response_2_raw = input(
            "Enter additional notes you know play well alongside (comma-separated): "
        ).title()
        response_2 = set(x.strip() for x in response_2_raw.split(","))
        more_notes = [MusicalNote.find_note(name) for name in response_2]
        if all(more_notes):
            user_selection.extend(more_notes)
            more_notes_selected = True
        else:
            print("Something's incorrect. Try again.")
    return True


def query_db(notes_selection: List[MusicalNote]) -> None:
    """Finds scales, modes and chords for user note selection, collects them by type."""
    # looking up matching scales (aka ionian modes)
    for scale in MusicalScale.all_existing_scales:
        if (
            set(notes_selection).issubset(scale.notes)
            and notes_selection[0] is scale.notes[0]
        ):
            scales_found.append(scale)

    # looking up matching modes (ionian excluded)
    for mode in MusicalMode.all_existing_modes:
        if (
            set(notes_selection).issubset(mode.notes)
            and notes_selection[0] is mode.notes[0]
        ):
            modes_found.append(mode)

    # looking up corresponding chords for scales and modes found above, by key
    for chord in MusicalChord.all_existing_chords:
        for scale in scales_found:
            if chord.key == scale.key:
                chords_found.append(chord)
        for mode in modes_found:
            if chord.key == mode.key:
                chords_found.append(chord)


def display_results():
    """Displays db feedback for user interaction."""
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


if __name__ == "__main__":
    interface_user()
    query_db(user_selection)
    display_results()
