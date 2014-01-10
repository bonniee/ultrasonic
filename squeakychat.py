from sound_decoder import *
from sound_encoder import *
import curses, traceback, sys, os, argparse, nltk, string, viterbi

class SqueakyChat:

  def __init__(self, viterbi_flag=False):
    
    # Set up audio backend
    self.TEMP_FILE = 'tmp.wav'
    self.COIN = "smb_coin.wav"
    self.enc = Encoder()
    self.dec = Decoder(0)
    self.dec.attach_character_callback(self.printer)
    self.dec.attach_idle_callback(self.idle_callback)
    self.buf = ''

    self.should_viterbi = viterbi_flag


  def toggleBit(int_type, offset):
    mask = 1 << offset
    return(int_type ^ mask)

  def viterbify(self):
    input_str = self.buf
    if len(input_str) < 1:
      return
    self.buf = ''

    corpus = nltk.corpus.nps_chat.raw()
    alpha = string.ascii_letters + string.digits + string.punctuation
    print alpha
    start_probs, trans_probs = viterbi.get_probabilities(corpus, alpha)
    viterbi_obj = viterbi.Viterbi(start_probs, trans_probs)
    print 'viterbify! str = ' + input_str

    for char in input_str:
      print 'viterbi: handling char ' + char
      probs_dict = {char : 0 for char in alpha}
      probs_dict[char] = 0.8
      for i in range(8):
        weird = ord(char) ^ (1 << i)
        if chr(weird) in probs_dict:
          print 'toggle bit: ' + chr(weird)
          probs_dict[chr(weird)] = 0.025
      viterbi_obj.observe(probs_dict)
      print 'Viterbi BEST PATH'
      print viterbi_obj.best_path()


  def idle_callback(self):
    # print 'idle_callback'
    if len(self.buf) > 0:
      self.viterbify()

  def printer(self, char):
    print 'received ' + char
    if self.should_viterbi:
      if (char is '\n'):
        self.viterbify()
      self.buf += char
    else:
      sys.stdout.write('%s' % char)
      sys.stdout.flush()

  def start_chat(self):
    while True:
      try:
        s = raw_input('')
        if len(s) < 1:
          continue
        s = '\n' + s + '\n'
        self.enc.encode(s, self.TEMP_FILE)
        self.dec.stop_listening()
        os.system("afplay " + self.TEMP_FILE)
        os.system("rm " + self.TEMP_FILE)
        self.dec.start_listening()

      except:
        # traceback.print_exc(file=sys.stdout)
        self.dec.quit()
        sys.exit(0)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(prog="squeaky_chat")
  parser.add_argument('--v', help="Use Viterbi", action="store_true")
  args = parser.parse_args()
  print args

  chat = SqueakyChat(args.v)
  chat.start_chat()
