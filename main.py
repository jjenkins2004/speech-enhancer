from audioLoader import loadAudio
from compressor import compress

threshold = 20
ratio = 3
attack = 100
release = 200
makeupGain = None
kneeWidth = 2.5

def main():
    audio, sr = loadAudio("link")
    compress(audio, sr, threshold, ratio, attack, release, makeupGain, kneeWidth)

if __name__ == "__main__":
    main()