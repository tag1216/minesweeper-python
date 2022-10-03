import random

from mineseeper.models import Board, Point


class Game:

    def __init__(self, width: int, height: int, mines: int):
        self.width = width
        self.height = height
        self.mines = mines
        self.board = self.create_board(width, height, mines)

    @staticmethod
    def create_board(width: int, height: int, mines: int) -> Board:

        board = Board(width, height)

        for cell in random.sample(list(board.cells.values()), k=mines):
            cell.is_mine = True

        for p, cell in board.cells.items():
            cells_around = board.around(p).values()
            mines_around = sum(1 for x in cells_around if x.is_mine)
            cell.mines_around = mines_around

        return board

    @property
    def cells(self):
        return self.board.cells

    @property
    def remaining_mines(self):
        num_flag = sum(1 for c in self.board.cells.values() if c.is_flag)
        return self.mines - num_flag

    @property
    def remaining_cells(self):
        num_open = sum(1 for c in self.board.cells.values() if c.is_open)
        num_cells = len(self.cells)
        return num_cells - num_open - self.mines

    def open(self, p: Point):

        cell = self.cells[p]

        if cell.is_open:
            return True

        cell.is_open = True
        cell.is_flag = False

        if cell.is_mine:
            return False

        if cell.mines_around == 0:
            for around_p in self.board.around(p).keys():
                self.open(around_p)

        return True

    def toggle_flag(self, p: Point):
        self.board.cells[p].is_flag = not self.board.cells[p].is_flag
