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

#variables for gain reduction computation
alphaAttack = 0.0
alphaRelease = 0.0
state = 0.0
maxInputLevel = float('-inf')
maxGainReduction = 0.0
slope = 0.0

#variables for lookahead gain reduction computation
delay = 0.0
delayInSamples
writePosition = 0
buffer = []
lastPushedSamples = 0

#constants
mBlockSize = 512
log2ToDb = 20 / 3.321928094887362

def setSettings(thresh, makeupGain, kneeWidth, compRatio, lookahead, attack, release, sr):
    global inCompressionThreshDb, outCompressionThreshDb, kneeWidthDb
    global compressionRatio, lookaheadMs, attackMs, releaseMs, sampleRate
    global alphaAttack, alphaRelease, slope
    global delay, delayInSamples

    inCompressionThreshDb = thresh
    outCompressionThreshDb = inCompressionThreshDb + makeupGain
    kneeWidthDb = kneeWidth
    compressionRatio = compRatio
    lookaheadMs = lookahead
    attackMs = attack
    releaseMs = release
    sampleRate = sr

    #setting alphaAttack
    alphaAttack = 1.0 - math.exp(-1.0 / (sampleRate * attackMs/1000))

    #setting alphaRelease
    alphaRelease = 1.0 - math.exp(-1.0 / (sampleRate * releaseMs/1000))

    #setting slope based on compression ratio
    slope = 1 / compressionRatio - 1

    #lookahead delay time
    if (lookaheadMs > 0):
        delay = lookaheadMs/1000

    #setting lookahead circular buffer
    delayInSamples = int(delay * sampleRate)
    arr = np.zeros(mBlockSize + delayInSamples, dtype=float)


#keep track of last frame
class FrameStats:
    def __init__(self):
        self.max_input_sample_db = -math.inf 
        self.db_gain_of_max_input_sample = 0.0

mLastFrameStats = FrameStats()

#envelope definitions
mEnvelope = np.zeros(mBlockSize, dtype=np.float32)

