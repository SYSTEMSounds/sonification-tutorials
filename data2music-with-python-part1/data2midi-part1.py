#!/usr/bin/env python

"""
data2midi-part1.py: Maps lunar impact crater data (.csv) into musical notes (.mid).

Written by Matt Russo
www.astromattrusso.com
www.system-sounds.com
"""

import pandas as pd   # https://pypi.org/project/pandas/
import matplotlib.pylab as plt  # https://pypi.org/project/matplotlib/
from audiolazy import str2midi # https://pypi.org/project/audiolazy/
from midiutil import MIDIFile # https://midiutil.readthedocs.io/en/1.2.1/

##############################################################################
filename = 'lunarCraterAges'  #filename of csv with data

duration_beats = 52.8 #desired duration in beats (1 beat = 1 second if bpm=60)
bpm = 60 #tempo (beats per minute)

y_scale = 0.5  #scaling parameter for y-axis data (1 = linear)

#note set for mapping (or use a few octaves of a specific scale)
note_names = ['C1','C2','G2',
             'C3','E3','G3','A3','B3',
             'D4','E4','G4','A4','B4',
             'D5','E5','G5','A5','B5',
             'D6','E6','F#6','G6','A6']

vel_min,vel_max = 35,127   #minimum and maximum note velocity

##############################################################################
def map_value(value,min_value,max_value,min_result,max_result):
    '''maps value (or array of values) from one range to another'''
    result = min_result + (value - min_value)/(max_value-min_value)*(max_result - min_result)
    return result
##############################################################################

## Load data
df = pd.read_csv(filename + '.csv')  #load data as a pandas dataframe
n_impacts = len(df)

ages = df['age'].values    #this is a numpy array (not a list), you can do mathematical operations directly on the object
diameters = df['diameter'].values

## Compress Time
t_data = map_value(ages, min(ages), max(ages), duration_beats, 0) #compress time from Myrs to beats, largest age (oldest crater) mapped to beat 0

## Calculate duration in seconds
duration_sec = max(t_data)*60/bpm #duration in seconds (actually, onset of last note)
print('Duration:',duration_sec,'seconds')

## Normalize and scale y-axis data
y_data = map_value(diameters, min(diameters), max(diameters), 0, 1) #normalize data, so it runs from 0 to 1
y_data = y_data**y_scale

## Make list of MIDI numbers of chosen notes for mapping
note_midis = [str2midi(n) for n in note_names] #make a list of midi note numbers
n_notes = len(note_midis)
print('Resolution:',n_notes,'notes')

## Map y-axis data to MIDI notes and velocity
midi_data = []
vel_data = []
for i in range(n_impacts):
    note_index = round(map_value(y_data[i], 0, 1, n_notes-1, 0)) #bigger craters are mapped to lower notes
    midi_data.append(note_midis[note_index])

    note_velocity = round(map_value(y_data[i], 0, 1, vel_min, vel_max)) #bigger craters will be louder
    vel_data.append(note_velocity)

## Save MIDI file
my_midi_file = MIDIFile(1) #one track
my_midi_file.addTempo(track=0, time=0, tempo=bpm)

for i in range(n_impacts):
    my_midi_file.addNote(track=0, channel=0, pitch=midi_data[i], time=t_data[i] , duration=2, volume=vel_data[i])

with open(filename + '.mid', "wb") as f:
    my_midi_file.writeFile(f)
print('Saved',filename + '.mid')
