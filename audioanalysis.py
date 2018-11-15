import wave
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math

types = {
    1: np.int8,
    2: np.int16,
    4: np.int32
}

featuresound = {
	"nchannels" : None,
	"sampwidth" : None,
	"framerate" : None,
	"nframes" : 0,
	"comptype" : None,
	"compname" : None,
	"samples" : None
}

CONST_SENS = 1 # parameter feel

POS_ISEMIPARABOLS = [ ]
NEG_ISEMIPARABOLS = [ ]
POS_EXSEMIPARABOLS = [ ]
NEG_EXSEMIPARABOLS = [ ]

def openSound(path, mode):
	try:
		wav = wave.open(path, mode=mode)
	except FileNotFoundError as e:
		print(e)
		sys.exit()

	nchannels, sampwidth, framerate, nframes, comptype, compname = wav.getparams()
	content = wav.readframes(nframes)
	samples = np.fromstring(content, dtype=types[sampwidth])

	featuresound["nchannels"] = nchannels
	featuresound["sampwidth"] = sampwidth
	featuresound["framerate"] = framerate
	featuresound["nframes"] = nframes
	featuresound["comptype"] = comptype
	featuresound["compname"] = compname

	return samples, nchannels, featuresound

def showGraphic(width, height, featuresound, samples):
	duration = featuresound["nframes"] / featuresound["framerate"]
	DPI = 72
	peak = 256 ** featuresound["sampwidth"] * 0.5
	k = math.ceil(featuresound["nframes"] / width / 32)

	plt.figure(1, figsize=(float(width)/DPI, float(height)/DPI), dpi=DPI)
	plt.subplots_adjust(wspace=0, hspace=0)

	for n in range(featuresound["nchannels"]):
		channel = samples[n::featuresound["nchannels"]]

		channel = channel[0::k]
		if featuresound["nchannels"] == 1:
			channel = channel - peak

		axes = plt.subplot(2, 1, n+1)
		axes.plot(channel, 'g')
		#plt.fill([0, float(width)/DPI], [0, int(float(height)/DPI)], 'b')
		plt.grid(True, color='blue')

	plt.show()

def calcRanges(parabols):
	RANGES = [ ]

	froma = list(parabols)
	toa = list(parabols)
	for i in range(len(parabols)):
		froma[i] = int(round(parabols[i]-((parabols[i]/100)*CONST_SENS*100)))
		toa[i] = int(round(parabols[i]+((parabols[i]/100)*CONST_SENS*100)))
		RANGES.append(range(froma[i], toa[i]+1))

	return RANGES

def analyseChannel(exsample, exchan, isample, ichan):
	sumparabol = 0
	tmp = 0

	print("Analysis started. Please wait, it may take a long time...")
	for n in range(exchan):
		for i in range(len(exsample[n::exchan])):
			if tmp < exsample[n::exchan][i]:
				tmp = exsample[n::exchan][i]
				sumparabol += tmp
			else:
				POS_EXSEMIPARABOLS.append(sumparabol)
				sumparabol = 0

			if tmp > exsample[n::exchan][i]:
				tmp = exsample[n::exchan][i]
				sumparabol += tmp
			else:
				NEG_EXSEMIPARABOLS.append(sumparabol)
				sumparabol = 0
			
	for m in range(ichan):
		for i in range(len(isample[m::ichan])):
			if tmp < isample[m::ichan][i]:
				tmp = isample[m::ichan][i]
				sumparabol += tmp
			else:
				POS_ISEMIPARABOLS.append(sumparabol)
				sumparabol = 0

			if tmp > isample[m::ichan][i]:
				tmp = isample[m::ichan][i]
				sumparabol += tmp
			else:
				NEG_ISEMIPARABOLS.append(sumparabol)
				sumparabol = 0


	#POS_EXSEMIPARABOLS
	#NEG_EXSEMIPARABOLS
	#POS_ISEMIPARABOLS
	#NEG_ISEMIPARABOLS
	# EXPARABOLS = [ ]
	# for i in POS_EXSEMIPARABOLS:
	# 	EXPARABOLS.append(i)

	# for i in NEG_EXSEMIPARABOLS:
	# 	EXPARABOLS[i] += i

	# print(EXPARABOLS)

	posexp = calcRanges(POS_EXSEMIPARABOLS)
	negexp = calcRanges(NEG_EXSEMIPARABOLS)
	#posip = calcRanges(POS_ISEMIPARABOLS)
	#negip = calcRanges(NEG_ISEMIPARABOLS)

	pos_opt = 0
	neg_opt = 0

	#print(len(set(POS_EXSEMIPARABOLS)))
	#print(len(POS_ISEMIPARABOLS))
	# count = 0
	# for i in POS_ISEMIPARABOLS:
	# 	for j in posexp:
	# 		if POS_ISEMIPARABOLS[i] in posexp[j]:
	# 			pos_opt += 1
	# 			count += 1
	# 			#if len(set(POS_EXSEMIPARABOLS)) == len(POS_ISEMIPARABOLS):
	# 		else:
	#  			neg_opt += 1
	#  			count = 0

	count = 0
	for i in range(len(POS_ISEMIPARABOLS)):
		if i < len(posexp):
			if POS_ISEMIPARABOLS[i] in posexp[i]:
				pos_opt += 1
				count += 1
				if count < 1:
					pos_opt *= count
			else:
	 			neg_opt += 1
	 			count = 0

	for i in range(len(NEG_ISEMIPARABOLS)):
		if i < len(negexp):
			if NEG_ISEMIPARABOLS[i] in negexp[i]:
				pos_opt += 1
				count += 1
				if count < 1:
					pos_opt *= count
			else:
	 			neg_opt += 1
	 			count = 0

	return pos_opt, neg_opt

if __name__ == "__main__":
	try:
		if not 1 < len(sys.argv):
			raise Exception("Error! First parameter is not specified!\nHelp:\n audioanalysis {exam.wav} {input.wav}\n or\n audioanalysis {exams.txt} {input.wav} - where in TXT is a list of example names.")
		elif not 2 < len(sys.argv):
			raise Exception("Error! Second parameter is not specified!\nHelp:\n audioanalysis {exam.wav} {input.wav}\n or\n audioanalysis {exams.txt} {input.wav} - where in TXT is a list of example names.")
	except Exception as error:
		print(error)
		sys.exit()

	exsamples, exchan, exfeature = openSound(sys.argv[1], 'r') #exams
	isamples, ichan, ifeature = openSound(sys.argv[2], 'r') # input

	#showGraphic(1000, 500, exfeature, exsamples)
	#showGraphic(1000, 500, ifeature, isamples)

	pos_opt, neg_opt = analyseChannel(exsamples, exchan, isamples, ichan)

	try:
		print("Match percentage = {0}%".format((pos_opt/(pos_opt+neg_opt))*100))
	except ZeroDivisionError as error:
		print(error)
		#sys.exit()
 