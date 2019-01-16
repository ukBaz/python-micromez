
sudo apt-get install python3-pip
sudo pip3 install setuptools
sudo pip3 install freetype-py
sudo apt-get install libfreetype6-dev
./font_to_py.py /usr/share/fonts/opentype/ipafont-gothic/ipag.ttf 16 myfont.py


Building mraa
=============
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

```python
from time import sleep
import mraa
cs_pin = mraa.Gpio(12)
cs_pin.dir(mraa.DIR_OUT)
dev = mraa.Spi(0)

txbuf = bytearray([0x01, 0x80, 0x00])

while True:
    cs_pin.write(False)
    rxbuf = dev.write(txbuf)
    cs_pin.write(True)
    print(rxbuf)
    # print(struct.unpack(">H", rxbuf[1:]))
    print(((rxbuf[1] & 0x03) << 8) | rxbuf[2])
    sleep(1)
```

sudo apt-get install python-dev python3-dev
sudo apt-get install python3-pip

sudo pip3 install spidev

