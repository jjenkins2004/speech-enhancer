import numpy as np
import sys
import os
#getting path for the noise_reduction c library
current_dir = os.getcwd()
lib_dir = os.path.join(current_dir, 'rnnoise_IO')
sys.path.append(lib_dir)
import noise_reduction

def rnnoise_process(array):
    noise_reduction.rnnoise_process(array)
    

