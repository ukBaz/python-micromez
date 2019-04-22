Overview
========
This is the Python library to support the micromez add-on board that is part of the 96Boards Mezzanine Community effort:
https://github.com/96boards/mezzanine-community/tree/master/boards/other/micromez

Documentation
=============
https://micromez.readthedocs.io/en/latest/overview.html


Building mraa
=============
This library has a dependancy on the mraa GPIO library which can be installed with Python bindings as follows:
```
sudo apt-get install git build-essential swig3.0 python3-dev nodejs-dev cmake libjson-c-dev

git clone https://github.com/intel-iot-devkit/mraa.git
cd mraa
mkdir build
cd build
cmake -DBUILDSWIG=ON \
      -DBUILDSWIGPYTHON=ON \
      -DBUILDSWIGPYTHON3=ON \
      -DBUILDSWIGNODE=OFF \
      -DBUILDSWIGJAVA=OFF \
      ..

make

sudo make install
```

Load additional Fonts
=====================
If more fonts are required in addition to the three provided, the following will need to be done:
```
sudo apt-get install python3-pip
sudo pip3 install setuptools
sudo pip3 install freetype-py
sudo apt-get install libfreetype6-dev
./font_to_py.py /usr/share/fonts/opentype/ipafont-gothic/ipag.ttf 16 myfont.py
```
