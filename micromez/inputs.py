from time import sleep
import mraa


class Si7034:
    """
    The Si7034 I2C Humidity and Temperature Sensor
    """
    _heater_settings = [0x00, 0x10, 0x11, 0x12, 0x14, 0x18, 0x1f]

    def __init__(self, bus=1, i2c_addr=0x70):
        self.device = mraa.I2c(bus)
        self.device.address(i2c_addr)
        self.heater = 0

    @property
    def temperature(self):
        """
        Get the current temperature reading (Centigrade)
        """
        reg_value = self.device.readBytesReg(0x7c, 0xa2)
        return self._calc_temp(reg_value[0], reg_value[1])

    def _calc_temp(self, reg0, reg1):
        temp_code = int.from_bytes([reg0, reg1], byteorder='big')
        act_temp = -45 + 175 * (temp_code / 2 ** 16)
        return round(act_temp, 2)

    @property
    def humidity(self):
        """
        Get the current humidity reading (Relative Humidity)
        """
        reg_value = self.device.readBytesReg(0x7c, 0xa2)
        return self._calc_rh(reg_value[3], reg_value[4])

    def _calc_rh(self, reg0, reg1):
        rh_code = int.from_bytes([reg0, reg1], byteorder='big')
        act_rh = 100 * (rh_code / 2 ** 16)
        return round(act_rh, 2)

    @property
    def heater(self):
        """
        The Si7034 contains an integrated resistive heating element that
        may be used to raise the temperature of the sensor.
        This element can be used to test the sensor, to drive off
        condensation, or to implement dew-point measurement when the
        Si7034 is used in conjunction with a separate temperature
        sensor such as another Si7034 (the heater will raise the
        temperature of the internal temperature sensor).
        """
        set_at = self.device.readWordReg(0xe7)
        return Si7034._heater_settings.index(set_at)

    @heater.setter
    def heater(self, value):
        self.device.writeReg(0xe6, Si7034._heater_settings[value])


