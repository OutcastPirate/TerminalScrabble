from board import Board
import settings
from colors import Color
from fieldLetters import fieldLet


class Game:
    def __init__(self):
        self._board = Board()

    @property
    def gameBoard(self):
        return self._board

    def printBoard(self):
        for i in range(settings.boardSize+1):
            print(f'{Color.BOLD}{i}{Color.ENDC}', end="\t")
        print('\n')
        for i in range(settings.boardSize):
            print(f'{Color.BOLD}{fieldLet(i+1)}{Color.ENDC}', end="\t")
            for field in self.gameBoard.getBoard()[i]:
                print(f'{Color.WARNING}{field.letter}{Color.ENDC}', end='\t')
            print('\n')


scrabble = Game()
scrabble.printBoard()
