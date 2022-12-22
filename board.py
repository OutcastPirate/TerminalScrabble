from settings import boardSize
from field import Field


class Board:
    def __init__(self):
        self._size = boardSize
        self._fields = []
        for i in range(boardSize):
            row = []
            for x in range(boardSize):
                rowField = Field()
                row.append(rowField)
            self._fields.append(row)

    def getBoard(self):
        return self._fields


# game = Board()
# print(game.getBoard())
