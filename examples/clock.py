from time import sleep
from datetime import datetime

from micromez import inputs
from micromez import outputs

from micromez.fonts import square_font


def display_time(pixels, oled, lrg_font):
    time_now = datetime.now().time()
    time_str = '{0:02d}:{1:02d}'.format(time_now.hour, time_now.minute)
    pixels.all_off()
    pixels.draw_text(lrg_font, time_str, 30, 50)
    oled.display(pixels.memory_map)


def display_Si7034(sensor, pixels, oled, med_font, lrg_font):
    show_temperature(sensor.temperature, pixels, oled, med_font, lrg_font)


def display_LIS2DS12(accel, pixels, oled, med_font, lrg_font):
    show_temperature(accel.temperature, pixels, oled, med_font, lrg_font)


def show_temperature(temperature, pixels, oled, med_font, lrg_font):
    tmp_str = '{0:.2f}'.format(temperature)
    celsius = '{0}C'.format(chr(176))
    pixels.all_off()
    pixels.draw_text(med_font, 'Room', 20, 20)
    pixels.draw_text(med_font, 'Temp:', 70, 20)
    pixels.draw_text(lrg_font, tmp_str, 10, 60)
    pixels.draw_text(lrg_font, celsius, 95, 60)
    oled.display(pixels.memory_map)


def clock():
    regulator = inputs.Lp3990()

    if not regulator.powered:
        regulator.powered = True

    oled = outputs.OLED96()
    pixels = outputs.Grid()
    pixels.all_off()
    lrg_font = square_font.size32
    med_font = square_font.size16

    sensor = inputs.Si7034()
    accel = inputs.LIS2DS12()
    accel.powered = True

    btn_a = inputs.Button('a')
    btn_b = inputs.Button('b')
    btn_c = inputs.Button('c')
    btn_d = inputs.Button('d')

    show_item = 0
    inverted = False

    while True:
        if btn_a.is_pressed:
            print('Clock')
            show_item = 0
        if btn_b.is_pressed:
            if inverted:
                print('Normal display')
                oled.normal()
                inverted = False
            else:
                print('Invert display')
                oled.invert()
                inverted = True
            sleep(0.5)
        if btn_c.is_pressed:
            print('Si7034 Temperature')
            show_item = 1
        if btn_d.is_pressed:
            print('LIS2DS12 Temperature')
            show_item = 2

        if show_item == 0:
            display_time(pixels, oled, lrg_font)
        elif show_item == 1:
            display_Si7034(sensor, pixels, oled, med_font, lrg_font)
        elif show_item == 2:
            display_LIS2DS12(accel, pixels, oled, med_font, lrg_font)
        sleep(0.5)


if __name__ == '__main__':
    clock()
