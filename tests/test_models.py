import unittest

from mineseeper.models import Board
from mineseeper.models import Cell
from mineseeper.models import Point


class TestPoint(unittest.TestCase):

    def test(self):

        p1 = Point(1, 2)
        p2 = Point(1, 2)
        p3 = Point(2, 1)

        self.assertFalse(p1 is p2)
        self.assertTrue(p1 == p2)
        self.assertFalse(p2 == p3)


class TestCell(unittest.TestCase):

    def test_eq(self):
        self.assertNotEqual(Cell(), Cell())


class TestBoard(unittest.TestCase):

    def test(self):

        board = Board(3, 3)

        self.assertIsNotNone(board.cells[Point(0, 0)])
        self.assertIsNotNone(board.cells[Point(2, 2)])

    def test_getitem(self):

        board = Board(2, 2)
        self.assertEqual(board[Point(1, 0)], board.cells[Point(1, 0)])
        self.assertEqual(board[Point(1, 0)], board.cells[Point(1, 0)])

    def test_around(self):

        board = Board(3, 3)

        self.assertEqual(
            list(board.around(Point(1, 1)).keys()),
            [
                Point(0, 0),
                Point(1, 0),
                Point(2, 0),
                Point(0, 1),
                Point(2, 1),
                Point(0, 2),
                Point(1, 2),
                Point(2, 2),
            ]
        )

        self.assertEqual(
            list(board.around(Point(2, 0)).keys()),
            [
                Point(1, 0),
                Point(1, 1),
                Point(2, 1),
            ]
        )
