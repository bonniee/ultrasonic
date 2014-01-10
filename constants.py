# Audio constants
RATE = 44100
CHUNK_SIZE = 512
AUDIOBUF_SIZE = 2048

# Constants for FSK
BASELINE = 19400.0

CHARSTART = 19600.0
CHARSTART_THRESH = 100

ZERO = 19800.0
ZERO_THRESH = 20

ONE = 20000.0
ONE_THRESH = 20

BIT_DURATION = 0.2
IDLE_LIMIT = 20 # If we don't hear anything for a while (~2sec), clear buffer.
