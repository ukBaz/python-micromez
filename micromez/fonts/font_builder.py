import argparse
from collections import namedtuple
from freetype import *

mono = True

font_family = {}
Character = namedtuple('Character', ['rows',
                                     'width',
                                     'pitch',
                                     'top',
                                     'left',
                                     'pixmap'])


def print_gray(data, rows, width, pitch, top, left):
    for y in range(rows):
        line = []
        for x in range(width):
            pointer = y * width + x
            line.append('{0:0>3}'.format(data[pointer]))
        print(line)


def print_mono(symbol, character):

    for row in range(character.rows):
        if row == 0 and row == character.rows - 1:
            print()
        elif row == 0:
            print('"{}": [{},'.format(symbol,
                                      [pix.replace('0', '.').replace('1', '#')
                                       for pix in character.pixmap[row]]))
        elif row == character.rows - 1:
            print('{}]'.format([pix.replace('0', '.').replace('1', '#')
                                for pix in character.pixmap[row]]))
        else:
            print('{},'.format([pix.replace('0', '.').replace('1', '#')
                                for pix in character.pixmap[row]]))
    print(',')


def write_font_file(out_file, size, append):
    if append:
        write_type = 'a'
    else:
        write_type = 'w'

    with open(out_file, '{}'.format(write_type)) as font_file:
        font_file.write('size{} = {{\n'.format(size))
        for font in font_family:
            t = font_family[font]
            font_file.write('"{}": [{}, {}, {}, {}, {}, [\n'.format(font,
                                                                    t.rows,
                                                                    t.width,
                                                                    t.pitch,
                                                                    t.top,
                                                                    t.left))
            for row in range(t.rows):
                font_file.write('{},\n'.format(t.pixmap[row]))
            font_file.write(']],\n')
        font_file.write('}\n')


def mono_pixmap(character, data, rows, width, pitch, top, left):
    bit_data = ''
    pixmap = []
    for i in data:
        # bit_data += '{0:08b}'.format(i)[::-1]
        bit_data += '{0:08b}'.format(i)
    # print(len(bit_data))
    for y in range(rows):
        line = []
        for x in range(pitch * 8):
            pointer = y * (pitch * 8) + x
            # print(y, pitch * 8, x, y * (pitch * 8) + x)
            line.append('{}'.format(bit_data[pointer]))
        trim_line = line[:width]
        pixmap.append(trim_line)

    font_family[character] = Character(rows, width, pitch, top, left, pixmap)


def get_available_chars(font_file):
    face = Face(font_file)
    charcode, agindex = face.get_first_char()
    while agindex != 0:
        # print(chr(charcode), agindex)
        yield charcode
        charcode, agindex = face.get_next_char(charcode, agindex)


def make_bitmap(font_file, character, height=16, monochrome=True):
    face = Face(font_file)
    # face.set_char_size(32 * 64)
    face.set_pixel_sizes(0, height)
    if mono:
        face.load_char(chr(character), FT_LOAD_RENDER | FT_LOAD_TARGET_MONO)
    else:
        face.load_glyph(face.get_char_index(character))
    slot = face.glyph
    top = slot.bitmap_top
    left = slot.bitmap_left
    bitmap = slot.bitmap
    data, rows, width, pitch = (bitmap.buffer,
                                bitmap.rows,
                                bitmap.width,
                                bitmap.pitch)
    # print(rows, width, pitch, data)
    # print(rows, width, pitch, top, left)

    if mono:
        mono_pixmap(character, data, rows, width, pitch, top, left)
    else:
        print_gray(data, rows, width, pitch, top, left)


"""
python3 font_builder.py VT323-Regular.ttf  computer_font.py 8 16 32
python3 font_builder.py NovaSquare.ttf square_font.py 8 16 32
python3 font_builder.py GloriaHallelujah.ttf hand_font.py 8 16 32

Then to retrieve:
import computer_font
computer_font.size16[str(ord('x'))]

Maybe make it a function?
"""


def build_font_file(ttf_file, output_file, sizes):
    append = False
    for size in sizes:
        print(size, sizes)
        for character in get_available_chars(ttf_file):
            make_bitmap(ttf_file, character, size)

        # for symbol in font_family:
        #     print_mono(symbol, font_family[symbol])

        write_font_file(output_file, size, append)
        append = True


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('font_file')
    parser.add_argument('bitmap_file')
    parser.add_argument('heights',
                        help="Target heights for font",
                        type=int,
                        nargs='+')

    args = parser.parse_args()
    # get_available_chars(args.font_file)
    build_font_file(args.font_file,
                    args.bitmap_file,
                    args.heights)
