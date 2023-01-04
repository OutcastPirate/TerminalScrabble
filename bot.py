from player import Player
from checkDict import newDict
from copy import copy
from pointTable import pointTable
from math import floor
from settings import boardSize, boardCharacter, maxWordLength
from random import choice
from board import NotConnectedError, BoardError
from field import FieldError


class Bot(Player):

    def checkOwnWords(self):
        possible = {}
        for letter in self._tileLetters:
            for word in newDict[letter]:
                availableTiles = copy(self._tileLetters)
                counter = 0
                word = word.upper()
                for letter in word:
                    if letter in availableTiles:
                        del availableTiles[availableTiles.index(letter)]
                        counter += 1
                if counter == len(word):
                    possible[word] = 0
        for word in possible.keys():
            for letter in word:
                possible[word] += pointTable[letter]
        return possible

    def makeMove(self, board, ref):
        self._moves = []
        words = sorted(self.checkOwnWords())
        if len(words) > 0:
            bestWord = words[0]
        mid = floor(boardSize / 2)
        moves = []
        if board._fields[mid][mid]._letter == boardCharacter:
            moves.append([bestWord, 0, (mid, mid), choice(("right", "down"))])
        else:
            for i in range(boardSize):
                stop = False
                for j in range(boardSize):
                    possible = {}
                    freeFields = 0
                    if board._fields[i][j]._letter != boardCharacter and board._fields[i][j - 1]._letter == boardCharacter:  # noqa: E501
                        for x in range(maxWordLength):
                            if board._fields[i][j + x] == boardCharacter:
                                freeFields += 1
                            else:
                                break
                        for word in newDict[board._fields[i][j]._letter]:
                            tiles = copy(self._tileLetters)
                            tiles.append(board._fields[i][j]._letter)
                            counter = 0
                            word = word.upper()
                            for letter in word:
                                if letter in tiles:
                                    index = tiles.index(letter)
                                    del tiles[index]
                                    # try:
                                    #     del self._tiles[index]
                                    # except IndexError:
                                    #     pass
                                    counter += 1
                            if counter == len(word) and word not in possible.keys():  # noqa: E501
                                possible[word] = 0
                                for letter in word:
                                    possible[word] += pointTable[letter]
                                moves.append([word, possible[word], (i, j + 1), "right"])  # noqa: E501
                            if len(possible) > 0:
                                try:
                                    if not board.validateBoard():
                                        raise BoardError()

                                    # board.insertHorizontal(sorted(possible)[0], (fieldLet(i + 1), j + 1), ref)  # noqa: E501

                                except (NotConnectedError, FieldError, BoardError):  # noqa: E501
                                    pass
                if stop:
                    break
        self._moves = moves
