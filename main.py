from audioIO import loadAudio
from audioIO import writeAudio
from compressor import compress
from rnnoise_wrapper import rnnoise_process

threshold = -45
ratio = 40
attack = 10
release = 500
makeupGain = 27
kneeWidth = 0

def main():
    audio, sr = loadAudio("audio/test.m4a")
    #rnnoise_process(audio)
    compress(audio, sr, threshold, ratio, attack, release, makeupGain, kneeWidth)
    writeAudio(audio, sr)
    # print(audio[0])
    # writeAudio(audio, sr)

if __name__ == "__main__":
    main()