from board import Board, WrongWordError
from settings import boardCharacter as BCHAR
from settings import boardSize as BSIZE
from colors import Color as C
from fieldLetters import fieldLet
from board import BoardError, NotConnectedError
from tiles import tiles
from tile import TileError
from player import Player
from bot import Bot
from math import floor
from copy import copy
from field import FieldError
# from checkDict import createDict
from random import choice
from os import system, name as osName


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

    def printTempBoard(self):
        for i in range(BSIZE+1):
            print(f'{C.BD} {i} {C.ENDC}', end="\t")
        print('\n')
        for i in range(BSIZE):
            print(f'{C.BD} {fieldLet(i+1)}{C.ENDC}', end="\t")
            for field in self._tempBoard.getBoard()[i]:
                middle = floor(BSIZE / 2)
                if field == self._tempBoard.getBoard()[middle][middle]:
                    format = C.MID + C.BD
                    if field.letter == BCHAR:
                        print(f'{format}{field.letter}{C.ENDC}', end='\t')
                    else:
                        print(f'{format} {field.letter} {C.ENDC}', end='\t')
                elif field.letter == BCHAR:
                    print(f'{C.RED}{field.letter}{C.ENDC}', end='\t')
                else:
                    print(f'{C.GRE} {field.letter} {C.ENDC}', end='\t')
            print('\n')

    def placeTilesCheck(self, currentPlayer, cancelTurn):
        try:
            self.placeTilesTurn(currentPlayer)
            middle = floor(BSIZE / 2)
            if self._tempBoard.getBoard()[middle][middle]._letter == BCHAR:
                self.cancelMoveTurn(currentPlayer, cancelTurn['tiles'])
                print('\nFirst tile has to be placed on the middle field. \n')
                input()
        except IndexError:
            print("Chosen field out of bounds")
            self.cancelMoveTurn(currentPlayer, cancelTurn['tiles'])
            input()
        except FieldError:
            if not isinstance(currentPlayer, Bot):
                print("Chosen field is occupied")
                input()
        except TileError:
            if not isinstance(currentPlayer, Bot):
                print("\nAvailable tiles don't match the input.\n")
                input()
        except NotConnectedError:
            if not isinstance(currentPlayer, Bot):
                print("\nAll tiles have to be connected.\n")
                input()
        except WrongWordError:
            if not isinstance(currentPlayer, Bot):
                print("Word goes out of bounds")
                input()
            self.cancelMoveTurn(currentPlayer, cancelTurn['tiles'])

    def placeTilesTurn(self, currentPlayer):
        if not isinstance(currentPlayer, Bot):
            print("\nFormat: coordinates separated with a blank space")
            print('Multiple tiles: 1 A - write down / A 1 - write right\n')
            field = input('Choose input field: ')
            position = field.split(' ')
            try:
                row = position[0]
                column = int(position[1])
                direction = 'right'
            except ValueError:
                row = position[1]
                try:
                    column = int(position[0])
                except ValueError:
                    raise IndexError
                direction = 'down'
            rows = []
            for i in range(BSIZE + 1):
                rows.append(fieldLet(i+1))
            if column <= 0 or column > BSIZE or row not in rows:
                raise IndexError("Coords out of bounds")
            coords = (row, column)
            word = input("Choose tile(s): ")
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

    def swapTilesTurn(self, currentPlayer):
        print("Format: '1,2,3' -> swap the first three tiles")
        chosen = input("Wchich tiles do you want to swap: ")
        positions = chosen.split(',')
        currentPlayer.swapTiles(positions, self._tiles)
        print(f'Your new tiles: {currentPlayer._tileLetters}')
        input()

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
        if isinstance(currentPlayer, Bot):
            if (osName == 'posix'):
                system('clear')
            else:
                system('cls')
            self.printTempBoard()
            input()
