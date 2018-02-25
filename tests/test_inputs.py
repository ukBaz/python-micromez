import unittest
from unittest.mock import patch
from tests import mock_mraa


class TestInputs(unittest.TestCase):

    def setUp(self):
        # self.mraa_mock = MagicMock()
        self.mraa_mock = mock_mraa.mraa()
        modules = {
            'mraa': self.mraa_mock,
        }
        # self.mraa_mock.getVersion = mock_get_version
        self.module_patcher = patch.dict('sys.modules', modules)
        self.module_patcher.start()
        self.pin_default = {'dir': 1, 'edge': 1, 'state': True}
        from micromez import inputs

        self.module_under_test = inputs

    def tearDown(self):
        self.module_patcher.stop()

    def test_button_a(self):
        self.mraa_mock.Gpio.pins = {}
        btn = self.module_under_test.Button('a')
        self.assertDictEqual(self.mraa_mock.Gpio.pins,
                             {'33': self.pin_default})

    def test_button_b(self):
        self.mraa_mock.Gpio.pins = {}
        btn = self.module_under_test.Button('b')
        self.assertDictEqual(self.mraa_mock.Gpio.pins,
                             {'31': self.pin_default})

    def test_button_c(self):
        self.mraa_mock.Gpio.pins = {}
        btn = self.module_under_test.Button('c')
        self.assertDictEqual(self.mraa_mock.Gpio.pins,
                             {'29': self.pin_default})

    def test_button_d(self):
        self.mraa_mock.Gpio.pins = {}
        btn = self.module_under_test.Button('d')
        self.assertDictEqual(self.mraa_mock.Gpio.pins,
                             {'27': self.pin_default})

    def test_button_read(self):
        self.mraa_mock.Gpio.pins = {}
        btn = self.module_under_test.Button('d')
        self.assertFalse(btn.is_pressed)
        self.mraa_mock.Gpio.pins['27']['state'] = False
        self.assertTrue(btn.is_pressed)

    def test_LP3990_off(self):
        self.mraa_mock.Gpio.pins = {}
        regulator = self.module_under_test.Lp3990()
        self.assertTrue(regulator.powered)

    def test_LP3990_on(self):
        self.mraa_mock.Gpio.pins = {}
        regulator = self.module_under_test.Lp3990()
        regulator.powered = False
        self.assertFalse(regulator.powered)

    def test_si7034_temperature(self):
        sensor = self.module_under_test.Si7034()
        self.assertEqual(sensor.temperature, 30.25)

    def test_si7034_humidity(self):
        sensor = self.module_under_test.Si7034()
        self.assertEqual(sensor.humidity, 44.53)

    def test_si7034_heater0(self):
        sensor = self.module_under_test.Si7034()
        self.assertEqual(sensor.heater, 0)
        sensor.heater = 5
        self.assertEqual(sensor.heater, 5)

    def test_LIS2DS12_whoami(self):
        accel = self.module_under_test.LIS2DS12()
        self.assertEqual(accel.who_am_i, 0x43)

    def test_LIS2DS12_powered(self):
        accel = self.module_under_test.LIS2DS12()
        self.assertFalse(accel.powered)
        accel.powered = True
        self.assertTrue(accel.powered)
        accel.powered = False
        self.assertFalse(accel.powered)

    def test_LIS2DS12_steps(self):
        accel = self.module_under_test.LIS2DS12()
        self.assertFalse(accel.steps_enabled)
        accel.steps_enabled = True
        self.assertTrue(accel.steps_enabled)
        accel.steps_enabled = False
        self.assertFalse(accel.steps_enabled)

    def test_LIS2DS12_steps_enabled(self):
        accel = self.module_under_test.LIS2DS12()
        self.assertFalse(accel.steps_enabled)
        accel.steps_enabled = True
        self.assertTrue(accel.steps_enabled)
        accel.steps_enabled = False
        self.assertFalse(accel.steps_enabled)

    def test_LIS2DS12_steps_count(self):
        accel = self.module_under_test.LIS2DS12()
        self.assertFalse(accel.steps_enabled)
        self.assertFalse(accel.powered)
        accel.powered = False
        self.assertFalse(accel.powered)
        accel.steps_enabled = True
        self.assertTrue(accel.powered)
        self.assertEqual(accel.steps, 0)
        self.mraa_mock.I2c.devices['1']['0x1d']['0x3b'] = 0b10101010
        self.mraa_mock.I2c.devices['1']['0x1d']['0x3c'] = 0b01010101
        self.assertEqual(accel.steps, 21930)
        self.mraa_mock.I2c.devices['1']['0x1d']['0x3b'] = 0b11010101
        self.mraa_mock.I2c.devices['1']['0x1d']['0x3c'] = 0b00000000
        self.assertEqual(accel.steps, 213)

    def test_LIS2DS12_steps_reset(self):
        accel = self.module_under_test.LIS2DS12()
        accel.steps_enabled = True
        self.mraa_mock.I2c.devices['1']['0x1d']['0x3b'] = 0b11010101
        self.mraa_mock.I2c.devices['1']['0x1d']['0x3c'] = 0b00000000
        self.assertEqual(accel.steps, 213)
        accel.reset_steps()
        self.assertEqual(accel.steps, 0)

    def test_tilt_enable(self):
        accel = self.module_under_test.LIS2DS12()
        self.assertFalse(accel.tilt_enabled)
        accel.tilt_enabled = True
        self.assertTrue(accel.tilt_enabled)

    def test_tilt_change(self):
        accel = self.module_under_test.LIS2DS12()
        accel.tilt_enabled = True
        self.assertEqual(accel.tilt, 0)
        self.mraa_mock.I2c.devices['1']['0x1d']['0x39'] = 1
        self.assertEqual(accel.tilt, 1)
        self.mraa_mock.I2c.devices['1']['0x1d']['0x39'] = 2
        self.assertEqual(accel.tilt, 2)
        self.mraa_mock.I2c.devices['1']['0x1d']['0x39'] = 4
        self.assertEqual(accel.tilt, 4)
        self.mraa_mock.I2c.devices['1']['0x1d']['0x39'] = 8
        self.assertEqual(accel.tilt, 8)
        self.mraa_mock.I2c.devices['1']['0x1d']['0x39'] = 16
        self.assertEqual(accel.tilt, 16)
        self.mraa_mock.I2c.devices['1']['0x1d']['0x39'] = 32
        self.assertEqual(accel.tilt, 32)

    def test_temperature(self):
        accel = self.module_under_test.LIS2DS12()
        self.assertEqual(accel.temperature, 25)
        accel.powered = True
        self.assertEqual(accel.temperature, 29)
        self.mraa_mock.I2c.devices['1']['0x1d']['0x26'] = 0xfc
        self.assertEqual(accel.temperature, 21)

    def test_LIS2DS12_x(self):
        accel = self.module_under_test.LIS2DS12()
        self.assertEqual(accel.x, 0)
        self.mraa_mock.I2c.devices['1']['0x1d']['0x28'] = 0b11010101
        self.mraa_mock.I2c.devices['1']['0x1d']['0x29'] = 0b00000000
        self.assertEqual(accel.x, 0)
        accel.powered = True
        self.assertEqual(accel.x, 213)
        self.mraa_mock.I2c.devices['1']['0x1d']['0x28'] = 0b00000000
        self.mraa_mock.I2c.devices['1']['0x1d']['0x29'] = 0b11010101
        self.assertEqual(accel.x, -11008)

    def test_LIS2DS12_y(self):
        accel = self.module_under_test.LIS2DS12()
        self.assertEqual(accel.y, 0)
        self.mraa_mock.I2c.devices['1']['0x1d']['0x2a'] = 0b11010101
        self.mraa_mock.I2c.devices['1']['0x1d']['0x2b'] = 0b00000000
        self.assertEqual(accel.y, 0)
        accel.powered = True
        self.assertEqual(accel.y, 213)
        self.mraa_mock.I2c.devices['1']['0x1d']['0x2a'] = 0b00000000
        self.mraa_mock.I2c.devices['1']['0x1d']['0x2b'] = 0b11010101
        self.assertEqual(accel.y, -11008)

    def test_LIS2DS12_z(self):
        accel = self.module_under_test.LIS2DS12()
        self.assertEqual(accel.z, 0)
        self.mraa_mock.I2c.devices['1']['0x1d']['0x2c'] = 0b11010101
        self.mraa_mock.I2c.devices['1']['0x1d']['0x2d'] = 0b00000000
        self.assertEqual(accel.z, 0)
        accel.powered = True
        self.assertEqual(accel.z, 213)
        self.mraa_mock.I2c.devices['1']['0x1d']['0x2c'] = 0b00000000
        self.mraa_mock.I2c.devices['1']['0x1d']['0x2d'] = 0b11010101
        self.assertEqual(accel.z, -11008)

    def test_LIS2DS12_xyz(self):
        accel = self.module_under_test.LIS2DS12()
        accel.powered = True
        self.assertListEqual(accel.value, [0, 0, 0])
        self.mraa_mock.I2c.devices['1']['0x1d']['0x28'] = 0b00000100
        self.mraa_mock.I2c.devices['1']['0x1d']['0x29'] = 0b01010101
        self.mraa_mock.I2c.devices['1']['0x1d']['0x2a'] = 0b01010101
        self.mraa_mock.I2c.devices['1']['0x1d']['0x2b'] = 0b00110000
        self.mraa_mock.I2c.devices['1']['0x1d']['0x2c'] = 0b01010101
        self.mraa_mock.I2c.devices['1']['0x1d']['0x2d'] = 0b00000011
        self.assertListEqual(accel.value, [21764, 12373, 853])


if __name__ == '__main__':
    unittest.main()
