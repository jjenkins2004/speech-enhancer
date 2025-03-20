import numpy as np
from compressorHelper import definitions as d
from compressorHelper import envelope
import math
import logging

# Configure the logging: you can set the level and output format.
logging.basicConfig(
    filename="compressor.log",  # log file name
    filemode="w",  # appending to the file; use 'w' to overwrite each run
    level=logging.DEBUG,  # minimum level to log
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# Value Ranges:
# Lookahead max: 1000 ms


# takes an unnormalized 2d numpy array of 16 bit audio samples and applies dynamic range compression based on the settings
def compress(audio, settings):

    # normalize audio
    normalized_audio = audio.astype(np.float32) / 32768.0

    # initialize variables
    processed = 0
    audioLength = normalized_audio.shape[1]
    audioChannels = normalized_audio.shape[0]

    # initialize settings
    d.setSettings(
        audioChannels,
        settings.thresholdDb,
        settings.makeupGainDb,
        settings.kneeWidthDb,
        settings.compressionRatio,
        settings.lookAheadMs,
        settings.attackMs,
        settings.releaseMs,
        settings.sampleRate,
    )

    logging.info(
        "[Compressor]: Initialized, channels: %d, length: %d",
        audioChannels,
        audioLength,
    )

    # main loop which will apply dynamic range compression in blocks of 512, defined by mBlockSize
    while processed < audioLength:
        # find the number of frames to process on this iteration
        toProcess = min(audioLength - processed, d.mBlockSize)
        logging.info("[Compressor]: Processed %d / %d", processed, audioLength)

        # print("[Compressor]: Updating Envelope")
        # update envelope
        envelope.UpdateEnvelope(normalized_audio, processed, toProcess)

        # print("[Compressor]: Updating delayed data")
        # update delayed data, copy the currently block bring processed in audio with an offset of delay for every channel
        delay = d.delayInSamples
        d.delayedInput[:, delay : delay + toProcess] = normalized_audio[
            :, processed : processed + toProcess
        ]

        # print("[Compressor]: Applying Envelope")
        # apply envelope and get data values
        envelope.ApplyEnvelope(normalized_audio, processed, toProcess)

        # increment number of frames processed
        processed += toProcess

    # reconverting normalized audio into 16-bit
    return (normalized_audio * 32767).astype(np.int16)
