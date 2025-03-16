

import definitions as d
import math

#helper functions for computing gain reduction and lookahead gain reduction


def computeGainInDecibelsFromSidechainSignal(numSamples):
    d.maxInputLevel = float('-inf')
    d.maxGainReduction = 0.0

    for i in range(numSamples):
        #convert the current signal to decibals
        levelInDecibals = d.log2ToDb * math.log2(abs(d.mEnvelope[i]))

        #update the max input level
        if (levelInDecibals > d.maxInputLevel):
            d.maxInputLevel = levelInDecibals
        
        #calculate the overshoot compared to the set threshold
        overShoot = levelInDecibals - d.inCompressionThreshDb

        #apply soft-knee compression curve, applying reduction based on how far input level exceeds threshold
        gainReduction = 0.0
        kneeHalf = d.kneeWidthDb/2
        if (overShoot <= -kneeHalf):
            gainReduction = 0.0
        elif (overShoot <= kneeHalf):
            gainReduction = 0.5 * d.slope * (overShoot + kneeHalf) * (overShoot + kneeHalf) / d.kneeWidthDb
        else:
            gainReduction = d.slope * overShoot

        #factor in attack or release
        diff = gainReduction - d.state
        if (diff < 0):
            d.state += d.alphaAttack * diff
        else:
            d.state += d.alphaRelease * diff
        
        #apply the gain reduction
        d.mEnvelope[i] = d.state

        #update max gain reduction
        if (d.state < d.maxGainReduction):
            d.maxGainReduction = d.state

def pushSamples(numSamples):
    startIndex = 0
    blockSize1 = 0
    blockSize2 = 0
    pos = d.writePosition
    L = d.buffer.size

    if (pos < 0):
        pos += L
    pos = pos % L

    if (numSamples > 0):
        startIndex = pos
        blockSize1 = min(L-pos, numSamples)
        samplesLeft = numSamples - blockSize1
        blockSize2 = 0 if samplesLeft <= 0 else samplesLeft

    # Copy blockSize1 samples from d.mEnvelope into d.buffer starting at startIndex
    d.buffer[startIndex : startIndex + blockSize1] = d.mEnvelope[:blockSize1]

    # If blockSize2 > 0, copy the next blockSize2 samples from d.mEnvelope into the beginning of d.buffer
    if blockSize2 > 0:
        d.buffer[:blockSize2] = d.mEnvelope[blockSize1 : blockSize1 + blockSize2]

    d.writePosition += numSamples
    d.writePosition = d.writePosition % L

    d.lastPushedSamples = numSamples

def process():
    return

def readSamples():
    return