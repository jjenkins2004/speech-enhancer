from . import definitions as d
import math

# helper functions for computing gain reduction and lookahead gain reduction


# computing gain
def computeGainInDecibelsFromSidechainSignal(audio, processed, numSamples):
    d.maxInputLevel = float("-inf")
    d.maxGainReduction = 0.0

    for i in range(numSamples):
        # convert the current signal to decibals
        epsilon = 1e-10
        value = abs(d.mEnvelope[i])
        if value < epsilon:
            value = epsilon
        levelInDecibels = d.log2ToDb * math.log2(value)

        # update the max input level
        if levelInDecibels > d.maxInputLevel:
            d.maxInputLevel = levelInDecibels

        # calculate the overshoot compared to the set threshold
        overShoot = levelInDecibels - d.inCompressionThreshDb

        # apply soft-knee compression curve, applying reduction based on how far input level exceeds threshold
        gainReduction = 0.0
        kneeHalf = d.kneeWidthDb / 2
        if overShoot <= -kneeHalf:
            gainReduction = 0.0
        elif overShoot <= kneeHalf:
            gainReduction = (
                0.5
                * d.slope
                * (overShoot + kneeHalf)
                * (overShoot + kneeHalf)
                / d.kneeWidthDb
            )
        else:
            gainReduction = d.slope * overShoot

        # factor in attack or release
        diff = gainReduction - d.state
        if diff < 0:
            d.state += d.alphaAttack * diff
        else:
            d.state += d.alphaRelease * diff

        # apply the gain reduction
        d.mEnvelope[i] = d.state

        # update max gain reduction
        if d.state < d.maxGainReduction:
            d.maxGainReduction = d.state


# yeah i have no idea how the lookahead gain reduction works and looks way to hard to figure out
# shout out to Daniel Rudrich for making this
# https://github.com/audacity/audacity/blob/a96466f4924ea4c7525e1a4429d55070e685f17e/au3/libraries/lib-dynamic-range-processor/SimpleCompressor/LookAheadGainReduction.cpp


# push current samples into circular buffer
def pushSamples(numSamples):
    startIndex = 0
    blockSize1 = 0
    blockSize2 = 0
    pos = d.writePosition
    L = d.buffer.size

    if pos < 0:
        pos += L
    pos = pos % L

    if numSamples > 0:
        startIndex = pos
        blockSize1 = min(L - pos, numSamples)
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
    nextGainReductionValue = 0.0
    step = 0.0

    index = d.writePosition - 1
    if index < 0:
        index += d.buffer.size

    size1 = 0
    size2 = 0
    if d.lastPushedSamples > 0:
        size1 = min(index + 1, d.lastPushedSamples)
        samplesLeft = d.lastPushedSamples - size1
        size2 = 0 if samplesLeft <= 0 else samplesLeft

    for i in range(size1):
        smpl = d.buffer[index]

        if smpl > nextGainReductionValue:
            d.buffer[index] = nextGainReductionValue
            nextGainReductionValue += step
        else:
            step = -smpl / d.delayInSamples
            nextGainReductionValue = smpl + step
        index -= 1

    if size2 > 0:
        index = d.buffer.size - 1

        for i in range(size2):
            smpl = d.buffer[index]

            if smpl > nextGainReductionValue:
                d.buffer[index] = nextGainReductionValue
                nextGainReductionValue += step
            else:
                step = -smpl / d.delayInSamples
                nextGainReductionValue = smpl + step
            index -= 1

    if index < 0:
        index = d.buffer.size - 1

    size1 = 0
    size2 = 0
    if d.delayInSamples > 0:
        size1 = min(index + 1, d.delayInSamples)
        samplesLeft = d.delayInSamples - size1
        size2 = 0 if samplesLeft <= 0 else samplesLeft

    breakWasUsed = False

    for i in range(size1):
        smpl = d.buffer[index]

        if smpl > nextGainReductionValue:
            d.buffer[index] = nextGainReductionValue
            nextGainReductionValue += step
        else:
            breakWasUsed = True
            break
        index -= 1

    if (not breakWasUsed) and size2 > 0:
        index = d.buffer.size - 1
        for i in range(size2):
            smpl = d.buffer[index]

            if smpl > nextGainReductionValue:
                d.buffer[index] = nextGainReductionValue
                nextGainReductionValue += step
            else:
                break
            index -= 1


def readSamples(numSamples):
    startIndex = 0
    blockSize1 = 0
    blockSize2 = 0
    pos = d.writePosition - d.lastPushedSamples - d.delayInSamples
    L = d.buffer.size

    if pos < 0:
        pos += L
    pos = pos % L

    if numSamples > 0:
        startIndex = pos
        blockSize1 = min(L - pos, numSamples)
        samplesLeft = numSamples - blockSize1
        blockSize2 = 0 if samplesLeft <= 0 else samplesLeft

    # Copy blockSize1 samples from d.buffer starting at startIndex into d.mEnvelope
    d.mEnvelope[:blockSize1] = d.buffer[startIndex : startIndex + blockSize1]

    # If there are wrapped samples, copy blockSize2 samples from the start of d.buffer
    if blockSize2 > 0:
        d.mEnvelope[blockSize1 : blockSize1 + blockSize2] = d.buffer[:blockSize2]
