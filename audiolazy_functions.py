#https://github.com/danilobellini/audiolazy/blob/master/audiolazy/lazy_midi.py

import itertools as it
from math import log2, isinf, isnan

# Useful constants
MIDI_A4 = 69   # MIDI Pitch number
FREQ_A4 = 440. # Hz
SEMITONE_RATIO = 2. ** (1. / 12.) # Ascending

def midi2freq(midi_number):
    """
    Given a MIDI pitch number, returns its frequency in Hz.
    """
    return FREQ_A4 * 2 ** ((midi_number - MIDI_A4) * (1./12.))


def str2midi(note_string):
    """
    Given a note string name (e.g. "Bb4"), returns its MIDI pitch number.
    """
    if note_string == "?":
        return nan
    data = note_string.strip().lower()
    name2delta = {"c": -9, "d": -7, "e": -5, "f": -4, "g": -2, "a": 0, "b": 2}
    accident2delta = {"b": -1, "#": 1, "x": 2}
    accidents = list(it.takewhile(lambda el: el in accident2delta, data[1:]))
    octave_delta = int(data[len(accidents) + 1:]) - 4
    return (MIDI_A4 +
          name2delta[data[0]] + # Name
          sum(accident2delta[ac] for ac in accidents) + # Accident
          12 * octave_delta # Octave
         )

def str2freq(note_string):
    """
    Given a note string name (e.g. "F#2"), returns its frequency in Hz.
    """
    return midi2freq(str2midi(note_string))


def freq2midi(freq):
    """
    Given a frequency in Hz, returns its MIDI pitch number.
    """
    result = 12 * (log2(freq) - log2(FREQ_A4)) + MIDI_A4
    return nan if isinstance(result, complex) else result

def midi2str(midi_number, sharp=True):
    """
    Given a MIDI pitch number, returns its note string name (e.g. "C3").
    """
    if isinf(midi_number) or isnan(midi_number):
        return "?"
    num = midi_number - (MIDI_A4 - 4 * 12 - 9)
        
    note = (num + .5) % 12 - .5
    rnote = int(round(note))
    error = note - rnote
    octave = str(int(round((num - note) / 12.)))
    if sharp:
        names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    else:
        names = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
    name = names[rnote] + octave
    if abs(error) < 1e-4:
        return name
    else:
        err_sig = "+" if error > 0 else "-"
        err_str = err_sig + str(round(100 * abs(error), 2)) + "%"
    return name + err_str


def freq2str(freq):
    """
    Given a frequency in Hz, returns its note string name (e.g. "D7").
    """
    return midi2str(freq2midi(freq))