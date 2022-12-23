from board import Board
import settings
from colors import Color
from fieldLetters import fieldLet
from board import BoardError
from tiles import tiles


class Game:
    def __init__(self):
        self._tempBoard = Board()
        self._board = Board()
        self._tiles = tiles

    @property
    def gameBoard(self):
        return self._board

    def horizontalWord(self, content, position):
        self._tempBoard.insertHorizontal(content, position)
        if not self._tempBoard.validateBoard():
            raise BoardError(f"{content} on {position} does not match board")
            # print(f"{content} on {position} does not match current board")
        else:
            self._board.insertHorizontal(content, position)

    def verticalWord(self, content, position):
        self._tempBoard.insertVertical(content, position)
        if not self._tempBoard.validateBoard():
            raise BoardError(f"{content} on {position} does not board")
            # print(f"{content} on {position} does not match current board")
        else:
            self._board.insertVertical(content, position)

    def printBoard(self):
        for i in range(settings.boardSize+1):
            print(f'{Color.BOLD}{i}{Color.ENDC}', end="\t")
        print('\n')
        for i in range(settings.boardSize):
            print(f'{Color.BOLD}{fieldLet(i+1)}{Color.ENDC}', end="\t")
            for field in self.gameBoard.getBoard()[i]:
                if field.letter == '▢':
                    print(f'{Color.RED}{field.letter}{Color.ENDC}', end='\t')
                else:
                    print(f'{Color.GRE}{field.letter}{Color.ENDC}', end='\t')
            print('\n')


scrabble = Game()
scrabble.horizontalWord('kot', ("B", 2))
scrabble.verticalWord("pies", ("C", 9))
scrabble.verticalWord("krata", ("A", 6))
scrabble.printBoard()
