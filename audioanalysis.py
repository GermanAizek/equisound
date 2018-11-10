import wave
import numpy as np
import os
import sys

types = {
    1: np.int8,
    2: np.int16,
    4: np.int32
}

EXAMS = [ ]
#EXAM_CHANNELS = [ ]
#INPUT_CHANNELS = [ ]

CONST_SENS = 5 # percent

POS_OPT = 0
NEG_OPT = 0

def openSound(path, mode):
	if path.split('.')[1] == "txt":
		print("You have uploaded some example, wait for them to load.")

		with open(path, 'r') as file:
			for exam in file:
				wav = wave.open(exam, mode=mode)
				nchannels, sampwidth, framerate, nframes, comptype, compname = wav.getparams()
				content = wav.readframes(nframes)
				samples = np.fromstring(content, dtype=types[sampwidth])
				EX_SAMPLES.append(samples)
				EX_CHANNELS.append(nchannels)

		print("Exams succeful loaded: {0}".format(EXAMS))		
	else:
		#print("You have uploaded one example, comparison will not be accurate.")

		wav = wave.open(path, mode=mode)
		nchannels, sampwidth, framerate, nframes, comptype, compname = wav.getparams()
		content = wav.readframes(nframes)
		samples = np.fromstring(content, dtype=types[sampwidth])

		return samples, nchannels

# input
#iwav = wave.open(sys.argv[2], mode=mode)
#inchannels, isampwidth, iframerate, inframes, icomptype, icompname = iwav.getparams()
#icontent = wav.readframes(inframes)
#isamples = np.fromstring(icontent, dtype=types[isampwidth])

# calc
def analyseChannel(exsample, exchan, isample, ichan):
	print("Analysis started. Please wait, it may take a long time...")
	for n in range(exchan):
		for m in range(ichan):
			for value in exsample[n::exchan]:
				for ivalue in isample[m::ichan]:
					for val_range in range(int(value-((value/100)*CONST_SENS)), int(value+((value/100)*CONST_SENS))):
						global POS_OPT, NEG_OPT
						if ivalue == val_range:
							POS_OPT += 1
						else:
							NEG_OPT += 1
						
						print(POS_OPT)
						print(NEG_OPT)
			print("sample")

if __name__ == "__main__":
	try:
		if not 1 < len(sys.argv):
			raise Exception("Error! First parameter is not specified!\nHelp:\n audioanalysis {exam.wav} {input.wav}\n or\n audioanalysis {exams.txt} {input.wav} - where in TXT is a list of example names.")
		elif not 2 < len(sys.argv):
			raise Exception("Error! Second parameter is not specified!\nHelp:\n audioanalysis {exam.wav} {input.wav}\n or\n audioanalysis {exams.txt} {input.wav} - where in TXT is a list of example names.")
		#else:
		#	raise Exception("Parameters a lot!\nHelp:\n audioanalysis {exam.wav} {input.wav}\n or\n audioanalysis {exams.txt} {input.wav} - where in TXT is a list of example names.")
	except Exception as error:
		print(error)
		sys.exit()

	exsample, exchan = openSound(sys.argv[1], 'r') #exams
	isample, ichan = openSound(sys.argv[2], 'r') # input
	
	analyseChannel(exsample, exchan, isample, ichan)

	print("Match percentage = {0}".format((POS_OPT/POS_OPT+NEG_OPT)*100))