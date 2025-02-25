import numpy as np
from compressorHelper import definitions
from compressorHelper import envelope
from compressorHelper import delay
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
        toProcess = min(audioLength-processed, definitions.mBlockSize)

        #TODO implement the updateEnvelope function
        #update envelope
        envelope.UpdateEnvelope(audio, processed, toProcess)
        
        #TODO implement the CopyWithDelay
        #update deplaying data
        delay.CopyWithDelay(toProcess)

        #TODO implement the apply evelope function
        #apply envelope and get data values
        delayedInputAbsMax, delayedInputAbsMaxIndex = envelope.ApplyEvelope()

        #saving maximum values into mLastFrameStats
        blockMaxDb = definitions.log2ToDb * math.log2(delayedInputAbsMax)
        mLastFrameStats = definitions.mLastFrameStats
        if (mLastFrameStats.maxInputSampleDb < blockMaxDb):
            mLastFrameStats.maxInputSampleDb = blockMaxDb;
            mLastFrameStats.dbGainOfMaxInputSample = definitions.mEnvelope[delayedInputAbsMaxIndex];
        
        #increment number of frames processed
        processed += toProcess



    return result