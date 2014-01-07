from __future__ import division # float division of integers
from collections import deque

import pyaudio
import wave
import struct
import math
import numpy
import sys
from scipy import signal

from constants import *

# Mathy things
TWOPI = 2 * math.pi
WINDOW = numpy.hamming(CHUNK_SIZE)

class Decoder:
  def __init__(self, debug):
    self.audio = None

    half_win = int(BIT_DURATION * RATE / CHUNK_SIZE / 2)
    self.win_len = 2 * half_win
    self.win_fudge = int(self.win_len / 2)
    self.buffer = deque()
    self.buf_len = self.win_len + self.win_fudge
    self.sig_0 = [0] * half_win + [-1] * half_win
    self.sig_1 = [1] * half_win + [-1] * half_win
    self.sig_N = [-1] * self.win_len
    self.prev_state = -1
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
      self.signal_to_bits()
      self.process_byte()

  def printbuf(self, buf):
    newbuf = ['-' if x is -1 else x for x in buf]
    print repr(newbuf).replace(', ', '').replace('\'', '')

  # Takes the raw noisy samples of -1/0/1 and finds the bitstream from it
  def signal_to_bits(self):
    if len(self.buffer) < self.buf_len:
      return
    buf = list(self.buffer)
    
    if self.debug:
      self.printbuf(buf)
    
    costs = [[] for i in range(3)]
    for i in range(self.win_fudge):
      win = buf[i : self.win_len + i]
      costs[0].append(sum(x != y for x, y in zip(win, self.sig_0)))
      costs[1].append(sum(x != y for x, y in zip(win, self.sig_1)))
      costs[2].append(sum(x != y for x, y in zip(win, self.sig_N)))
    min_costs = [min(costs[i]) for i in range(3)]
    min_cost = min(min_costs)
    signal = min_costs.index(min_cost)
    fudge = costs[signal].index(min_cost)
    for i in range(self.win_len + fudge):
      self.buffer.popleft()

    if signal < 2:
      self.byte.append(signal)
    else:
      self.idle_count += 1

    if self.debug:
      if signal == 2:
        signal = '-'
      sys.stdout.write('')
      sys.stdout.write('|{}|\n'.format(signal))
      sys.stdout.flush()

  # For now, just print out the characters as we go.
  def process_byte(self):

    if len(self.byte) != 8:
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

  # Determine the raw input signal of silences, 0s, and 1s. Insert into sliding window.
  def update_state(self, power0, power1):
    state = -1

    if self.prev_state is -1:
      thresh = THRESH_HIGH
    else:
      thresh = THRESH_LOW

    if power1 / power0 > THRESHOLD:
      state = 1
    elif power0 / power1 > THRESHOLD:
      state = 0
    # print int(power1 / power0), int(power0 / power1)

    # if self.debug:
    #   if state == -1:
    #     sys.stdout.write('-')
    #   else:
    #     sys.stdout.write(str(state))
    #   sys.stdout.flush()
    self.prev_state = state

    if len(self.buffer) >= self.buf_len:
      self.buffer.popleft()
    self.buffer.append(state)

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
    self.audio = [aud * win for aud, win in zip(self.audio, WINDOW)]


def main():
  if len(sys.argv) == 2 and sys.argv[1] == 'debug':
    dec = Decoder(1)
  else:
    dec = Decoder(0)
  dec.listen()

if __name__ == "__main__":
    main()
