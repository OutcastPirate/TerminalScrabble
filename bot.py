from player import Player
from checkDict import newDict
from copy import copy
from pointTable import pointTable
from math import floor
from settings import boardSize, boardCharacter
from fieldLetters import fieldLet


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
        words = sorted(self.checkOwnWords())
        bestWord = words[0]
        mid = floor(boardSize / 2)
        if board._fields[mid][mid]._letter == boardCharacter:
            board.insertHorizontal(bestWord, (fieldLet(mid + 1), mid + 1), ref)
