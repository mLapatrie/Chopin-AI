
import os
import py_midicsv as pm
from math import ceil

midi_files = os.listdir("sorting/midi input")
csv_files = os.listdir("sorting/compressed input")

tones = {
    # char : tone
    "!": 21,  # A0
    "#": 22,  # A#0
    "$": 23,  # B0
    "%": 24,  # C1
    "&": 25,  # C#1
    "(": 26,  # D1
    ")": 27,  # D#1
    "*": 28,  # E1
    "+": 29,  # F1
    "-": 30,  # F#1
    ".": 31,  # G1
    "0": 32,  # G#1
    "1": 33,  # A1
    "2": 34,  # A#1
    "3": 35,  # B1
    "4": 36,  # C2
    "5": 37,  # C#2
    "6": 38,  # D2
    "7": 39,  # D#2
    "8": 40,  # E2
    "9": 41,  # F2
    ":": 42,  # F#2
    ";": 43,  # G2
    "<": 44,  # G#2
    "=": 45,  # A2
    ">": 46,  # A#2
    "?": 47,  # B2
    "@": 48,  # C3
    "A": 49,  # C#3
    "B": 50,  # D3
    "C": 51,  # D#3
    "D": 52,  # E3
    "E": 53,  # F3
    "F": 54,  # F#3
    "G": 55,  # G3
    "H": 56,  # G#3
    "I": 57,  # A3
    "J": 58,  # A#3
    "K": 59,  # B3
    "L": 60,  # C4
    "M": 61,  # C#4
    "N": 62,  # D4
    "O": 63,  # D#4
    "P": 64,  # E4
    "Q": 65,  # F4
    "R": 66,  # F#4
    "S": 67,  # G4
    "T": 68,  # G#4
    "U": 69,  # A4
    "V": 70,  # A#4
    "W": 71,  # B4
    "X": 72,  # C5
    "Y": 73,  # C#5
    "Z": 74,  # D5
    "[": 75,  # D#5
    "]": 76,  # E5
    "^": 77,  # F5
    "_": 78,  # F#5
    "a": 79,  # G5
    "b": 80,  # G#5
    "c": 81,  # A5
    "d": 82,  # A#5
    "e": 83,  # B5
    "f": 84,  # C6
    "g": 85,  # C#6
    "h": 86,  # D6
    "i": 87,  # D#6
    "j": 88,  # E6
    "k": 89,  # F6
    "l": 90,  # F#6
    "m": 91,  # G6
    "n": 92,  # G#6
    "o": 93,  # A6
    "p": 94,  # A#6
    "q": 95,  # B6
    "r": 96,  # C7
    "s": 97,  # C#7
    "t": 98,  # D7
    "u": 99,  # D#7
    "v": 100,  # E7
    "w": 101,  # F7
    "x": 102,  # F#7
    "y": 103,  # G7
    "z": 104,  # G#7
    "{": 105,  # A7
    "|": 106,  # A#7
    "}": 107,  # B7
    "~": 108  # C8
}
tones_keys = list(tones)
tones_values = list(tones.values())


def compress_midi(_midi_files):
    open("sorting/input_text.txt", "w").write("")
    for file in _midi_files:
        csv_string = pm.midi_to_csv(f"sorting/midi input/{file}")
        compressed_csv = []

        for i in range(len(csv_string)):
            compressed_string = csv_string[i].split(", ")
            if len(compressed_string) == 6 and "Note_off_c" not in compressed_string[2] \
                and "Control_c" not in compressed_string[2] and "Header" not in compressed_string[2] \
                    and not compressed_string[-1] == "0\n":
                compressed_csv.append([int(compressed_string[1]), tones_keys[int(compressed_string[4]) - 21], int(compressed_string[4])])

        compressed_to_string(sorted(compressed_csv), file)


def compressed_to_string(_compressed_csv, _file):
    compressed_string = ""
    for i in range(len(_compressed_csv)):
        current_string = _compressed_csv[i][1]
        try:
            difference = _compressed_csv[i+1][0] - _compressed_csv[i][0]
            for space in range(ceil(difference/100)):
                current_string += " "
            compressed_string += current_string
        except IndexError:
            compressed_string += current_string

    open(f"sorting/compressed output/csv_{_file.replace('.mid', '')}.txt", "w").write(compressed_string)
    open(f"sorting/input_text.txt", "a").write(compressed_string + "\n")


def csv_to_mid(_csv_files):
    for file in _csv_files:

        text_to_csv(file)

        with open(f"sorting/midi output/midi_{file.replace('.txt', '').replace('csv_', '')}.mid", "wb") as output_file:
            pm.FileWriter(output_file).write(pm.csv_to_midi(f"sorting/translating/{file}"))


# Takes text and fill the gaps to csv
def text_to_csv(_file):
    cleaned_sorted = list(open(f"sorting/compressed input/{_file}", "r").readlines()[0].replace('\n', ''))
    clean_csv = []

    timing = 0
    for char in cleaned_sorted:
        if char == ' ':
            timing += 400
        else:
            clean_csv.append([timing, tones[char]])

    formatted_csv = []
    for comb in clean_csv:
        formatted_csv.append(['1', str(comb[0]), "Note_on_c", "0", str(comb[1]), "100"])

    formatting_front = [['1', '0', 'MIDI_port', '0'], ['1', '0', 'Key_signature', '2', '"major"'],
                        ['1', '0', 'Tempo', '600000'], ['1', '0', 'Time_signature', '4', '2', '24', '8'],
                        ['1', '0', 'Start_track'], ['0', '0', 'Header', '1', '2', '480']]
    for form in formatting_front:
        formatted_csv.insert(0, form)

    last_timing = int(formatted_csv[-1][1]) + 500

    formatting_end = [['1', f"{last_timing}", 'End_track'], ['0', '0', 'End_of_file']]
    for form in formatting_end:
        formatted_csv.append(form)

    for i in range(len(formatted_csv)):
        formatted_csv[i] = ", ".join(formatted_csv[i])

    open(f"sorting/translating/{_file}", "w").write("\n".join(formatted_csv))


if __name__ == "__main__":
    fr = input("from (midi)/from (text): ")
    if fr == "midi":
        compress_midi(midi_files)
    else:
        csv_to_mid(csv_files)
    print("done")
