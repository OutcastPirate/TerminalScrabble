from settings import boardSize, boardCharacter
from field import Field
from fieldLetters import fieldInt
from checkDict import getWords
from math import floor


class NotConnectedError(Exception):
    pass


class WrongWordError(Exception):
    pass


class BoardError(Exception):
    pass


def wordInDict(word):
    if word not in getWords(word[0]):
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

    def insertHorizontal(self, content, position, reference):
        row, column = position
        row = fieldInt(row[0])
        content = content.upper()
        validate = []
        validate.append((row - 1, column - 2))
        for i in range(len(content)):
            validate.append((row, column + i - 1))
            validate.append((row - 2, column + i - 1))
        validate.append((row - 1, column - 1 + len(content)))
        letters = []
        for field in validate:
            try:
                letters.append(self._fields[field[0]][field[1]]._letter)
            except IndexError:
                pass

        middle = floor(boardSize / 2)
        firstTerm = (len(set(letters)) == 1)
        secondTerm = (list(set(letters))[0] == boardCharacter)
        thirdTerm = (self._fields[middle][middle]._letter != boardCharacter)
        if firstTerm and secondTerm and thirdTerm:
            raise NotConnectedError
        for i in range(len(content)):
            self._fields[row - 1][column + i - 1].setLetter(content[i])

    def insertVertical(self, content, position, reference):
        row, column = position
        row = fieldInt(row[0])
        content = content.upper()
        validate = []
        validate.append((row - 2, column - 1))
        for i in range(len(content)):
            validate.append((row + i - 1, column - 2))
            validate.append((row + i - 1, column))
        validate.append((row - 1 + len(content), column - 1))
        letters = []
        for field in validate:
            try:
                letters.append(self._fields[field[0]][field[1]]._letter)
            except IndexError:
                raise WrongWordError
        middle = floor(boardSize / 2)
        firstTerm = (len(set(letters)) == 1)
        secondTerm = (list(set(letters))[0] == boardCharacter)
        thirdTerm = (self._fields[middle][middle]._letter != boardCharacter)
        if firstTerm and secondTerm and thirdTerm:
            raise NotConnectedError
        for i in range(len(content)):
            self._fields[row + i - 1][column - 1].setLetter(content[i])

    def validateBoard(self):
        words = self.getBoardWords()
        for word in words:
            if not wordInDict(word.lower()):
                return False
        return True

    def getBoardWords(self):
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
