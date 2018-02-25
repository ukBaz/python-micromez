import mraa
import math


class OLED96:
    """
    0.96" OLED screen with SSD1306 controller
    """
    OLED_HEIGHT = 64
    OLED_WIDTH = 128

    DISPLAY_SLEEP = 0xAE
    DISPLAY_WAKEUP = 0xAF
    DISPLAY_OFF = 0xAE
    OSC_FREQ = 0xD5
    MULTIPLEX_RATIO = 0xA8
    DISPLAY_OFFSET = 0xD3
    DISPLAY_START_LINE = 0x40
    CHRG_PUMP_SETTING = 0x8D
    CHRG_PUMP_ENABLE = 0x14
    COL127_SEG0 = 0xA1
    COM_SCAN_DOWN = 0xC8
    COM_PINS_CONF = 0xDA
    MEMORY_ADDR_MODE = 0x20
    HORZ_ADDR_MODE = 0x00
    B0_CONTRAST = 0x81
    PRE_CHARGE_PERIOD = 0xD9
    REGULATOR_OUTPUT = 0xDB
    DISPLAY_ON = 0xA5
    DISPLAY_RESUME = 0xA4
    NORMAL_DISPLAY_MODE = 0xA6
    INVERSE_DISPLAY_MODE = 0xA7
    COLUMN_ADDR = 0x21
    PAGE_ADDR = 0x22
    SEND_DATA = 0x40
    SEND_CMD = 0x00

    def __init__(self, bus=0, i2c_addr=0x3c):
        self.device = mraa.I2c(bus)
        self.device.address(i2c_addr)
        self._memory_pages = []
        self._fill_memory()
        self._initialization()

    def __enter__(self):
        return self

    def __del__(self):
        self.clean_up()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clean_up()

    def _send_command(self, *commands):
        for cmd in commands:
            # print('self.device.writeReg(0x00, 0x{:02x})'.format(cmd))
            self.device.writeReg(OLED96.SEND_CMD, cmd)

    def _send_data(self, data):
        for page in data:
            # control = 0x40  # Co = 0, DC = 0
            self.device.writeReg(OLED96.SEND_DATA, page)

    def _send_data32(self, data):
        chunk_size = 32
        for i in range(0, len(data), chunk_size):
            frame = [OLED96.SEND_DATA] + data[i:i + chunk_size]
            self.device.write(bytearray(frame))

    def _fill_memory(self, status=False):
        if status:
            content = 0xFF
        else:
            content = 0x00
        pages = (OLED96.OLED_HEIGHT // 8) * OLED96.OLED_WIDTH
        self._memory_pages = [content] * pages

    def _initialization(self):
        self._send_command(OLED96.DISPLAY_SLEEP)
        self._send_command(OLED96.OSC_FREQ, 0x80)
        self._send_command(OLED96.MULTIPLEX_RATIO, 0x3F)
        self._send_command(OLED96.DISPLAY_OFFSET, 0X00)
        self._send_command(OLED96.DISPLAY_START_LINE)
        self._send_command(OLED96.CHRG_PUMP_SETTING, OLED96.CHRG_PUMP_ENABLE)
        self._send_command(OLED96.COL127_SEG0)
        self._send_command(OLED96.COM_SCAN_DOWN)
        self._send_command(OLED96.COM_PINS_CONF, 0x12)
        self._send_command(OLED96.MEMORY_ADDR_MODE, OLED96.HORZ_ADDR_MODE)
        self._send_command(OLED96.B0_CONTRAST, 0xCF)
        self._send_command(OLED96.PRE_CHARGE_PERIOD, 0xF1)
        self._send_command(OLED96.REGULATOR_OUTPUT, 0x40)
        self._send_command(OLED96.DISPLAY_RESUME)
        self._send_command(OLED96.NORMAL_DISPLAY_MODE)
        self._send_command(OLED96.DISPLAY_WAKEUP)

    def off(self):
        """
        Turn display off
        """
        self._send_command(OLED96.DISPLAY_OFF)

    def clean_up(self):
        """
        Clear display and power off
        """
        self.clear()
        self.off()

    def invert(self):
        """
        Put the display in inverted mode
        """
        self._send_command(OLED96.INVERSE_DISPLAY_MODE)

    def normal(self):
        """
        Put the display in normal mode
        """
        self._send_command(OLED96.NORMAL_DISPLAY_MODE)

    def clear(self):
        """
        Clear the display
        """
        self._fill_memory()
        self.display()

    def fill(self):
        """
        Fill the display
        """
        self._fill_memory(True)
        self.display()

    def scroll_text(self, horizontal=None, vertical=None):
        """
        Scroll current content of display
        :param horizontal:
            Set to any value to scroll horizontally
        :param vertical:
            Currently not implemented
        """
        if horizontal is not None and vertical is not None:
            self._send_command(0x29, 0x00, 0x00, 0x00, 0x07, 0x01, 0x2f)
        elif horizontal is not None and vertical is None:
            self._send_command(0x26, 0x00, 0x00, 0x00, 0x07, 0x00, 0x2f)

    def test_disp(self, loop=1024, data=0xff):
        """Display test pattern."""
        self.device.writeReg(0x00, 0x21)
        self.device.writeReg(0x00, 0)  # Column start address. (0 = reset)
        self.device.writeReg(0x00, OLED96.OLED_WIDTH - 1)  # Column end addr
        self.device.writeReg(0x00, 0x22)
        self.device.writeReg(0x00, 0)  # Page start address. (0 = reset)
        self.device.writeReg(0x00, (OLED96.OLED_HEIGHT // 8) - 1)  # Page end
        # Write buffer data
        print('Data used: ', data)
        for y in range(loop):
            # control = 0x40  # Co = 0, DC = 0
            self.device.writeWordReg(0x40, data)

    def display(self, data=None):
        """Write display buffer to physical display."""
        if data is None:
            data = self._memory_pages
        self._send_command(OLED96.COLUMN_ADDR, 0x00,
                           OLED96.OLED_WIDTH - 1)
        self._send_command(OLED96.PAGE_ADDR, 0x00,
                           (OLED96.OLED_HEIGHT // 8) - 1)
        # Write buffer data
        self._send_data32(data)


class Grid:
    """
    Class for manipulating data to be drawn to screen
    [0, 0] is top left
    """
    def __init__(self, width=128, height=64):
        self.width = width
        self.height = height
        self._display = []
        self.all_off()

    @property
    def memory_map(self):
        """
        Data in format ready to display on screen
        """
        pages = []
        for row in range(0, len(self._display), 8):
            for column in range(len(self._display[row])):
                page_value = [self._display[row + 7][column],
                              self._display[row + 6][column],
                              self._display[row + 5][column],
                              self._display[row + 4][column],
                              self._display[row + 3][column],
                              self._display[row + 2][column],
                              self._display[row + 1][column],
                              self._display[row + 0][column]]
                pages.append(int(''.join(str(e) for e in page_value), 2))

        return pages

    def draw_square(self, x_loc, y_loc, x_size, y_size, fill=True):
        """
        Create a square in the display buffer
        :param x_loc:
            The X origin of the square
        :param y_loc:
            The Y origin of the square
        :param x_size:
            The size of the square in X direction
        :param y_size:
            The size of the square in Y direction
        :param fill:
            Boolean of if pixels are on (True) or off (False)
        """
        for x in range(x_loc, x_loc + x_size):
            for y in range(y_loc, y_loc + y_size):
                try:
                    self._display[y][x] = int(fill)
                except IndexError:
                    raise ValueError

    def _set_all(self, value):
        self._display = [[value for columns in range(self.width)]
                         for rows in range(self.height)]

    def all_off(self):
        """
        Set all pixels to off
        """
        self._set_all(0)

    def all_on(self):
        """
        Set all pixels on
        """
        self._set_all(1)

    def rotate(self, matrix, degree):
        """
        Output a matrix/pixmap rotated by the specified angle

        :param matrix:
            2D array of 1's or 0's reflecting item to be drawn
        :param degree:
            Required rotation of pixmap
            Valid values: 0, 90, 180, 270, 360
        """
        if abs(degree) not in [0, 90, 180, 270, 360]:
            # raise error or just return nothing or original
            pass
        if degree == 0:
            return matrix
        elif degree > 0:
            return self.rotate(list(zip(*matrix[::-1])), degree - 90)
        else:
            return self.rotate(list(zip(*matrix))[::-1], degree + 90)

    def draw_pixmap(self, pixmap, x_loc, y_loc, clear=False):
        """
        Draw the pixmap at the specified location

        :param pixmap:
            2D array of 1's or 0's reflecting item to be drawn
        :param x_loc:
            The origin in X for the pixmap
        :param y_loc:
            The origin in Y for the pixmap
        :param clear:
            Boolean to remove drawn shape
        """
        for row in range(len(pixmap)):
            y_pix = y_loc + row
            for column in range(len(pixmap[row])):
                x_pix = x_loc + column
                if str(pixmap[row][column]) == '1' and not clear:
                    self.set_pixel(x_pix, y_pix)
                else:
                    self.clear_pixel(x_pix, y_pix)

    def draw_character(self, font, character, x_loc, y_loc, clear=False):
        """
        Draw a single character using font and location

        :param font:
            Specify micromez font file
        :param character:
            Character to display
        :param x_loc:
            location in X
        :param y_loc:
            location in Y
        :param clear:
            Boolean to remove character
        """
        # rows, width, pitch, top, left, pixmap
        font_glyph = font[str(ord(character))]
        rows = font_glyph[0]
        columns = font_glyph[1]
        pitch = font_glyph[2]
        top = font_glyph[3]
        left = font_glyph[4]
        pixmap = font_glyph[5]
        x_offset = columns - left
        y_offset = rows - top
        for row in range(rows):
            y_pix = y_loc + row - top
            for column in range(columns):
                x_pix = x_loc + column
                if pixmap[row][column] == '1' and not clear:
                    self.set_pixel(x_pix, y_pix)
                else:
                    self.clear_pixel(x_pix, y_pix)
        return columns + left

    def draw_text(self, font, text, x_loc, y_loc):
        """
        Draw a text string in the specified font and location

        :param font:
            micromez font file and size e.g. hand_font.size8
        :param text:
            Text string to display
        :param x_loc:
            origin in X
        :param y_loc:
            origin in Y

        """
        for character in text:
            x_loc += self.draw_character(font, character, x_loc, y_loc)

    def set_pixel(self, x_loc, y_loc):
        """
        Switch an individual pixel on

        :param x_loc:
            X location
        :param y_loc:
            Y location
        """
        if x_loc < self.width and y_loc < self.height:
            self._display[y_loc][x_loc] = 1

    def clear_pixel(self, x_loc, y_loc):
        """
        Switch and individual pixel off

        :param x_loc:
            X location
        :param y_loc:
            Y location
        """
        if x_loc < self.width and y_loc < self.height:
            self._display[y_loc][x_loc] = 0

    def draw_circle(self, centre_x, centre_y, radius):
        """
        Draw circle

        :param centre_x:
            Origin in X
        :param centre_y:
            Origin in Y
        :param radius:
            Radius of circle in pixels
        """
        x = radius - 1
        y = 0
        dx = 1
        dy = 1
        err = dx - (radius << 1)

        while x >= y:
            self.set_pixel(centre_x + x, centre_y + y)
            self.set_pixel(centre_x + y, centre_y + x)
            self.set_pixel(centre_x - y, centre_y + x)
            self.set_pixel(centre_x - x, centre_y + y)
            self.set_pixel(centre_x - x, centre_y - y)
            self.set_pixel(centre_x - y, centre_y - x)
            self.set_pixel(centre_x + y, centre_y - x)
            self.set_pixel(centre_x + x, centre_y - y)

            print(x, y, dx, dy,
                  (centre_x + x, centre_y + y),
                  (centre_x + y, centre_y + x),
                  (centre_x - y, centre_y + x),
                  (centre_x - x, centre_y + y),
                  (centre_x - x, centre_y - y),
                  (centre_x - y, centre_y - x),
                  (centre_x + y, centre_y - x),
                  (centre_x + x, centre_y - y),
                  err)
            self.print_grid()
            if err <= 0:
                y += 1
                err += dy
                dy += 2
            if err > 0:
                x -= 1
                dx += 2
                err += (-radius << 1) + dx

    def print_grid2(self):
        for row in zip(*self._display):
            str_row = ''.join(str(q) for q in row)
            str_row = str_row.replace('1', '*')
            str_row = str_row.replace('0', ' ')
            print(str_row)

    def print_grid(self):
        for row in self._display:
            str_row = ''.join(str(q) for q in row)
            print('{}'.format(str_row.replace('0', '.').replace('1', '#')))

    def draw_circle_2(self, x_loc, y_loc, radius):
        for angle in range(0, 360, 5):
            x = radius * math.sin(math.radians(angle)) + x_loc
            y = radius * math.cos(math.radians(angle)) + y_loc
            self._display[int(x)][int(y)] = 1

    def _bool_to_byte(self, bool_list):
        sum(v << i for i, v in enumerate(bool_list[::-1]))

    def _draw_orth_line(self, x1, y1, x2, y2, pix_value):
        if x2 - x1 == 0:
            for y in range(y1, y2):
                self._display[y][x1] = pix_value
        else:
            for x in range(x1, x2):
                self._display[y1][x] = pix_value

    def _draw_angle_line(self, x1, y1, x2, y2, pix_value):
        xd = x2 - x1
        yd = y2 - y1
        if xd < yd:
            rate = yd / xd
            y = y1
            for x in range(x1, x2 + 1):
                self._display[int(y)][x] = pix_value
                y += rate
        else:
            rate = xd / yd
            x = x1
            for y in range(y1, y2 + 1):
                self._display[y][int(x)] = pix_value
                x += rate

    def draw_line(self, x1, y1, x2, y2, clear=False):
        """
        Draw a line between to coordinates

        :param x1:
            Start location in X
        :param y1:
            Start location in Y
        :param x2:
            End location in X
        :param y2:
            end locaiton in Y
        :param clear:
            Boolean to clear specified line
        """
        pix_val = 0 if clear else 1
        xd = x2 - x1
        yd = y2 - y1
        if xd == 0 or yd == 0:
            self._draw_orth_line(x1, y1, x2, y2, pix_val)
        else:
            self._draw_angle_line(x1, y1, x2, y2, pix_val)
