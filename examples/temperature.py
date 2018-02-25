from micromez import inputs
from micromez import outputs
from time import sleep

sensor = inputs.Si7034()

sensor.heater = 5

for x in range(10):

    print('Temperature is: {0:.2f}'.format(sensor.temperature))
    print('Humidity is: {0:.2f}'.format(sensor.humidity))
    sleep(1)

sensor.heater = 0
