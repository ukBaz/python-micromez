from freetype import *

def bits(x):
    data = []
    for i in range(8):
        data.insert(0, int((x & 1) == 1))
        x = x >> 1
    return data


def print_grid(data):
    for row in zip(*data):
        str_row = ''.join(str(q) for q in row)
        str_row = str_row.replace('1', '*')
        str_row = str_row.replace('0', ' ')
        print(str_row)

if __name__ == '__main__':
    # import numpy
    # import matplotlib.pyplot as plt

    face = Face('./Vera.ttf')
    face.set_char_size( 48*64 )
    face.load_char('H', FT_LOAD_RENDER |
                        FT_LOAD_TARGET_MONO )

    bitmap = face.glyph.bitmap
    width  = face.glyph.bitmap.width
    rows   = face.glyph.bitmap.rows
    pitch  = face.glyph.bitmap.pitch

    data = []
    for i in range(bitmap.rows):
        row = []
        for j in range(bitmap.pitch):
            row.extend(bits(bitmap.buffer[i*bitmap.pitch+j]))
        data.extend(row[:bitmap.width])
    # Z = numpy.array(data).reshape(bitmap.rows, bitmap.width)
    # plt.imshow(Z, interpolation='nearest', cmap=plt.cm.gray, origin='lower')
    # plt.show()
    print(len(data))
    print(width)
    my_char = []
    my_row = []
    for my_bit in data:
        if len(my_row) > pitch:
            my_char.append(my_row)
            print(my_row)
            my_row = []
        else:
            my_row.append(my_bit)

    # print(data[my_index:my_index + 48])

    # print_grid(data)
