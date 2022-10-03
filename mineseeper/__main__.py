import curses

import click

from mineseeper.game import Game
from mineseeper.view import CursesView


@click.command()
@click.option('--width', '-w', default=8)
@click.option('-h', '--height', default=8)
@click.option('--mines', '-m', default=8)
def main(width: int, height: int, mines: int):

    game = Game(width, height, mines)
    view = CursesView(game)
    view.start()


if __name__ == '__main__':
    main()
