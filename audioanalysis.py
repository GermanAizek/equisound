import wave
import numpy as np

import os

types = {
    1: np.int8,
    2: np.int16,
    4: np.int32
}

EXAM_CHANNELS = [ ]
INPUT_CHANNELS = [ ]

CONST_SENS_MIN = 3 # percent min
CONST_SENS_MAX = 7 # percent max

POS_OPT, NEG_OPT = 0, 0

# example
wav = wave.open("crow1a.wav", mode="r")
nchannels, sampwidth, framerate, nframes, comptype, compname = wav.getparams()
content = wav.readframes(nframes)
samples = np.fromstring(content, dtype=types[sampwidth])

for n in range(nchannels):
	EXAM_CHANNELS.append(samples[n::nchannels])
	

# input
iwav = wave.open("crow2a.wav", mode="r")
inchannels, isampwidth, iframerate, inframes, icomptype, icompname = iwav.getparams()
icontent = wav.readframes(inframes)
isamples = np.fromstring(icontent, dtype=types[isampwidth])

for n in range(inchannels):
	INPUT_CHANNELS.append(samples[n::inchannels])
	
print("Please wait, it may take a long time...")
	
# calc
for channel in EXAM_CHANNELS:
	for value in channel:
		for ichannel in INPUT_CHANNELS:
			for ivalue in ichannel:
				for val_range in range(int(value/100*CONST_SENS_MIN), int(value/100*CONST_SENS_MAX)):
					if ivalue == val_range:
						POS_OPT += 1
					else:
						NEG_OPT += 1
					
	print(POS_OPT)
	print(NEG_OPT)
	
print("Match percentage = {0}".format((POS_OPT/POS_OPT+NEG_OPT)*100))