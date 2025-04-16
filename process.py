from audioIO import loadAudio
from audioIO import writeAudio
from dynamic_range_compression import compress
import faulthandler; faulthandler.enable()
from rnnoise_wrapper import rnnoise_process

threshold = -10
ratio = 10
attack = 10
release = 500
makeupGain = 0
kneeWidth = 10
lookAhead = 50


class CompressorSettings:
    def __init__(
        self,
        thresholdDb,
        makeupGainDb,
        kneeWidthDb,
        compressionRatio,
        lookAheadMs,
        attackMs,
        releaseMs,
        sampleRate,
    ):
        self.thresholdDb = thresholdDb
        self.makeupGainDb = makeupGainDb
        self.kneeWidthDb = kneeWidthDb
        self.compressionRatio = compressionRatio
        self.lookAheadMs = lookAheadMs
        self.attackMs = attackMs
        self.releaseMs = releaseMs
        self.sampleRate = sampleRate


def main():
    audio, sr = loadAudio("audio/test.m4a")
    settings = CompressorSettings(
        thresholdDb=threshold,
        makeupGainDb=makeupGain,
        kneeWidthDb=kneeWidth,
        compressionRatio=ratio,
        lookAheadMs=lookAhead,
        attackMs=attack,
        releaseMs=release,
        sampleRate=sr,
    )
    audio = compress(audio, settings)
    rnnoise_process(audio)
    writeAudio(audio, sr)


if __name__ == "__main__":
    main()
