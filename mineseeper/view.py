import curses

from mineseeper.game import Game
from mineseeper.models import Point

KEY_ESC = ord('\x1b')
KEY_MOUSE = curses.KEY_MOUSE

BOARD_Y = 2
BOARD_X = 2
BOARD_SPACE = 2


class CursesView:

    def __init__(self, game: Game):
        self.game = game

    def start(self):
        curses.wrapper(self.main)

    def main(self, stdscr: curses.window):

        curses.mousemask(curses.BUTTON1_CLICKED | curses.BUTTON1_DOUBLE_CLICKED)
        stdscr.clear()

        stdscr.addstr(0, 0, '[ESC:Quit] [Click:Toggle Flag] [DoubleClick: Open]')

        while True:

            stdscr.addstr(1, 0, f'mines {self.game.remaining_mines} / {self.game.mines}')

            for y in range(self.game.height):
                for x in range(self.game.width):
                    cell = self.game.cells[Point(x, y)]
                    if cell.is_flag:
                        c = 'F'
                    elif not cell.is_open:
                        c = '_'
                    else:
                        c = str(cell.mines_around)
                    stdscr.addstr(y + BOARD_Y,
                                  x * (BOARD_SPACE + 1) + BOARD_X,
                                  c)

            k = stdscr.getch()

            if k == KEY_ESC:
                break
            if self.game.remaining_mines > 0 and k == KEY_MOUSE:
                (_, x, y, _, bstate) = curses.getmouse()
                p = self.point(x, y)

                if not (0 <= p.x < self.game.width and 0 <= p.y < self.game.height):
                    continue

                cell = self.game.cells[p]

                if cell.is_open:
                    continue

                if bstate == curses.BUTTON1_DOUBLE_CLICKED:
                    self.game.open(p)
                elif bstate == curses.BUTTON1_CLICKED:
                    self.game.toggle_flag(p)

                if self.game.remaining_mines == 0:
                    stdscr.addstr(BOARD_Y + self.game.height, 0, 'clear!')

        stdscr.refresh()

    @staticmethod
    def point(x, y):
        board_x = (x - BOARD_X) // (BOARD_SPACE + 1)
        board_y = y - BOARD_Y
        return Point(board_x, board_y)
