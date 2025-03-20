import definitions as d
import gainReduction
import numpy as np
import math


def UpdateEnvelope(audio, processed, toProcess):
    # get the range of samples for each channel from the parameters
    block = audio[:, processed : processed + toProcess]

    # compute the maximum absolute value across channels for each sample in the block
    d.m_envelope = np.max(np.abs(block), axis=0)

    # compute the gain reduction based on the m_envelope
    gainReduction.computeGainInDecibelsFromSidechainSignal(toProcess)

    # quit early if there is no lookahead smoothing
    if d.lookaheadMs <= 0:
        return

    # do lookahead smoothing processing, no idea how this works...
    gainReduction.pushSamples(toProcess)
    gainReduction.process()
    gainReduction.readSamples(toProcess)


def ApplyEvelope(audio, processed, toProcess):
    # get values needed
    makeupGainDb = d.makeupGainDb
    delay = d.delayInSamples

    # loop through each channel
    for i in range(d.channels):

        #get delayed input from lookahead processing
        delayedIn = d.delayedInput[i]

        # process one channel at a time
        for j in range(toProcess):
            #calculate the gain factor
            gain_factor = math.pow(10, 0.05 * (d.mEnvelope[j] + makeupGainDb))

            #apply gain factor using delayedIn from lookahead processing
            audio[i][processed + j] = delayedIn[j] * gain_factor
            
        #shift delayed input 
        d.mDelayedInput[i][:delay] = delayedIn[toProcess:toProcess+delay]
