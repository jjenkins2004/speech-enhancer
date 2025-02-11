import numpy as np
import librosa as li

def loadAudio(link):
    audio,sr = li.load(link, sr=None)
    return audio,sr