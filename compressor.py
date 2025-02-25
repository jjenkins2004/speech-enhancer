import numpy as np
from compressorHelper import definitions
from compressorHelper import envelope
import math

#takes a 2d numpy array of 16 bit audio samples and applies dynamic range compression based on the settings
def compress(audio):

    #initialize variables 
    processed = 0
    audioLength = audio.shape[0]
    audioChannels = audio.shape[1]
    result = np.zeros((audioLength, audioChannels), dtype=np.int16) #this nparray will store the processed audio

    #main loop which will apply dynamic range compression in blocks of 512, defined by mBlockSize
    while(processed < audioLength):
        
        #find the number of frames to process on this iteration
        toprocess = min(audioLength-processed, definitions.mBlockSize)

        #update envelope
        envelope.UpdateEnvelope(toprocess)

        #apply envelope
        envelope.ApplyEvelope()
        
    return result