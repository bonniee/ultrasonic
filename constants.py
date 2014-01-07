# Audio constants
RATE = 44100
CHUNK_SIZE = 512

# Constants for FSK
BASELINE = 19400.0

CHARSTART = 19600.0
CHARSTART_THRESH = 100

ZERO = 19800.0
ZERO_THRESH = 20

ONE = 20000.0
ONE_THRESH = 20

BIT_DURATION = 0.1
IDLE_LIMIT = 50 # If we don't hear anything for a while, clear buffer.
