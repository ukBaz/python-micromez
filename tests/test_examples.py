import unittest
from unittest.mock import patch
import _thread
from time import sleep
from tests import mock_mraa


class TestExamples(unittest.TestCase):

    def setUp(self):
        # self.mraa_mock = MagicMock()
        self.mraa_mock = mock_mraa.mraa()
        modules = {
            'mraa': self.mraa_mock,
        }
        # self.mraa_mock.getVersion = mock_get_version
        self.module_patcher = patch.dict('sys.modules', modules)
        self.module_patcher.start()
        from examples import buttons

        self.module_under_test = buttons

    def tearDown(self):
        self.module_patcher.stop()

    def test_instantiation(self):
        def button_toggle():
            self.mraa_mock.Gpio.pins['33']['state'] = False
            sleep(0.2)
            self.mraa_mock.Gpio.pins['33']['state'] = True
            self.mraa_mock.Gpio.pins['31']['state'] = False
            sleep(0.2)
            self.mraa_mock.Gpio.pins['31']['state'] = True
            self.mraa_mock.Gpio.pins['29']['state'] = False
            sleep(0.2)
            self.mraa_mock.Gpio.pins['29']['state'] = True
            self.mraa_mock.Gpio.pins['27']['state'] = False
            sleep(0.2)
            self.mraa_mock.Gpio.pins['27']['state'] = False
            sleep(0.2)

        _thread.start_new_thread(button_toggle, ())
        self.module_under_test.main()


if __name__ == '__main__':
    unittest.main()
