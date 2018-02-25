from micromez.inputs import *
from time import sleep


def main():
    settings = 0b0000
    btn_a = Button('A')
    btn_b = Button('b')
    btn_c = Button('c')
    btn_d = Button('d')

    while not settings == 0b1111:
        if btn_a.is_pressed:
            print('Button A pressed')
            settings = settings | 0b1000
            sleep(0.25)
        elif btn_b.is_pressed:
            print('Button B pressed')
            settings = settings | 0b0100
            sleep(0.25)
        elif btn_c.is_pressed:
            print('Button C pressed')
            settings = settings | 0b0010
            sleep(0.25)
        elif btn_d.is_pressed:
            print('Button D pressed')
            settings = settings | 0b0001
            sleep(0.25)


if __name__ == '__main__':
    main()
