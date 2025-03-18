import definitions
import gainReduction
import numpy as np

def UpdateEnvelope(audio, processed, toProcess):
    #get the range of samples for each channel from the parameters
    block = audio[:, processed:processed + toProcess]
    
    #compute the maximum absolute value across channels for each sample in the block
    definitions.m_envelope = np.max(np.abs(block), axis=0)

    #compute the gain reduction based on the m_envelope
    gainReduction.computeGainInDecibelsFromSidechainSignal(toProcess)

    #quit early if there is no lookahead smoothing
    if (definitions.lookaheadMs <= 0):
        return
    
    #do lookahead smoothing processing, no idea how this works...
    gainReduction.pushSamples(toProcess)
    gainReduction.process()
    gainReduction.readSamples()

def ApplyEvelope():
    print("applying envelope...")