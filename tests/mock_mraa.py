
class mraa:
    DIR_IN = 1
    DIR_OUT = 0
    DIR_OUT_HIGH = 2
    DIR_OUT_LOW = 3
    EDGE_BOTH = 1
    EDGE_FALLING = 3
    EDGE_NONE = 0
    EDGE_RISING = 2

    def getVersion(self):
        return 'v1.7.0'

    class Gpio:
        pin_lookup = {}
        pins = {}

        def __init__(self, pin, owner=True, raw=False):
            if self in mraa.Gpio.pins:
                pass
            else:
                mraa.Gpio.pin_lookup[self] = str(pin)
                mraa.Gpio.pins[str(pin)] = {'dir': mraa.DIR_IN,
                                            'edge': mraa.EDGE_BOTH,
                                            'state': True
                                            }

        def dir(self, dir):
            pin_number = mraa.Gpio.pin_lookup[self]
            mraa.Gpio.pins[pin_number]['dir'] = dir

        def read(self):
            pin_number = mraa.Gpio.pin_lookup[self]
            return mraa.Gpio.pins[pin_number]['state']

        def write(self, value):
            pin_number = mraa.Gpio.pin_lookup[self]
            mraa.Gpio.pins[pin_number]['state'] = bool(value)

    class I2c:
        devices = {}
        # devices['1']['0x70']['0x7c0xa2']
        Si7034_TEMP_HUM = [0x6e, 0x14, 0x3e, 0x71, 0xff, 0xe2]

        def __init__(self, bus):
            self.bus = str(bus)
            self.i2c_addr = None
            if self.bus in mraa.I2c.devices:
                pass
            else:
                mraa.I2c.devices[self.bus] = {}

        def _check_LIS2DS12_powered(self, hex_reg):
            NEED_POWER_ENABLED = ['0x26', '0x28', '0x29', '0x2a', '0x2b', '0x2c', '0x2d', '0x3b', '0x3c']
            if hex_reg in NEED_POWER_ENABLED:
                return mraa.I2c.devices[self.bus][self.i2c_addr]['0x20'] > 0
            else:
                return True

        def address(self, i2c_addr):
            self.i2c_addr = str(hex(i2c_addr))
            if self.i2c_addr in mraa.I2c.devices[self.bus]:
                pass
            else:
                mraa.I2c.devices[self.bus][self.i2c_addr] = {}
            if self.i2c_addr == '0x70':
                mraa.I2c.devices[self.bus][self.i2c_addr]['0x7c0xa2'] = mraa.I2c.Si7034_TEMP_HUM
                mraa.I2c.devices[self.bus][self.i2c_addr]['0xe6'] = 0
                mraa.I2c.devices[self.bus][self.i2c_addr]['0xe7'] = 0
            if self.i2c_addr == '0x1d':
                mraa.I2c.devices[self.bus][self.i2c_addr]['0xf'] = 0x43
                mraa.I2c.devices[self.bus][self.i2c_addr]['0x20'] = 0
                mraa.I2c.devices[self.bus][self.i2c_addr]['0x21'] = 0
                mraa.I2c.devices[self.bus][self.i2c_addr]['0x22'] = 0
                mraa.I2c.devices[self.bus][self.i2c_addr]['0x23'] = 0
                mraa.I2c.devices[self.bus][self.i2c_addr]['0x24'] = 0
                mraa.I2c.devices[self.bus][self.i2c_addr]['0x25'] = 0
                mraa.I2c.devices[self.bus][self.i2c_addr]['0x26'] = 4
                mraa.I2c.devices[self.bus][self.i2c_addr]['0x27'] = 0
                mraa.I2c.devices[self.bus][self.i2c_addr]['0x28'] = 0
                mraa.I2c.devices[self.bus][self.i2c_addr]['0x29'] = 0
                mraa.I2c.devices[self.bus][self.i2c_addr]['0x2a'] = 0
                mraa.I2c.devices[self.bus][self.i2c_addr]['0x2b'] = 0
                mraa.I2c.devices[self.bus][self.i2c_addr]['0x2c'] = 0
                mraa.I2c.devices[self.bus][self.i2c_addr]['0x2d'] = 0
                mraa.I2c.devices[self.bus][self.i2c_addr]['0x31'] = 0
                mraa.I2c.devices[self.bus][self.i2c_addr]['0x39'] = 0
                mraa.I2c.devices[self.bus][self.i2c_addr]['0x3b'] = 0
                mraa.I2c.devices[self.bus][self.i2c_addr]['0x3c'] = 0
                mraa.I2c.devices[self.bus][self.i2c_addr]['0x3f'] = 0

        def readBytesReg(self, reg, data):
            loc = str(hex(reg)) + str(hex(data))
            if mraa.I2c.devices[self.bus][self.i2c_addr] == 0x1d:
                if mraa.I2c.devices[self.bus][0x20] > 0:
                    rtrn = mraa.I2c.devices[self.bus][self.i2c_addr][loc]
                else:
                    rtrn = 0
            else:
                rtrn = mraa.I2c.devices[self.bus][self.i2c_addr][loc]
            return rtrn

        def writeReg(self, reg, data):
            mraa.I2c.devices[self.bus][self.i2c_addr][str(hex(reg))] = data

            if self.i2c_addr == '0x1d' and '0x3a' == str(hex(reg)):
                reset_bit = 0b10000000
                if reset_bit != (mraa.I2c.devices[self.bus][self.i2c_addr][str(hex(reg))] & reset_bit):
                    mraa.I2c.devices[self.bus][self.i2c_addr]['0x3b'] = 0
                    mraa.I2c.devices[self.bus][self.i2c_addr]['0x3c'] = 0

        def readWordReg(self, reg):
            if self.i2c_addr == '0x70' and str(hex(reg)) == '0xe7':
                reg = 0xe6
            return mraa.I2c.devices[self.bus][self.i2c_addr][str(hex(reg))]

        def readReg(self, reg):
            hex_reg = str(hex(reg))
            if self.i2c_addr == '0x1d':
                if self._check_LIS2DS12_powered(hex_reg):
                    rtrn = mraa.I2c.devices[self.bus][self.i2c_addr][hex_reg]
                else:
                    rtrn = 0
            else:
                rtrn = mraa.I2c.devices[self.bus][self.i2c_addr][hex_reg]
            return rtrn
