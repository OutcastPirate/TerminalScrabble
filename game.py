from board import Board, BoardError
from settings import BSIZE
from fieldLetters import fieldLet
from tiles import tiles
from tile import TileError
from player import Player
from copy import copy
from random import choice
from bot import Bot


class NameRepetitionError(Exception):
    pass


class Game:
    def __init__(self):
        self._tempBoard = Board()
        self._board = Board()
        self._tiles = tiles
        self._players = []
        self._winner = Player('')
        self._turnsSkipped = 0
        self._gameInProgress = False
        self._playerIndex = 0
        self._botEnd = 0
        self._turnIndex = 0
        self._playerMoveCounter = 0
        self._ENDGAME = False
        self._botCancel = False
        self._endTurn = False
        self._currentPlayer = Player('')

    @property
    def gameBoard(self):
        return self._board

    def getPlayerNames(self):
        names = []
        for player in self._players:
            names.append(player._name)
        return names

    def addPlayer(self, player):
        if not isinstance(player, Player):
            raise ValueError("Player has to be an instance of Player class")
        names = self.getPlayerNames()
        if player._name in names:
            raise NameRepetitionError
        self._players.append(player)

    def removePlayer(self, player):
        if player not in self._players:
            raise ValueError("This player is not in game")
        self._players.remove(player)

    @property
    def players(self):
        return self._players

    def setGameVariables(self):
        self.assignTiles()
        self._turnsSkipped = 0
        self._gameInProgress = True
        self._playerIndex = 0
        self._botEnd = 0
        self._turnIndex = 1
        self._playerMoveCounter = 0
        self._ENDGAME = False
        self._botCancel = False
        self._endTurn = False
        self._cancelTurn = {}
        self._currentPlayer = None

    def validatePlayerCount(self):
        if len(self._players) == 4:
            return 0
        elif len(self._players) < 2:
            return 1
        else:
            return 2

    def horizontalWord(self, content, position):
        self._tempBoard.insertHorizontal(content, position, self._board)

    def verticalWord(self, content, position):
        self._tempBoard.insertVertical(content, position, self._board)

    def assignTiles(self):
        for player in self.players:
            player.getStartingTiles(self._tiles)

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

    def cancelMoveTurn(self, currentPlayer):
        self.turnBoards(self._tempBoard, self._board)
        currentPlayer._tiles = copy(self._cancelTurn['tiles'])
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

    def setWinner(self):
        points = []
        for player in self._players:
            points.append(player._points)
        maxPoints = max(points)
        if points.count(maxPoints) > 1:
            self._winner = None
        else:
            index = points.index(maxPoints)
            self._winner = self._players[index]

    def checkGameEnd(self):
        endTerm1 = self._playerIndex == 0
        endTerm2 = len(self._tiles) == 0
        if endTerm1 and endTerm2:
            self._ENDGAME = True

    def preparePlayer(self):
        self._endTurn = False
        self._botCancel = False
        self._currentPlayer = self._players[self._playerIndex]
        if self._playerMoveCounter == 0:
            self._cancelTurn = {
                'tiles': copy(self._currentPlayer._tiles),
                'board': copy(self._board)
            }

    def defineBotTurn(self):
        if self._playerMoveCounter >= 2:
            if self._botCancel:
                return 'c'
            else:
                self._turnsSkipped = 0
                return 'e'
        else:
            return 'p'

    def endTurn(self, currentPlayer):
        if not self._tempBoard.validateBoard():
            raise BoardError()
        currentPlayer.givePoints(self.checkNewWords())
        self.turnBoards(self._board, self._tempBoard)
        currentPlayer.reloadTiles(self._tiles)
        pIndex = self._playerIndex + 1
        self._playerIndex = pIndex % len(self.players)
        self._playerMoveCounter = 0
        self._turnIndex += 1

    def verifyEndTurn(self):
        if self._playerMoveCounter == 1:
            self._turnsSkipped += 1
        else:
            self._turnsSkipped = 0
