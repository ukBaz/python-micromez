from time import sleep
import signal
from micromez.fonts import computer_font
from micromez import outputs
from micromez import inputs


def draw_update():
    print(accel.get_orientation())


def draw_test():
    pixels.all_off()
    pixels.draw_text(computer_font.size16, str(accel.read_steps()), 20, 20)
    oled.display(pixels.memory_map)


if __name__ == '__main__':
    regulator = inputs.Lp3990()
    regulator.powered = True

    accel = inputs.LIS2DS12()
    accel.powered = True
    accel.step_enabled = True

    oled = outputs.OLED96()

    pixels = outputs.Grid()

    draw_test()
    scr_change2 = inputs.Button('INT2')

    scr_change2.when_pressed = draw_test

    while True:
        print('While: ', accel.steps, scr_change2.is_pressed)
        print('{:08b}'.format(accel.device.readReg(0x3d)))

        sleep(2)

    signal.pause()
