from sound_decoder import *
from sound_encoder import *
import sys
import argparse
import string

class SqueakyChat:

  def __init__(self):
    
    # Set up audio backend
    self.enc = Encoder()
    self.dec = Decoder(0)
    self.dec.attach_character_callback(self.printer)
    self.dec.attach_idle_callback(self.idle_callback)
    self.buf = ''

  def toggleBit(int_type, offset):
    mask = 1 << offset
    return(int_type ^ mask)

  def idle_callback(self):
    if len(self.buf) > 0:
      print
      self.buf = ''

  def printer(self, char):
    # print 'received ' + char
    self.buf += char
    sys.stdout.write('%s' % char)
    sys.stdout.flush()

  def start_chat(self):
    while True:
      try:
        s = raw_input('')
        if len(s) < 1:
          continue
        self.dec.stop_listening()
        self.enc.encodeplay(s)
        self.dec.start_listening()

      except:
        self.dec.quit()
        self.enc.quit()
        sys.exit(0)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(prog="squeaky_chat")

  chat = SqueakyChat()
  chat.start_chat()
  
