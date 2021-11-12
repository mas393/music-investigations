#!/usr/bin/env python

# Author: Matthew Stephenson
# Email: matthewstephenson39@gmail.com
# 2021-10-16 Personal Hackathon Project
# Messing around with sin waves to produce some sounds

from scipy.io.wavfile import write
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
from playsound import playsound



def get_sinusoid(freq: float, time: np.linspace) -> np.linspace:
    return np.sin(2*np.pi*freq*time)
    
def add_partials(freq: float, time: np.linspace, sound: np.linspace , num_partials: int) -> np.linspace:
    #partialstep = lambda x: 2**x
    diminish = lambda x: 2**x
    for i in range(1, num_partials):
        sound += get_sinusoid(freq*i, time)/diminish(i)
    sound = sound/sound.max()
    return sound

def sound_decay(freq: float, time: np.linspace, sound: np.linspace) -> np.linspace:
    a,envelope = signal.gausspulse(time, fc = freq, bw = 0.005, retenv = True)
    envelope = np.sin(np.pi*time)
    return sound*envelope

def nth_degree_major_chord(freq: float, time: np.linspace, chordterms: int = 3, chordstep: float = 1/4, partials: bool = True, num_partials: int = 5) -> np.linspace:
    sound = get_sinusoid(freq, time)
    if partials:
        sound =  add_partials(freq, time, sound, num_partials)
        
    for i in range(1, chordterms):
        nextsound = get_sinusoid(freq*(1+chordstep*i), time)
        if partials:
            nextsound = add_partials(freq*(1+chordstep*i), time, nextsound, num_partials)

        sound += nextsound

    return sound/chordterms

def major_chord(freq: float, time: np.linspace, chordstep: float = 1/4, partials: bool = True, num_partials: int = 5) -> np.linspace:
    return nth_degree_major_chord(freq = freq, time = time, chordterms=3, chordstep=chordstep, partials=partials, num_partials=num_partials)

def minor_chord(freq: float, time: np.linspace, chordstep: float = 1/4, partials: bool = True, num_partials: int = 5) -> np.linspace:
    sound_root = get_sinusoid(freq, time)
    sound_second = get_sinusoid(freq*(1+chordstep), time)
    sound_third = get_sinusoid(freq*(1+chordstep*3/2), time)
    
    if partials:
        sound_root = add_partials(freq, time, sound_root, num_partials)
        sound_second = add_partials(freq*(1+chordstep), time, sound_second, num_partials)
        sound_third = add_partials(freq*(1+chordstep*3/2), time, sound_third, num_partials)

    return (sound_root + sound_second + sound_third)/3

def main():
    SAMPLERATE=44100
    BASEFREQUENCY=220
    STEPS = 6

    #t = np.linspace(0., 2*STEPS/BASEFREQUENCY, SAMPLERATE) #for plotting
    t = np.linspace(0., 1, SAMPLERATE) #for audio

    FILES = []
    for i in range(1,STEPS):
        
        
        #produce a major chord along with the root of the beats created by the major chord
        '''
        data = major_chord(BASEFREQUENCY, t, chordstep=i/STEPS)
        data = sound_decay(BASEFREQUENCY, t, data)
        filename = "{}_{}major.wav".format(i, STEPS)
        write(filename, SAMPLERATE, data)
        
        data = get_sinusoid(BASEFREQUENCY*i/STEPS, t)
        data = add_partials(BASEFREQUENCY*i/STEPS, t, data, 3)
        data = sound_decay(BASEFREQUENCY, t, data)
        filename = "{}_{}major_beats.wav".format(i, STEPS)
        write(filename, SAMPLERATE, data)
        '''
        
        # produce a tone with i amount of partials
        # nth partial is sin(2**n*f) with amplitude 1/2**n/2**n (1/2**n is only linear)

        data = get_sinusoid(BASEFREQUENCY, t)
        data = add_partials(BASEFREQUENCY, t, data, i)
        data = sound_decay(BASEFREQUENCY, t, data)
        filename = "{}_harmonics.wav".format(i)
        FILES.append(filename)
        write(filename, SAMPLERATE, data)

        
        # produces major and minor chords for a base over an octave
            
        '''
        #data = major_chord(BASEFREQUENCY, t, chordstep=i/STEPS, partials = True)
        data = nth_degree_major_chord(freq = BASEFREQUENCY, time = t, chordterms=3, chordstep=i/STEPS)
        data = sound_decay(BASEFREQUENCY, t, data)
        filename = "{}_{}major.wav".format(i,STEPS)
        write(filename, SAMPLERATE, data)
        
        data = minor_chord(BASEFREQUENCY, t, chordstep=i/STEPS, partials = True)
        data = sound_decay(BASEFREQUENCY, t, data)
        filename = "{}_{}minor.wav".format(i,STEPS)
        write(filename, SAMPLERATE, data)
        '''
        
        # produces the major and minor for a step up from from the base (e.g 1/5,1/4/1/3)
        '''
        data = major_chord(BASEFREQUENCY, t, chordstep=1/i, partials = True)
        data = sound_decay(BASEFREQUENCY, t, data)
        filename = "{}_{}major.wav".format(1,i)
        write(filename, SAMPLERATE, data)
        
        data = minor_chord(BASEFREQUENCY, t, chordstep=1/i, partials = True)
        data = sound_decay(BASEFREQUENCY, t, data)
        filename = "{}_{}minor.wav".format(1,i)
        write(filename, SAMPLERATE, data)
        '''
        
        # produces a good sounding major chord (1/3 steps) for all octaves on piano (e.g. A1, A2, ...)
        # TODO: fix the decay rates for different BASEFREQUENCY values
        '''
        BASEFREQUENCY = 32.703
        data = major_chord(BASEFREQUENCY*2**(i-1), t, chordstep=1/3, partials = True)
        data = sound_decay(BASEFREQUENCY*2**(i-1), t, data)
        filename = "{}_major.wav".format(BASEFREQUENCY*2**(i-1))
        write(filename, SAMPLERATE, data)
        '''
        
        # number of components of sign wave for a given major chord
        # i.e
        # step 1 = sin() + sin()
        # step 2 = sin() + sin() + sin()
        '''
        data = nth_degree_major_chord(BASEFREQUENCY, t, chordterms = i, chordstep = 1/3)
        data = sound_decay(BASEFREQUENCY, t, data)
        filename = "{}_terms_major".format(i) 
        write(filename, SAMPLERATE, data)
        '''

        '''
        # does not work as intended
        # changing the sampleing rate to produce different sound waves through alliasing of a single freq
        # producing the step amount of harmonics of the base freq
        # i.e fsample - fin = fout
        FREQ = 3520
        SAMP = FREQ/2**i + FREQ
        print(SAMP)
        data = get_sinusoid(FREQ, t)
        filename = "{}_hz_using_samp_rate_{}".format(FREQ/2**i, int(SAMP))
        write(filename, int(SAMP), data)
        '''

        

        
        
    #for f in FILES:
    #playsound(FILES[3])
    #plt.show()

if __name__ == "__main__":
    main()


