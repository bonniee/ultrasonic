from __future__ import division # float division of integers

import pyaudio
import wave
import struct
import math
import numpy
import sys

from constants import *

# Mathy things
TWOPI = 2 * math.pi
WINDOW = numpy.hamming(CHUNK_SIZE)

class Decoder:
  def __init__(self, debug):
    # -1 for no signal, 0 and 1
    self.state = -1
    self.new_state = -1
    self.new_count = 1
    self.audio = None
    self.byte = []
    self.idle_count = 0
    self.debug = debug

  def listen(self):
    print 'Listening... (For debug output, use <python sound_decoder.py debug>)'
    p = pyaudio.PyAudio()
    stream = p.open(format = pyaudio.paInt16,
                    channels = 1,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = CHUNK_SIZE)

    # Listen to READ_SIZE samples at a time.
    while (True):
      audiostr = stream.read(CHUNK_SIZE)
      self.audio = list(struct.unpack("%dh" % CHUNK_SIZE, audiostr))
      self.window()
      power0 = self.goertzel(ZERO)
      power1 = self.goertzel(ONE)
      self.update_state(power0, power1)
      self.process_byte()

  # For now, just print out the characters as we go.
  def process_byte(self):

    if len(self.byte) != 8:
      self.idle_count += 1
      if self.idle_count > IDLE_LIMIT:
        if len(self.byte) > 0:
          self.byte = []
          print
        self.idle_count = 0
      return;
    
    ascii = 0
    for bit in self.byte:
      ascii = (ascii << 1) | bit
    char = chr(ascii)
    sys.stdout.write(char)
    sys.stdout.flush()
    self.byte = []

  # We want to see SMOOTH_COUNT previous samples match before switching. Evens out noise.
  def update_state(self, power0, power1):
    cur_state = -1
    if power1 / power0 > THRESHOLD:
      cur_state = 1
    elif power0 / power1 > THRESHOLD:
      cur_state = 0

    if self.debug:
      if cur_state == -1:
        sys.stdout.write('-')
      else:
        sys.stdout.write(str(cur_state))
      sys.stdout.flush()

    # If the current state matches the last few states:
    if self.new_state == cur_state:
      if self.new_count <= SMOOTH_COUNT:
        self.new_count += 1 # new_count can only ever go up to SMOOTH_COUNT + 1.

      # If we have enough of the same new state to reasonably believe it, change state
      if self.new_count == SMOOTH_COUNT:
        self.state = cur_state
        self.idle_count = 0

        # If the new state is a 0 or 1, use it!
        if self.state != -1:
          self.byte.append(self.state)
          if self.debug:
            sys.stdout.write('|' + str(self.state) + '|')
            sys.stdout.flush()

    # The current state is different from the last few states, so reset.
    else:
      self.new_state = cur_state
      self.new_count = 1

  def goertzel(self, frequency):
    prev1 = 0.0
    prev2 = 0.0
    norm_freq = frequency / RATE
    coeff = 2 * math.cos(TWOPI * norm_freq)
    for sample in self.audio:
      s = sample + (coeff * prev1) - prev2
      prev2 = prev1
      prev1 = s
    power = (prev2 * prev2) + (prev1 * prev1) - (coeff * prev1 * prev2)
    return int(power) + 1 # prevents division by zero problems

  def window(self):
    for i in range(CHUNK_SIZE):
      self.audio[i] = self.audio[i] * WINDOW[i]

def main():
  if len(sys.argv) == 2 and sys.argv[1] == 'debug':
    dec = Decoder(1)
  else:
    dec = Decoder(0)
  dec.listen()

if __name__ == "__main__":
    main()
