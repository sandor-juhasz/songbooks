import re
import glob

def parse_abc(filename):
    songs=[]
    song={"note_lines":[]}
    with open(filename, 'r') as f:
        for line in f:
            fragments=re.split(":", line.strip())
            if len(fragments)==1 and not line.startswith("%"):
                song["note_lines"].append(fragments[0])
    songs.append(song)
    return songs

def parse_note_line(note_line):
    note_line=re.sub(r"[ ()>|zZ]", "", note_line) # Removes whitespaces and other markings.
    note_line=re.sub(r"\|", "", note_line)  # Removes the beat markers.
    note_line=re.sub(r'"[a-zA-Z0-9]*"', "", note_line)          # Removes chords

    line=[]
    pattern="([\^_]?[a-zA-Z][',]?)([0-9]?/*[0-9]?)"
    for (note, length) in re.findall(pattern, note_line):
        line.append({"note": abc_note_to_midi(note), "length": length})
    return line

def abc_note_to_midi(note):
    midi_note=60    # C4, aka middle C.
    octave = ['C', '_', 'D','_', 'E', 'F', '_', 'G','_', 'A','_', 'B']
    
    if note.startswith("^"):
        midi_note=midi_note+1
        note=note[1:]
    elif note.startswith("_"):
        midi_note=midi_note-1
        note=note[1:]

    if note[0].islower():
        note=note[0].upper()+"'"+note[1:]

    raise_octave=note.count("'")
    lower_octave=note.count(",")
    midi_note=midi_note+octave.index(note[0])+(raise_octave-lower_octave)*12

    return midi_note

def midi_to_abc_note(midi_note):
    octave = ['C', '^C', 'D','^D', 'E', 'F', '^F', 'G','^G', 'A','^A', 'B']
    octaves=(midi_note-60) // 12
    if octaves < 0:
        octave_suffix=',' * (-octaves)
    elif octaves > 0:
        octave_suffix="'" * octaves
    else:
        octave_suffix=""
        
    abc_note=octave[(midi_note-60) % 12] + octave_suffix
    return abc_note

def midi_to_relative_solfa(midi_note):
    octave = ['do', 'di', 're','ri', 'mi', 'fa', 'fi', 'so','si', 'la','li', 'ti']
        
    relative_solfa=octave[(midi_note-60) % 12]
    return relative_solfa

def get_notes(song):
    notes=set()
    for note_line in song["note_lines"]:
        line = parse_note_line(note_line)
        for note in line:
            notes.add(note["note"])

    n = list(notes)
    n.sort()
    return [midi_to_abc_note(x) for x in n]
    
def main():
    for filename in glob.glob("/vagrant/books/magyar-gyerekdalok/*.abc"):
        songs= parse_abc(filename)
        for song in songs:
            notes=get_notes(song)
            print(filename + " " + " ".join(notes))

if __name__ == "__main__":
    main()
