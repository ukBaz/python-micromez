from signal import pause
from random import randint
import mraa

print(mraa.getVersion())
print(mraa.getPlatformName())


def caller(machine_obj):
    print(machine_obj.new_number)


class BingoMachine:
    def __init__(self, data_rdy_pin=33):
        # Pin for interrupt signal
        self._int1 = mraa.Gpio(data_rdy_pin)
        self._int1.dir(mraa.DIR_IN)
        self._int1.edge(mraa.EDGE_FALLING)

    @property
    def int1(self):
        return not self._int1.read()

    @property
    def new_number(self):
        return randint(0, 90)

    def on_button_press(self, fn, *args):
        self._int1.isr(mraa.EDGE_FALLING, fn, args[0])


machine = BingoMachine()

machine.on_button_press(caller, machine)

pause()
