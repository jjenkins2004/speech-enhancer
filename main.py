from audioIO import loadAudio
from audioIO import writeAudio
from compressor import compress

threshold = -45
ratio = 40
attack = 10
release = 500
makeupGain = 27
kneeWidth = 0

def main():
    audio, sr = loadAudio("audio/test.m4a")
    print(audio)
    compress(audio, sr, threshold, ratio, attack, release, makeupGain, kneeWidth)
    writeAudio(audio, sr)

if __name__ == "__main__":
    main()