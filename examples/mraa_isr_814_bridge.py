from signal import pause
from random import randint
import mraa

print(mraa.getVersion())
print(mraa.getPlatformName())


def bridge_func(*args):
    print(args)
    # person.caller(bingo.new_number)


class BingoCaller:
    def __init__(self):
        self.numbers_called = []
        print('Setup some fancy GUI')

    def caller(self, machine_obj):
        self.numbers_called.append(machine_obj.new_number)
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

    def on_button_press(self, fn, machine, person):
        self._int1.isr(mraa.EDGE_FALLING, fn, person)


dave = BingoCaller()
machine = BingoMachine()

machine.on_button_press(bridge_func, machine, dave)

pause()
