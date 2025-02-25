import definitions
import numpy as np

def UpdateEnvelope(audio, processed, toProcess):
    #get the range of samples for each channel from the parameters
    block = audio[:, processed:processed + toProcess]
    
    #compute the maximum absolute value across channels for each sample in the block
    definitions.m_envelope = np.max(np.abs(block), axis=0)

def ApplyEvelope():
    print("applying envelope...")