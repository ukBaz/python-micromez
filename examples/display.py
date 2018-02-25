from time import sleep

from micromez.fonts import computer_font
from micromez.fonts import hand_font
from micromez.fonts import square_font

from micromez import outputs
from micromez import inputs

regulator = inputs.Lp3990()
regulator.powered = True

oled = outputs.OLED96()
pixels = outputs.Grid()

for x in range(10):
    oled.invert()
    sleep(0.5)
    oled.normal()
    sleep(0.5)

# oled.update(sensors.OLED96.TEST_DATA)
oled.clear()
oled.fill()
oled.clear()


def draw_stuff(font_size):
    pixels.draw_square(0, 0, 24, 24)
    oled.display(pixels.memory_map)
    pixels.draw_square(77, 38, 24, 24)
    oled.display(pixels.memory_map)
    start_loc = 2
    pixels.draw_character(font_size, 'A', start_loc, 2)
    pixels.draw_character(font_size, 'n', start_loc, 8)
    pixels.draw_character(font_size, 'd', start_loc, 2)
    pixels.draw_character(font_size, 'r', start_loc, 8)
    pixels.draw_character(font_size, 'e', start_loc, 8)
    pixels.draw_character(font_size, 'a', start_loc, 8)
    oled.display(pixels.memory_map)

    pixels.all_off()
    row1 = 34
    row2 = 62
    start_loc = 2
    start_loc += pixels.draw_character(font_size, 'H', start_loc, row1)
    start_loc += pixels.draw_character(font_size, 'e', start_loc, row1)
    start_loc += pixels.draw_character(font_size, 'l', start_loc, row1)
    start_loc += pixels.draw_character(font_size, 'l', start_loc, row1)
    start_loc += pixels.draw_character(font_size, 'o', start_loc, row1)

    start_loc = 2
    start_loc += pixels.draw_character(font_size, 'w', start_loc, row2)
    start_loc += pixels.draw_character(font_size, 'o', start_loc, row2)
    start_loc += pixels.draw_character(font_size, 'r', start_loc, row2)
    start_loc += pixels.draw_character(font_size, 'l', start_loc, row2)
    start_loc += pixels.draw_character(font_size, 'd', start_loc, row2)
    start_loc += pixels.draw_character(font_size, '!', start_loc, row2)
    oled.display(pixels.memory_map)

    pixels.all_off()
    pixels.draw_text(font_size, 'ukBaz!', 20, 50)
    oled.display(pixels.memory_map)

    pixels.all_off()
    pixels.draw_text(font_size, '96 Boards', 0, 50)
    oled.display(pixels.memory_map)

    pixels.all_off()
    pixels.draw_text(font_size, 'OLED wins!', 0, 50)
    oled.display(pixels.memory_map)
    sleep(1)
    pixels.all_off()


if __name__ == '__main__':
    for x in range(5):
        draw_stuff(hand_font.size8)
        draw_stuff(hand_font.size16)
        draw_stuff(hand_font.size32)
        draw_stuff(computer_font.size8)
        draw_stuff(computer_font.size16)
        draw_stuff(computer_font.size32)
        draw_stuff(square_font.size8)
        draw_stuff(square_font.size16)
        draw_stuff(square_font.size32)
