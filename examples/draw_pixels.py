from time import sleep
from random import randint

from micromez import outputs
from micromez import inputs

regulator = inputs.Lp3990()
regulator.powered = True

image = [['0', '0', '0', '0', '0'],
         ['0', '1', '0', '1', '0'],
         ['0', '0', '0', '0', '0'],
         ['1', '0', '0', '0', '1'],
         ['0', '1', '1', '1', '0']]

oled = outputs.OLED96()
pixels = outputs.Grid()
pixels.all_off()

for i in range(20):
    x = randint(0, 128)
    y = randint(0, 64)
    pixels.set_pixel(x, y)
    oled.display(pixels.memory_map)
    sleep(0.1)

pixels.all_off()
for x, y in zip(range(0, 128, 2), range(0, 64)):
    pixels.draw_pixmap(image, x, y)
    oled.display(pixels.memory_map)
    pixels.draw_pixmap(image, x, y, True)
