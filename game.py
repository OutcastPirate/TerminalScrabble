from board import Board, BoardError
from settings import boardSize as BSIZE
from fieldLetters import fieldLet
from tiles import tiles
from tile import TileError
from player import Player
from copy import copy
from random import choice
from bot import Bot


class Game:
    def __init__(self):
        self._tempBoard = Board()
        self._board = Board()
        self._tiles = tiles
        self._players = []

    @property
    def gameBoard(self):
        return self._board

    def addPlayer(self, player):
        if not isinstance(player, Player):
            raise ValueError("Player has to be an instance of Player class")
        self._players.append(player)

    def removePlayer(self, player):
        if player not in self._players:
            raise ValueError("This player is not in game")
        self._players.remove(player)

    @property
    def players(self):
        return self._players

    def horizontalWord(self, content, position):
        self._tempBoard.insertHorizontal(content, position, self._board)

    def verticalWord(self, content, position):
        self._tempBoard.insertVertical(content, position, self._board)

    def placeTilesTurn(self, currentPlayer, word, coords, direction):
        if not isinstance(currentPlayer, Bot):
            word = word.upper()
            for letter in word:
                if letter not in currentPlayer._tileLetters:
                    raise TileError
        else:
            move = choice(currentPlayer._moves)
            word = move[0][1:]
            direction = move[3]
            coords = (fieldLet(move[2][0] + 1), move[2][1] + 1)
        if direction == 'down':
            try:
                self.verticalWord(word, coords)
            except IndexError:
                return
        elif direction == 'right':
            try:
                self.horizontalWord(word, coords)
            except IndexError:
                return
        for letter in word:
            tileIndex = currentPlayer._tileLetters.index(letter)
            del currentPlayer._tiles[tileIndex]
            del currentPlayer._tileLetters[tileIndex]

    def cancelMoveTurn(self, currentPlayer, tiles):
        self.turnBoards(self._tempBoard, self._board)
        currentPlayer._tiles = copy(tiles)
        currentPlayer.updateLetters()

    def turnBoards(self, board, finalBoard):
        for i in range(BSIZE):
            for o in range(BSIZE):
                board._fields[i][o]._letter = finalBoard._fields[i][o]._letter

    def checkNewWords(self):
        newWords = []
        boardWords = self._board.getBoardWords()
        tempBoardWords = self._tempBoard.getBoardWords()
        for word in tempBoardWords:
            if word not in boardWords:
                newWords.append(word)
        return newWords

    def endTurn(self, currentPlayer):
        if not self._tempBoard.validateBoard():
            raise BoardError()
        currentPlayer.givePoints(self.checkNewWords())
        self.turnBoards(self._board, self._tempBoard)
        currentPlayer.reloadTiles(self._tiles)
