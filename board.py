from settings import BSIZE, BOARDCHARACTER
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


class BadFitError(Exception):
    pass


def wordInDict(word):
    if word not in getWords(word[0]):
        return False
    return True


class Board:
    def __init__(self):
        if BSIZE % 2 == 0 or BSIZE < 15:
            if __name__ != 'main':
                print("\nCannot start with current settings.\n")
                print("Board size has to be an even number >= 15.\n")
                quit()
        else:
            self._size = BSIZE
        self._fields = []
        for i in range(BSIZE):
            row = []
            for x in range(BSIZE):
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

        middle = floor(BSIZE / 2)
        firstTerm = (len(set(letters)) == 1)
        secondTerm = (list(set(letters))[0] == BOARDCHARACTER)
        thirdTerm = (self._fields[middle][middle]._letter != BOARDCHARACTER)
        if firstTerm and secondTerm and thirdTerm:
            raise NotConnectedError
        for i in range(len(content)):
            self._fields[row - 1][column + i - 1].setLetter(content[i])
        fourthTerm = (self._fields[middle][middle]._letter == BOARDCHARACTER)
        if firstTerm and secondTerm and fourthTerm:
            raise NotConnectedError

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
                pass
        middle = floor(BSIZE / 2)
        firstTerm = (len(set(letters)) == 1)
        secondTerm = (list(set(letters))[0] == BOARDCHARACTER)
        thirdTerm = (self._fields[middle][middle]._letter != BOARDCHARACTER)
        if firstTerm and secondTerm and thirdTerm:
            raise NotConnectedError
        for i in range(len(content)):
            self._fields[row + i - 1][column - 1].setLetter(content[i])
        fourthTerm = (self._fields[middle][middle]._letter == BOARDCHARACTER)
        if firstTerm and secondTerm and fourthTerm:
            raise NotConnectedError

    def validateBoard(self):
        words = self.getBoardWords()
        for word in words:
            if not wordInDict(word.lower()):
                return False
        return True

    def getBoardWords(self):
        words = []
        for i in range(BSIZE):
            row = ''
            for o in range(BSIZE):
                row += self._fields[i][o].letter
            line = row.split(BOARDCHARACTER)
            for word in line:
                if word != '' and len(word) > 1:
                    words.append(word)
        for i in range(BSIZE):
            row = ''
            for o in range(BSIZE):
                row += self._fields[o][i].letter
            line = row.split(BOARDCHARACTER)
            for word in line:
                if word != '' and len(word) > 1:
                    words.append(word)
        return words

    def validateMoveFit(self, word, coords, direction):
        row = fieldInt(coords[0]) - 1
        column = coords[1] - 1
        if direction == 'right':
            for i in range(len(word)):
                if column + i not in range(BSIZE):
                    raise BadFitError
        if direction == 'down':
            for i in range(len(word)):
                if row + i not in range(BSIZE):
                    raise BadFitError
