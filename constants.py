# Audio constants
RATE = 44100
CHUNK_SIZE = 512

# Constants for FSK
# ZERO = 19000.0
# ONE = 19200.0
ZERO = 19000.0
ONE = 19200.0
BIT_DURATION = 0.2
THRESHOLD = 1000
SMOOTH_COUNT = 3
IDLE_LIMIT = 100 # If we don't hear anything for 100 chunks (2ish seconds with 1024), clear buffer
