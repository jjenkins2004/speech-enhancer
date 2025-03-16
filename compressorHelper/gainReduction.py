import definitions as d
import math

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

def pushSamples():
    return

def process():
    return

def readSamples():
    return