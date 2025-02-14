#!/bin/bash

#clone the rnnoise library
rm -rf rnnoise
git clone https://github.com/xiph/rnnoise.git

# setup rnnoise library
echo "downloading rnnoise files"
cd rnnoise
./autogen.sh
echo "configuring rnnoise library"
./configure
echo "making library"
make

# fix install_name of librnnoise.0.dylib
echo "fixing install_name of librnnoise.0.dylib"
install_name_tool -id @loader_path/../rnnoise/.libs/librnnoise.0.dylib .libs/librnnoise.0.dylib

#make the wrapper
cd ../rnnoise_IO
make clean
make
cd ..

echo "Setup complete!"