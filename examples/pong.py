from time import sleep
import signal
from collections import namedtuple
import random
from micromez.fonts import computer_font
from micromez import outputs
from micromez import inputs

regulator = inputs.Lp3990()
regulator.powered = True

oled = outputs.OLED96()

pixels = outputs.Grid()


class Player:
    SCREEN = [63, 127]
    SIZE = [4, 12]
    START = 28
    FONT = computer_font.size32
    SCORE_Y = 20

    def __init__(self, x_loc, score_loc):
        self.prev_pos = [x_loc, Player.START]
        self.curr_pos = [x_loc, Player.START]
        self.move_incr = 4
        self._move()

        self._score = 0
        self.score_loc = score_loc
        self.score = 0

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, new_score):
        pixels.draw_character(Player.FONT, str(self.score),
                              self.score_loc, Player.SCORE_Y, True)

        self._score = new_score

        pixels.draw_character(Player.FONT, str(self.score),
                              self.score_loc, Player.SCORE_Y)
        oled.display(pixels.memory_map)

    def move_up(self, *args):
        self._move(-self.move_incr)

    def move_down(self, *args):
        self._move(self.move_incr)

    def _move(self, move_by=4):
        self.prev_pos = self.curr_pos
        pixels.draw_square(self.prev_pos[0], self.prev_pos[1],
                           Player.SIZE[0], Player.SIZE[1],
                           False)
        self.curr_pos[1] = self.prev_pos[1] + move_by
        self._end_travel()
        pixels.draw_square(self.curr_pos[0], self.curr_pos[1],
                           Player.SIZE[0], Player.SIZE[1])
        # oled.display(pixels.memory_map)

    def _end_travel(self):
        if self.curr_pos[1] < 0:
            self.curr_pos[1] = 0
        elif self.curr_pos[1] > (63 - Player.SIZE[1]):
            self.curr_pos[1] = (63 - Player.SIZE[1])


class Puck:
    DIR = [-3, -2, -1, 1, 2, 3]
    SIZE = [2, 2]
    START = [64, 32]

    def __init__(self):
        self.prev_pos = Puck.START
        self.curr_pos = Puck.START
        self.move_incr = [2, 2]
        self.move()

    def _cursor(self, player):
        continue_game = True
        miss_high = self.curr_pos[1] > player.curr_pos[1] + Player.SIZE[1]
        miss_low = self.curr_pos[1] < player.curr_pos[1]
        if miss_high or miss_low:
            if player is p1:
                p1.score = p1.score
                p2.score = p2.score + 1
                if p2.score > 8:
                    continue_game = False
                self._new_point()

            else:
                p1.score = p1.score + 1
                p2.score = p2.score
                if p1.score > 8:
                    continue_game = False
                self._new_point()
        return continue_game

    def _new_point(self):
        pixels.draw_square(self.prev_pos[0], self.prev_pos[1],
                           Puck.SIZE[0], Puck.SIZE[1], False)
        self.prev_pos = Puck.START
        self.curr_pos = Puck.START
        self.move_incr = [random.choice(Puck.DIR), random.choice(Puck.DIR)]
        draw_court()

    def _collision(self):
        continue_game = True
        if self.curr_pos[0] < 4:
            continue_game = self._cursor(p1)
            self.move_incr[0] = abs(self.move_incr[0])
        elif self.curr_pos[0] > 123:
            continue_game = self._cursor(p2)
            self.move_incr[0] = -self.move_incr[0]
        if self.curr_pos[1] < 0:
            self.move_incr[1] = abs(self.move_incr[1])
        elif self.curr_pos[1] > 60:
            self.move_incr[1] = -self.move_incr[1]
        self.curr_pos = [sum(x) for x in zip(self.prev_pos, self.move_incr)]
        # print('Current pos: ', self.curr_pos)
        return continue_game

    def move(self):
        self.prev_pos = self.curr_pos
        self.curr_pos = [sum(x) for x in zip(self.prev_pos, self.move_incr)]
        continue_game = self._collision()
        pixels.draw_square(self.prev_pos[0], self.prev_pos[1],
                           Puck.SIZE[0], Puck.SIZE[1], False)
        pixels.draw_square(self.curr_pos[0], self.curr_pos[1],
                           Puck.SIZE[0], Puck.SIZE[1])

        oled.display(pixels.memory_map)

        return continue_game


def p1_move_down(*args):
    p1.move_down()


def p1_move_up(*args):
    p1.move_up()


def p2_move_down(*args):
    p2.move_down()


def p2_move_up(*args):
    p2.move_up()


def draw_court():
    pixels.draw_square(64, 0, 2, 63)


if __name__ == '__main__':
    active = True
    p1 = Player(0, 32)
    p2 = Player(124, 96)
    puck = Puck()
    draw_court()
    oled.display(pixels.memory_map)

    p1_up = inputs.Button('b')
    p1_down = inputs.Button('a')
    p1_up.when_pressed = p1_move_up
    p1_down.when_pressed = p1_move_down

    p2_up = inputs.Button('c')
    p2_down = inputs.Button('d')
    p2_up.when_pressed = p2_move_up
    p2_down.when_pressed = p2_move_down

    # signal.signal(signal.SIGALRM, puck.move())
    # signal.alarm(0.05)

    while active:
        active = puck.move()

    draw_court()
    pixels.draw_text(Player.FONT, 'Game', 10, 50)
    pixels.draw_text(Player.FONT, 'Over', 70, 50)
    oled.display(pixels.memory_map)

    sleep(10)
