from settings import boardSize, boardCharacter
from field import Field
from fieldLetters import fieldInt
from checkDict import getWords


class WrongWordError(Exception):
    pass


class BoardError(Exception):
    pass


def wordInDict(word):
    if word not in getWords(word[0]):
        # raise WrongWordError("This word doesn't exist in the dictionary.")
        return False
    return True


class Board:
    def __init__(self):
        if boardSize % 2 == 0:
            raise BoardError("Board size have to be an odd number")
        else:
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

    def insertHorizontal(self, content, position):
        row, column = position
        row = fieldInt(row[0])
        content = content.upper()
        for i in range(len(content)):
            self._fields[row - 1][column + i - 1].setLetter(content[i])

    def insertVertical(self, content, position):
        row, column = position
        row = fieldInt(row[0])
        content = content.upper()
        for i in range(len(content)):
            self._fields[row + i - 1][column - 1].setLetter(content[i])

    def validateBoard(self):
        words = []
        for i in range(boardSize):
            row = ''
            for o in range(boardSize):
                row += self._fields[i][o].letter
            line = row.split(boardCharacter)
            for word in line:
                if word != '' and len(word) > 1:
                    words.append(word)
        for i in range(boardSize):
            row = ''
            for o in range(boardSize):
                row += self._fields[o][i].letter
            line = row.split(boardCharacter)
            for word in line:
                if word != '' and len(word) > 1:
                    words.append(word)
        for word in words:
            if not wordInDict(word.lower()):
                # raise WrongWordError(f"{word} doesn't exist in dictionary.")
                return False
        return True

    def getWords(self):
        words = []
        for i in range(boardSize):
            row = ''
            for o in range(boardSize):
                row += self._fields[i][o].letter
            line = row.split(boardCharacter)
            for word in line:
                if word != '' and len(word) > 1:
                    words.append(word)
        for i in range(boardSize):
            row = ''
            for o in range(boardSize):
                row += self._fields[o][i].letter
            line = row.split(boardCharacter)
            for word in line:
                if word != '' and len(word) > 1:
                    words.append(word)
        return words
