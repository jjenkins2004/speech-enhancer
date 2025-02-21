import numpy as np
from pydub import AudioSegment 

def loadAudio(link):
    #make this compatible with m4a format
    audio = AudioSegment.from_file(link)
    #get sample rate
    sr = audio.frame_rate
    #convert audio to samples
    samples = audio.get_array_of_samples()
    #convert array.array into numpy array
    sound_np = np.array(samples, dtype=np.int16)

    #return sample rate and np array
    return sound_np, sr
    

def writeAudio(audio, sr):
    #convert to pydub object for writing
    audio_data = AudioSegment(
        audio.tobytes(),        # Audio data in byte format
        frame_rate=sr,          # Sample rate
        sample_width=2,         # Sample width (2 bytes = 16-bit PCM)
        channels=1              # Mono audio
    )
    audio_data.export("processed/result.m4a", format="ipod")
