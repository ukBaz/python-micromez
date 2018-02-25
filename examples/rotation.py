from time import sleep
from micromez import inputs


def rotation():
    # Setup accelerometer
    accel = inputs.LIS2DS12()
    accel.powered = True
    accel.tilt_enabled = True

    for x in range(60):
        print(accel.tilt)
        sleep(0.5)


if __name__ == '__main__':
    rotation()
