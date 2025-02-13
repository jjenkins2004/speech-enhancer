import numpy as np
import subprocess

# define the command to fix the install_name for for wrapper linking
command = [
    "install_name_tool",
    "-change",
    "/usr/local/lib/librnnoise.0.dylib",
    "@loader_path/../rnnoise-main/.libs/librnnoise.0.dylib",
    "rnnoise_IO/noise_reduction.so"
]

# execute the command
try:
    subprocess.run(command, check=True)
except subprocess.CalledProcessError as e:
    print(f"Error executing install_name_tool: {e}")

import sys
import os

#getting path for the noise_reduction c library
current_dir = os.getcwd()
lib_dir = os.path.join(current_dir, 'rnnoise_IO')
sys.path.append(lib_dir)

import noise_reduction

# Create a numpy array (this will be passed to your C function)
input_array = np.array([1.0, 2.0, 3.0, 4.0], dtype=np.float32)

# Call your C function wrapped in the Python module
noise_reduction.rnnoise_process(input_array)

