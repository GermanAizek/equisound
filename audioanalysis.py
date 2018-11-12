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

CONST_SENS = 5 # percent

POS_OPT = 0
NEG_OPT = 0

POS_PARABOLS = [ ]
NEG_PARABOLS = [ ]

def openSound(path, mode):
	wav = wave.open(path, mode=mode)
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
		plt.grid(True, color='blue')

	#axes.xaxis.set_major_formatter(ticker.FuncFormatter(format_time))
	plt.savefig("Sound view", dpi=DPI)
	plt.show()

# def showGraphicTable(width, height, featuresound, samples):
# 	for i in range(0, len(featuresound)):
# 		duration = featuresound[i]["nframes"] / featuresound[i]["framerate"]
# 		DPI = 72
# 		peak = 256 ** featuresound[i]["sampwidth"] * 0.5
# 		k = math.ceil(featuresound[i]["nframes"] / width / 32)

# 		plt.figure(1, figsize=(float(width)/DPI, float(height)/DPI), dpi=DPI)
# 		plt.subplots_adjust(wspace=0, hspace=0)

# 		for n in range(featuresound[i]["nchannels"]):
# 			channel = samples[i][n::featuresound[i]["nchannels"]]

# 			channel = channel[0::k]
# 			if featuresound[i]["nchannels"] == 1:
# 				channel = channel - peak

# 			axes = plt.subplot(2, 1, n+1)
# 			axes.plot(channel, 'g')
# 			plt.grid(True, color='blue')

# 		#axes.xaxis.set_major_formatter(ticker.FuncFormatter(format_time))
# 		plt.savefig("Sound view", dpi=DPI)
# 		plt.show()

# calc
def analyseChannel(exsample, exchan, isample, ichan):
	sumparabol = 0

	print("Analysis started. Please wait, it may take a long time...")
	for n in range(exchan):
		for value in exsample[n::exchan]:
			if value+1 < len(exsample[n::exchan]):
				if exsample[n::exchan][value+1] >= exsample[n::exchan][value]:
					sumparabol += value
				else:
					sumparabol += value
					if value+2 < len(exsample[n::exchan]):
						if exsample[n::exchan][value+2] >= exsample[n::exchan][value+1]:
							POS_PARABOLS.append(sumparabol)
							sumparabol = 0
					else:
						POS_PARABOLS.append(sumparabol)
						break
			else:
				POS_PARABOLS.append(sumparabol)
				break

	sumparabol = 0			

	for m in range(ichan):
		for ivalue in isample[m::ichan]:
			if ivalue+1 < len(isample[m::ichan]):
				if isample[m::ichan][ivalue+1] >= isample[m::ichan][ivalue]:
					sumparabol += ivalue
				else:
					sumparabol += ivalue
					if ivalue+2 < len(isample[m::ichan]):
						if isample[m::ichan][ivalue+2] >= isample[m::ichan][ivalue+1]:
							POS_PARABOLS.append(sumparabol)
							sumparabol = 0
					else:
						POS_PARABOLS.append(sumparabol)
						break
			else:
				POS_PARABOLS.append(sumparabol)
				break


	#for val_range in range(int(value-((value/100)*CONST_SENS)), int(value+((value/100)*CONST_SENS))):
	#	global POS_OPT, NEG_OPT
	#	if ivalue == val_range:
	#		POS_OPT += 1
	#	else:
	#		NEG_OPT += 1
		
	#	print(POS_OPT)
	#	print(NEG_OPT)
		print(POS_PARABOLS)


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

	exsamples, exchan, exfeature = openSound(sys.argv[1], 'r') #exams
	isamples, ichan, ifeature = openSound(sys.argv[2], 'r') # input
	
	#features, samples = [ ], [ ]
	#features.append(exfeature)
	#features.append(ifeature)
	#samples.append(exsamples)
	#samples.append(isamples)

	#showGraphicTable(1000, 500, features, samples)
	showGraphic(1000, 500, exfeature, exsamples)
	showGraphic(1000, 500, ifeature, isamples)

	#analyseChannel(exsample, exchan, isample, ichan)

	try:
		print("Match percentage = {0}".format((POS_OPT/POS_OPT+NEG_OPT)*100))
	except ZeroDivisionError as error:
		print(error)
		#sys.exit()