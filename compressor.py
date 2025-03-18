import numpy as np
from compressorHelper import definitions as d
from compressorHelper import envelope
import math

#Value Ranges:
#Lookahead max: 1000 ms

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
        toProcess = min(audioLength-processed, d.mBlockSize)

        #update envelope
        envelope.UpdateEnvelope(audio, processed, toProcess)
        
        #update delayed data, copy the currently block bring processed in audio with an offset of delay for every channel
        delay = d.delayInSamples
        d.mDelayedInput[:, delay : delay + toProcess] = audio[:, processed : processed + toProcess]

        #TODO implement the apply evelope function
        #apply envelope and get data values
        delayedInputAbsMax, delayedInputAbsMaxIndex = envelope.ApplyEvelope()

        #saving maximum values into mLastFrameStats
        blockMaxDb = d.log2ToDb * math.log2(delayedInputAbsMax)
        mLastFrameStats = d.mLastFrameStats
        if (mLastFrameStats.maxInputSampleDb < blockMaxDb):
            mLastFrameStats.maxInputSampleDb = blockMaxDb;
            mLastFrameStats.dbGainOfMaxInputSample = d.mEnvelope[delayedInputAbsMaxIndex];
        
        #increment number of frames processed
        processed += toProcess



    return result