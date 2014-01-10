import sys
import argparse
import numpy as np
from scipy.io import wavfile
from constants import *

class SoundFile:
   def  __init__(self, signal):
	   self.file = wave.open('test.wav', 'wb')
	   self.signal = signal
	   self.sr = 44100

   def write(self):
	   self.file.setparams((1, 2, self.sr, 44100*4, 'NONE', 'noncompressed'))
	   self.file.writeframes(self.signal)
	   self.file.close()

class Encoder:
	def __init__(self):
		self.num_channels = 1
		self.bits_per_sample = 16
		self.amplitude = 0.5

	def encode(self, somestring, filename):
		samples = None
		count = 0
		binform = ''.join('2' + format(ord(i), 'b').zfill(8) for i in somestring)
		soundlist = []
		# print binform
		for b in binform:
			freq = ZERO
			if (b is '1'):
				freq = ONE
			elif (b is '2'):
				freq = CHARSTART
			soundlist = np.hstack((soundlist, self.getbit(freq)))

		wavfile.write(filename,RATE,soundlist.astype(np.dtype('int16')))

	def getbit(self, freq):

		music=[]
		# t=np.arange(0,BIT_DURATION/2.0,1./RATE) #time
		t=np.arange(0,BIT_DURATION,1./RATE) #time

		x = np.sin(2*np.pi*freq*t) #generated signals
		x = [int(val * 32000) for val in x]

		sigmoid = [1 / (1 + np.power(np.e, -t)) for t in np.arange(-6, 6, 0.01)]
		sigmoid_inv = sigmoid[::-1]

		xstart = len(x) - len(sigmoid)
		for i in range(len(sigmoid)):
			x[xstart + i] = x[xstart + i] * sigmoid_inv[i]
			x[i] = x[i] * sigmoid[i]

		music=np.hstack((music,x))
		return music

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="sound_encoder")
	parser.add_argument('text', help="The text to encode")
	parser.add_argument('filename', help="The file to generate.")
	args = parser.parse_args()

	enc = Encoder()
	enc.encode(args.text, args.filename)
