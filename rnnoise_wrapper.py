import numpy as np

import sys
import os
current_dir = os.getcwd()
lib_dir = os.path.join(current_dir, 'rnnoise_IO')
sys.path.append(lib_dir)
import noise_reduction

# Create a numpy array (this will be passed to your C function)
input_array = np.array([1.0, 2.0, 3.0, 4.0], dtype=np.float32)

# Call your C function wrapped in the Python module
noise_reduction.rnnoise_process(input_array)

