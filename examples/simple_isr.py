from signal import pause
from time import sleep
from random import randint
import mraa

print(mraa.getVersion())
print(mraa.getPlatformName())


def move_up(*args):
    print(args)


class Tilt:
    def __init__(self, bus=1, i2c_addr=0x1d, int1_pin=23):
        self._CTRL1 = 0x20
        self._CTRL3 = 0x22
        self._CTRL4 = 0x23
        self._TAP_6D_THS = 0x31
        self._6D_SRC = 0x39
        # Pin for interrupt signal
        self._int1 = mraa.Gpio(int1_pin)
        self._int1.dir(mraa.DIR_IN)
        self._int1.edge(mraa.EDGE_FALLING)
        # i2c bus to read orientation
        # self.device = mraa.I2c(bus)
        # self.device.address(i2c_addr)
        # self.device.writeReg(self._CTRL1, 0b01100000)
        # self.device.writeReg(self._TAP_6D_THS, 0b01000000)
        # self.device.writeReg(self._CTRL4, 0b00000100)
        # # latched interrupt (reset by reading _6D_SRC)
        # self.device.writeReg(self._CTRL3, 0b00000110)
        # # Pulse interrupt
        # # self.device.writeReg(self._CTRL3, 0b00000010)

    @property
    def int1(self):
        return not self._int1.read()

    @property
    def orientation(self):
        # return '{:08b}'.format(self.device.readReg(self._6D_SRC))
        return randint(0, 9)

    def on_new_data(self, fn, *args):
        self._int1.isr(mraa.EDGE_FALLING, fn, args[0])


class Button:
    def __init__(self, pin):
        self._btn = mraa.Gpio(pin)
        self._btn.dir(mraa.DIR_IN)
        self._btn.edge(mraa.EDGE_FALLING)
        self._readings = []

    def when_pressed(self, callback, *args):
        self._btn.isr(mraa.EDGE_FALLING, callback, args[0])


# Using Button class
btn1 = Button(33)
btn1.when_pressed(print, 'Test on btn1', ' plus stuff')


# All at top level
btn2 = mraa.Gpio(31)
btn2.dir(mraa.DIR_IN)
btn2.edge(mraa.EDGE_FALLING)
btn2.isr(mraa.EDGE_FALLING, print, 'Test on btn2')

# Tilt test
accel = Tilt()
accel.on_new_data(print, accel.orientation)


# while True:
#     if accel.int1:
#         print(accel.orientation)
#         sleep(0.25)

pause()
