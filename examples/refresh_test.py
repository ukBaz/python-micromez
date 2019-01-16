from time import sleep

from micromez import outputs
from micromez import inputs

regulator = inputs.Lp3990()
regulator.powered = True

oled = outputs.OLED96()
pixels = outputs.Grid()

for x in range(10):
    print('Screen load {}'.format(x))
    oled.clear()
    sleep(0.5)
    oled.fill()
    sleep(0.5)
    oled.clear()