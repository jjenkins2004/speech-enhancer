import numpy as np
import math

yL_prev = 0


#takes a numpy array of audio samples and audio sample rate
def compress(audio, sr, threshold, ratio, attack, release, makeupGain, kneeWidth):

    # loop through all audio samples, audio range compression works by changing the amplitude 
    # of the sample based on the range compression settings. Multiplying the amplitude affects
    # the loudness of the sound sample.
    
    for sample in audio:
        mono_sample = np.mean(sample)
        control_gain = gain_computer(mono_sample, samplerate=sr)
        print(f"control gain: {control_gain}")
        print(f"initial sample: {sample}")
        sample *= control_gain
        print(f"new sample: {sample}")

#THIS DOESNT WORK....
#need to convert this code to python...
#https://github.com/audacity/audacity/blob/ef2bd94750cfc4a2df4545822f553d894346482b/au3/libraries/lib-dynamic-range-processor/CompressorProcessor.cpp

# this just calculates the factor that the sample should be multiplied by based on the settings
# of the range compression and the amplitude of the sample.
def gain_computer(sample, threshold=-20, ratio=3, attack=100, release=200, makeupGain=None, kneeWidth=2.5, samplerate=44100):
    global yL_prev
    if makeupGain is None:
        makeupGain = (1*ratio-1) * threshold * 0.5
    
    
    alphaAttack = math.exp(-1/(0.001 * samplerate * attack))
    alphaRelease= math.exp(-1/(0.001 * samplerate * release))
    
    # Level detection- estimate level using peak detector
    if (abs(sample) < 0.000001):
        x_g =-120
    else:
        x_g = 20*math.log10(abs(sample))
    
    # Apply second order interpolation soft knee
    if ((2* abs(x_g-threshold)) <= kneeWidth):
    # Quadratic Interpolation
        # y_g = x_g + (1*ratio -1) * ((x_g-threshold+kneeWidth)*(x_g-threshold+kneeWidth)) / (4*kneeWidth)
    # Linear Interpolation
        y_g = threshold - kneeWidth*0.5 + (x_g-threshold+kneeWidth*0.5)*(1+ratio)*0.5
    elif ((2*(x_g-threshold)) > kneeWidth):
        y_g = threshold + (x_g - threshold) * ratio
    else:
        y_g = x_g
    
    x_l = x_g - y_g
    
    # Ballistics- smoothing of the gain
    if (x_l > yL_prev):
        y_l = alphaAttack * yL_prev + (1 - alphaAttack ) * x_l
    else:
        y_l = alphaRelease * yL_prev + (1 - alphaRelease) * x_l
    
    c = math.pow(10,(makeupGain - y_l)*0.05)
    yL_prev = y_l
    
    return c