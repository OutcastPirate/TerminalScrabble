from player import Player
from checkDict import newDict
from copy import copy
from pointTable import pointTable
from math import floor
from settings import boardSize as BSIZE, boardCharacter as BCHAR, maxWordLength
from random import choice


class Bot(Player):

    def checkOwnWords(self):
        possible = {}
        for letter in self._tileLetters:
            for word in newDict[letter]:
                avTiles = copy(self._tileLetters)
                counter = 0
                word = word.upper()
                for letter in word:
                    if letter in avTiles:
                        del avTiles[avTiles.index(letter)]
                        counter += 1
                if counter == len(word):
                    possible[word] = 0
        for word in possible.keys():
            for letter in word:
                possible[word] += pointTable[letter]
        return possible

    def lastLetterWords(self, letter):
        words = []
        letter = letter.lower()
        for dictLetter in newDict.values():
            for word in dictLetter:
                if word[-1] == letter:
                    words.append(word)
        return words

    def checkRightHorizontalMoves(self, board):
        for i in range(BSIZE):
            for j in range(BSIZE):
                possible = {}
                freeFields = 0
                try:
                    term1 = board._fields[i][j]._letter != BCHAR
                    term2 = board._fields[i][j - 1]._letter == BCHAR
                    term3 = board._fields[i][j + 1]._letter == BCHAR
                    term4 = board._fields[i - 1][j + 1]._letter == BCHAR
                    term5 = board._fields[i + 1][j + 1]._letter == BCHAR
                except IndexError:
                    continue
                if term1 and term2 and term3 and term4 and term5:
                    for x in range(maxWordLength):
                        if board._fields[i][j + x] == BCHAR:
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
                                counter += 1
                        subTerm1 = counter == len(word)
                        subTerm2 = word not in possible.keys()
                        if subTerm1 and subTerm2:
                            possible[word] = 0
                            for letter in word:
                                possible[word] += pointTable[letter]
                            if board._fields[i][j]._letter != BCHAR:
                                pts = possible[word]
                                pos = (i, j + 1)
                                self._moves.append([word, pts, pos, "right"])

    def checkVerticalMoves(self, board):
        for i in range(BSIZE):
            for j in range(BSIZE):
                possible = {}
                freeFields = 0
                try:
                    term1 = board._fields[i][j]._letter != BCHAR
                    term2 = board._fields[i - 1][j]._letter == BCHAR
                    term3 = board._fields[i + 1][j]._letter == BCHAR
                    term4 = board._fields[i + 1][j + 1]._letter == BCHAR
                    term5 = board._fields[i + 1][j - 1]._letter == BCHAR
                except IndexError:
                    continue
                if term1 and term2 and term3 and term4 and term5:
                    for x in range(maxWordLength):
                        if board._fields[i + x][j] == BCHAR:
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
                                counter += 1
                        subTerm1 = counter == len(word)
                        subTerm2 = word not in possible.keys()
                        if subTerm1 and subTerm2:
                            possible[word] = 0
                            for letter in word:
                                possible[word] += pointTable[letter]
                            coord = (i + 1, j)
                            pts = possible[word]
                            self._moves.append([word, pts, coord, "down"])

    def checkInvHorMoves(self, board):
        """
        Meaning: Check for (Inv)erted (Hor)izontal Moves

        Checks for possible moves where the last letter is already on the board
        """
        for i in range(BSIZE):
            for j in range(BSIZE):
                possible = {}
                freeFields = 0
                try:
                    term1 = board._fields[i][j]._letter != BCHAR
                    term2 = board._fields[i][j - 1]._letter == BCHAR
                    term3 = board._fields[i][j + 1]._letter == BCHAR
                    term4 = board._fields[i + 1][j - 1]._letter == BCHAR
                    term5 = board._fields[i - 1][j - 1]._letter == BCHAR
                except IndexError:
                    continue
                if term1 and term2 and term3 and term4 and term5:
                    for x in range(maxWordLength):
                        if board._fields[i][j + x] == BCHAR:
                            freeFields += 1
                        else:
                            break
                    words = self.lastLetterWords(board._fields[i][j]._letter)
                    for word in words:
                        tiles = copy(self._tileLetters)
                        tiles.append(board._fields[i][j]._letter)
                        counter = 0
                        word = word.upper()
                        for letter in word:
                            if letter in tiles:
                                index = tiles.index(letter)
                                del tiles[index]
                                counter += 1
                        subTerm1 = counter == len(word)
                        subTerm2 = word not in possible.keys()
                        if subTerm1 and subTerm2:
                            possible[word] = 0
                            for letter in word:
                                possible[word] += pointTable[letter]
                            if board._fields[i][j]._letter != BCHAR:
                                text = " " + word[0:-1]
                                pts = possible[word]
                                indexTerm = (j - len(word) + 1) in range(BSIZE)
                                if indexTerm:
                                    pos = (i, j - len(word) + 1)
                                else:
                                    continue
                                self._moves.append([text, pts, pos, "right"])

    def checkInvVerMoves(self, board):
        """
        Meaning: Check for (Inv)erted (Ver)tical Moves

        Checks for possible moves where the last letter is already on the board
        """
        for i in range(BSIZE):
            for j in range(BSIZE):
                possible = {}
                freeFields = 0
                try:
                    term1 = board._fields[i][j]._letter != BCHAR
                    term2 = board._fields[i + 1][j]._letter == BCHAR
                    term3 = board._fields[i - 1][j]._letter == BCHAR
                    term4 = board._fields[i - 1][j - 1]._letter == BCHAR
                    term5 = board._fields[i - 1][j + 1]._letter == BCHAR
                except IndexError:
                    continue
                if term1 and term2 and term3 and term4 and term5:
                    for x in range(maxWordLength):
                        if board._fields[i - x][j] == BCHAR:
                            freeFields += 1
                        else:
                            break
                    words = self.lastLetterWords(board._fields[i][j]._letter)
                    for word in words:
                        tiles = copy(self._tileLetters)
                        tiles.append(board._fields[i][j]._letter)
                        counter = 0
                        word = word.upper()
                        for letter in word:
                            if letter in tiles:
                                index = tiles.index(letter)
                                del tiles[index]
                                counter += 1
                        subTerm1 = counter == len(word)
                        subTerm2 = word not in possible.keys()
                        if subTerm1 and subTerm2:
                            possible[word] = 0
                            for letter in word:
                                possible[word] += pointTable[letter]
                            if board._fields[i][j]._letter != BCHAR:
                                text = " " + word[0:-1]
                                indexTerm = (i - len(word) + 1) in range(BSIZE)
                                if indexTerm:
                                    coords = (i - len(word) + 1, j)
                                else:
                                    continue
                                pts = possible[word]
                                self._moves.append([text, pts, coords, "down"])

    def makeMove(self, board, ref):
        self._moves = []
        words = self.checkOwnWords()
        if len(words) > 0:
            bestWord = max(words, key=words.get)
        mid = floor(BSIZE / 2)
        if board._fields[mid][mid]._letter == BCHAR:
            word = " " + bestWord
            direction = choice(["right", "down"])
            self._moves.append([word, 0, (mid, mid), direction])
        else:
            self.checkRightHorizontalMoves(board)
            self.checkVerticalMoves(board)
            self.checkInvHorMoves(board)
            self.checkInvVerMoves(board)
