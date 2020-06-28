# TURING-CAMERA-RPI - camera capture service for the native Raspberry Pi camera  

## INSTALLATION STEPS FOR SCRIPTING  

### On MacOS
sudo apt-get install libjpeg-dev  
sudo apt-get install zlib1g-dev  
sudo apt-get install libpng-dev  
sudo pip install pillow  

### On RaspberryPi
sudo apt update  
sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
   pkg-config libgl1-mesa-dev libgles2-mesa-dev \
   python-setuptools libgstreamer1.0-dev git-core \
   gstreamer1.0-plugins-{bad,base,good,ugly} \
   gstreamer1.0-{omx,alsa} python-dev libmtdev-dev \
   xclip xsel libjpeg-dev
