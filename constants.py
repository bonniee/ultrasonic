# Audio constants
RATE = 44100
CHUNK_SIZE = 512

# Constants for FSK
ZERO = 19000.0
ONE = 19200.0
BIT_DURATION = 0.125
THRESHOLD = 1000
THRESH_HIGH = 8000
THRESH_LOW = 500
SMOOTH_COUNT = 3
IDLE_LIMIT = 100 # If we don't hear anything for a while, clear buffer.
