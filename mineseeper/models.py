from collections import OrderedDict
from dataclasses import dataclass, field
import itertools
from typing import Dict, Tuple, Union


@dataclass(eq=False)
class Cell:
    is_mine: bool = False
    is_open: bool = False
    is_flag: bool = False
    mines_around: int = 0


@dataclass(frozen=True, unsafe_hash=True, order=True)
class Point:
    x: int
    y: int


@dataclass
class Board:
    width: int
    height: int
    cells: Dict[Point, Cell] = field(default=None, init=False)

    def __post_init__(self):
        self.cells = OrderedDict(
            (Point(x, y), Cell(),)
            for y, x
            in itertools.product(range(self.height), range(self.width))
        )

    def __getitem__(self, i: Union[Point, Tuple[int, int]]) -> Cell:
        if isinstance(i, Point):
            p = i
        elif isinstance(i, Tuple):
            p = Point(*i)
        else:
            raise IndexError()
        return self.cells[p]

    def around(self, p: Point) -> Dict[Point, Cell]:
        xs = [x for x in [p.x - 1, p.x, p.x + 1] if 0 <= x < self.width]
        ys = [y for y in [p.y - 1, p.y, p.y + 1] if 0 <= y < self.height]
        return {
            Point(x, y): self.cells[Point(x, y)]
            for (y, x)
            in itertools.product(ys, xs)
            if not (x == p.x and y == p.y)
        }

    def dump(self, all_open: bool = False):

        def dump_cell(cell: Cell):
            return '*' if cell.is_mine else str(cell.mines_around)

        for y in range(self.height):
            row = '  '.join(dump_cell(self[(x, y,)]) for x in range(self.width))
            print(row)
