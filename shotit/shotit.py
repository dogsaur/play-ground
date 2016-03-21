from enum import Enum
import threading

class Getch:
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt
        import colorama
        colorama.init()

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

def locate(content, x = 0, y = 0):
    x = int(x)
    y = int(y)
    if x >= 255:
        x = 255
    if y >= 255:
        y = 255
    if x <= 0:
        x = 0
    if y <= 0:
        y = 0
    HORIZ = str(x)
    VERT = str(y)
    print("\033["+VERT+";"+HORIZ+"f"+content)

class Direction(Enum):
    up = 0
    right = 1
    down = 2
    left = 3

class Spirit:
    x = 0
    y = 0
    dx = {Direction.up : 0,
          Direction.right : 1,
          Direction.down : 0,
          Direction.left : -1}

    dy = {Direction.up : -1,
          Direction.right : 0,
          Direction.down : 1,
          Direction.left : 0}
    
    shape = [[]]
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.draw(self.x, self.y)
    
    def clear(self, x, y):
        for row_idx in range(len(self.shape)):
            row = self.shape[row_idx]
            for col_idx in range(len(row)):
                locate(' ', x + col_idx, y + row_idx)

    def draw(self, x, y):
        for row_idx in range(len(self.shape)):
            row = self.shape[row_idx]
            for col_idx in range(len(row)):
                locate(row[col_idx], x + col_idx, y + row_idx)

    def move(self, direct):
        self.clear(self.x, self.y)
        self.x += Spirit.dx[direct]
        self.y += Spirit.dy[direct]
        self.draw(self.x, self.y)

class TimerSpirit(Spirit):
    alive = True
    interval = 1
    def __init__(self, x, y, shape, interval):
        super(TimerSpirit, self).__init__(x, y, shape)
        self.interval = interval
        threading.Timer(interval, self.call).start()
    
    def __del__(self):
        self.alive = False
        self.clear(self.x, self.y)

    def call(self):
        if self.x == 0 or self.y == 0:
            self.__del__()
        self.move(Direction.up)
        if self.alive :
            threading.Timer(self.interval, self.call).start()
     
getch = Getch()

img = [
        [' ', ' ', ' ', '|', ' ', ' ', ' '],
        [' ', ' ', '|', '|', '|', ' ', ' '],
        ['+', '/', '[', ' ', ']', '\\', '+'],
        ['/', ' ', ' ', '|', ' ', ' ', '\\'],
        [' ', ' ', ' ', '^', ' ', ' ', ' ']
       ]

getch = Getch()
aircraft = Spirit(60, 20, img)
while True:
    key = getch()
    #if key == '\033':
    #    break
    if key in {'w', 'l', b'w'}:
        aricraft.move(Direction.up)
    if key in {'d', ';', b'd'}:
        aircraft.move(Direction.right)
    if key in {'s', 'j', b's'}:
        aircraft.move(Direction.down)
    if key in {'a', 'h', b'a'}:
        aircraft.move(Direction.left)
    if key == ' ':
        TimerSpirit(aircraft.x + 5, aircraft.y, [['*']], 0.2)

