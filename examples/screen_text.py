from time import sleep
from micromez.fonts import hand_font
from micromez.fonts import computer_font
from micromez.fonts import square_font

from micromez import outputs
from micromez import inputs

regulator = inputs.Lp3990()
regulator.powered = True

oled = outputs.OLED96()
pixels = outputs.Grid()

font_size = square_font.size16
pixels.draw_text(font_size, '96 Boards', 0, 20)

font_size = hand_font.size16
pixels.draw_text(font_size, '96 Boards', 0, 40)

font_size = computer_font.size16
pixels.draw_text(font_size, '96 Boards', 0, 60)

font_size = square_font.size8
pixels.draw_text(font_size, '96 Boards', 70, 10)

font_size = square_font.size16
pixels.draw_text(font_size, '96 Boards', 70, 30)

font_size = square_font.size32
pixels.draw_text(font_size, '96 Boards', 70, 60)
oled.display(pixels.memory_map)

sleep(10)
