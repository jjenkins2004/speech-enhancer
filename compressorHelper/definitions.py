import math
import numpy as np

#settings
inCompressionThreshDb = -10
outCompressionThreshDb = -10
kneeWidthDb = 5
compressionRatio = 10
lookaheadMs = 1
attackMs = 30
releaseMs = 150
sampleRate = 44100

#constants
mBlockSize = 512

def setSettings(thresh, makeupGain, kneeWidth, compRatio, lookahead, attack, release, sr):
    global inCompressionThreshDb, outCompressionThreshDb, kneeWidthDb
    global compressionRatio, lookaheadMs, attackMs, releaseMs, sampleRate

    inCompressionThreshDb = thresh
    outCompressionThreshDb = inCompressionThreshDb + makeupGain
    kneeWidthDb = kneeWidth
    compressionRatio = compRatio
    lookaheadMs = lookahead
    attackMs = attack
    releaseMs = release
    sampleRate = sr

#keep track of last frame
class FrameStats:
    def __init__(self):
        self.max_input_sample_db = -math.inf 
        self.db_gain_of_max_input_sample = 0.0

mLastFrameStats = FrameStats()

#constant for converting to db
log2ToDb = 20 / 3.321928094887362

#envelope definitions
mEnvelope = np.zeros(mBlockSize, dtype=np.float32)