class LIS2DS12:
    """
    ultra-low-power high-performance three-axis linear accelerometer
    """
    _WHO_AM_I = 0x0f
    _CTRL1 = 0x20
    _CTRL2 = 0x21
    _CTRL3 = 0x22
    _CTRL4 = 0x23
    _CTRL5 = 0X24
    _FIFO_CTRL = 0x25
    _OUT_T = 0x26
    _STATUS = 0x27
    _OUT_X_L = 0x28
    _OUT_X_H = 0x29
    _OUT_Y_L = 0x2a
    _OUT_Y_H = 0x2b
    _OUT_Z_L = 0x2c
    _OUT_Z_H = 0x2d
    _TAP_6D_THS = 0x31
    _6D_SRC = 0x39
    _FUNC_CTRL = 0x3f

    def __init__(self, bus=1, i2c_addr=0x1d):
        self.device = mraa.I2c(bus)
        self.device.address(i2c_addr)

    def __enter__(self):
        return self

    def __del__(self):
        self.clean_up()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clean_up()

    def clean_up(self):
        self.powered = False

    @property
    def power_mode(self):
        """
        selection of the different operating modes
        (Not yet implemented)
        """
        return False

    @property
    def powered(self):
        """
        Turn the device on with True and off with False
        """
        return self.device.readReg(LIS2DS12._CTRL1) > 0

    @powered.setter
    def powered(self, state):
        """
        Turn the device off
        """
        if state:
            self.device.writeReg(LIS2DS12._CTRL1, 0xf0)
            sleep(0.025)
        else:
            self.device.writeReg(LIS2DS12._CTRL1, 0x00)

    @property
    def steps_enabled(self):
        """
        Enable the counting of steps

        """
        step_count_bit = 0b00000001
        state = self.device.readReg(LIS2DS12._FUNC_CTRL)
        return step_count_bit & state

    @steps_enabled.setter
    def steps_enabled(self, state):
        """
        Enable the counting of steps

        """
        if state:
            self.device.writeReg(LIS2DS12._CTRL1, 0b00100000)
            self.device.writeReg(LIS2DS12._FUNC_CTRL, 0b00000001)
            self.device.writeReg(LIS2DS12._CTRL5, 0b00110100)
        else:
            step_count_bit = 0b00000001
            current_state = self.device.readReg(LIS2DS12._FUNC_CTRL)
            step_off = current_state & (~step_count_bit)
            self.device.writeReg(LIS2DS12._FUNC_CTRL, step_off)

    @property
    def tilt_enabled(self):
        """
        Enable notification of changes in orientation
        """
        tilt_bit = 0b00010000
        state = self.device.readReg(LIS2DS12._FUNC_CTRL)
        return tilt_bit & state

    @tilt_enabled.setter
    def tilt_enabled(self, state):
        """
        Enable notification of changes in orientation
        """
        if state:
            self.device.writeReg(LIS2DS12._CTRL1, 0b01100000)
            self.device.writeReg(LIS2DS12._TAP_6D_THS, 0b01000000)
            self.device.writeReg(LIS2DS12._FUNC_CTRL, 0b00110000)
            self.device.writeReg(LIS2DS12._CTRL4, 0b00000100)
            self.device.writeReg(LIS2DS12._CTRL3, 0b00000110)
        else:
            tilt_bit = 0b00000100
            current_state = self.device.readReg(LIS2DS12._CTRL4)
            tilt_off = current_state & (~tilt_bit)
            self.device.writeReg(LIS2DS12._CTRL4, tilt_off)

    @property
    def tilt(self):
        """
        The current orientation of the device
        32: Face up
        16: Face down
        8: landscape - back high
        4: landscape - front high
        2: portrait - left high
        1: portrait - right high
        """
        event_bit = 0b01000000
        reading = self.device.readReg(LIS2DS12._6D_SRC)
        return reading & (~event_bit)

    @property
    def steps(self):
        """
        Step count
        """
        return int.from_bytes([self.device.readReg(0x3b),
                               self.device.readReg(0x3c)],
                              byteorder='little', signed=True)

    def reset_steps(self):
        """
        Reset the step count
        """
        self.device.writeReg(0x3A, 0b10010000)
        sleep(0.025)
        self.device.writeReg(0x3A, 0b00010000)

    @property
    def temperature(self):
        """
        Value of current temperature
        """
        return 25 + int.from_bytes([self.device.readReg(0x26)],
                                   byteorder='little', signed=True)

    @property
    def who_am_i(self):
        """
        Device information
        """
        return self.device.readReg(0x0f)

    @property
    def x(self):
        """
        Raw value of X-axis
        """
        return int.from_bytes([self.device.readReg(0x28),
                               self.device.readReg(0x29)],
                              byteorder='little', signed=True)

    @property
    def y(self):
        """
        Raw value of Y-axis
        """
        return int.from_bytes([self.device.readReg(0x2a),
                               self.device.readReg(0x2b)],
                              byteorder='little', signed=True)

    @property
    def z(self):
        """
        Raw value of Z-axis
        """
        return int.from_bytes([self.device.readReg(0x2c),
                               self.device.readReg(0x2d)],
                              byteorder='little', signed=True)

    @property
    def value(self):
        """
        List of raw X, Y, and Z axis
        :return:
        """
        return [self.x, self.y, self.z]


class Lp3990:
    """
    LP3990 150-mA Linear Voltage Regulator for powering the OLED display
    """
    def __init__(self, en_pin=34):
        self._en_3v3 = mraa.Gpio(en_pin)
        self._en_3v3.dir(mraa.DIR_OUT)

    @property
    def powered(self):
        """
        State of the enable signal on regulator
        """
        return self._en_3v3.read()

    @powered.setter
    def powered(self, state):
        self._en_3v3.write(state)


class Button:
    """
    Accessing the Buttons

    :param btn: Required button (A, B, C or D)
    """
    def __init__(self, btn):
        btn_to_pin = {'A': 33,
                      'B': 31,
                      'C': 29,
                      'D': 27,
                      'INT1': 23,
                      'INT2': 25}
        try:
            self._btn = mraa.Gpio(btn_to_pin[btn.upper()])

        except KeyError:
            print('Button name is one of {}'.format(btn_to_pin.keys()))
        self._btn.dir(mraa.DIR_IN)

    @property
    def is_pressed(self):
        """
        Get state of button

        :return: ``True`` if the button is currently pressed otherwise
                 ``False``
        """
        return not self._btn.read()

    @property
    def when_pressed(self):
        """
        The function to run when the button is pressed.

        :param callback: Python to be executed when button pressed
        """
        pass

    @when_pressed.setter
    def when_pressed(self, callback):
        self._btn.isr(mraa.EDGE_FALLING, callback, None)
