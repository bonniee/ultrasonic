import sys
import argparse
import itertools

from wavebender import *
from constants import *

### Usage: python sound_encoder.py words ultra.wav

class Encoder:
	def __init__(self):
		self.num_channels = 1
		self.bits_per_sample = 16
		self.amplitude = 0.5

	def encode(self, somestring, filename):
		samples = None
		count = 0
		binform = ''.join(format(ord(i), 'b').zfill(8) for i in somestring)
		print binform
		for b in binform:
			freq = ZERO
			if (b is '1'):
				freq = ONE
			sample_bit = self.create_samples(BIT_DURATION, freq)
			count += 1
			if (samples is None):
				samples = sample_bit
			else:
				samples = itertools.chain(samples, sample_bit)
		self.save_wav(filename, samples, count * BIT_DURATION)

	def create_samples(self, duration, frequency):
		num_samples = int(RATE * duration * 0.5)
		channels = ((sine_wave(frequency, RATE, self.amplitude),) for i in range(self.num_channels))
		samples = compute_samples(channels, num_samples)
		channels = ((sine_wave(frequency, RATE, 0.0),) for i in range(self.num_channels))
		silence = compute_samples(channels, num_samples)
		return itertools.chain(samples, silence)
		
	def save_wav(self, filename, samples, total_duration):
		write_wavefile(filename, samples, RATE * total_duration, self.num_channels, self.bits_per_sample / 8, RATE)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="sound_encoder")
	parser.add_argument('text', help="The text to encode")
	parser.add_argument('filename', help="The file to generate.")
	args = parser.parse_args()
	enc = Encoder()
	enc.encode(args.text, args.filename)