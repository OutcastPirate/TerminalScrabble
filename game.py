from board import Board
import settings
from colors import Color
from fieldLetters import fieldLet
from board import BoardError
from tiles import tiles
from player import Player
from math import floor
from copy import copy
from field import FieldError
import os


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

    def displayLeaderboard(self):
        os.system('cls')
        print('\n')
        print(f'\t{Color.BOLD}{Color.BLU}{"Leaderboard":^30}{Color.ENDC}')
        print(f'\t{Color.BOLD}{"Player":20}{"Points":>10}{Color.ENDC}')
        print("\t" + f"{Color.BOLD}-{Color.ENDC}" * 30)
        for player in self._players:
            print(f'\t{player._name:20}{player._points:>10}')
        print('\n' * 5)
        os.system('pause')

    def horizontalWord(self, content, position):
        self._tempBoard.insertHorizontal(content, position)
        # if not self._tempBoard.validateBoard():
        #     raise BoardError(f"{content} on {position} does not match board")
        #     # print(f"{content} on {position} does not match current board")
        # else:
        #     pass
        #     self._board.insertHorizontal(content, position)
        pass

    def verticalWord(self, content, position):
        self._tempBoard.insertVertical(content, position)
        # if not self._tempBoard.validateBoard():
        #     raise BoardError(f"{content} on {position} does not match board")
        #     # print(f"{content} on {position} does not match current board")
        # else:
        #     pass
        #     self._board.insertVertical(content, position)
        pass

    def printBoard(self):
        for i in range(settings.boardSize+1):
            print(f'{Color.BOLD}{i}{Color.ENDC}', end="")
        print('\n')
        for i in range(settings.boardSize):
            print(f'{Color.BOLD}{fieldLet(i+1)}{Color.ENDC}', end="\t")
            for field in self.gameBoard.getBoard()[i]:
                middle = floor(settings.boardSize / 2)
                if field == self.gameBoard.getBoard()[middle][middle]:
                    print(f'{Color.MID}{Color.BOLD}{field.letter}{Color.ENDC}', end='\t')  # noqa: E501
                elif field.letter == settings.boardCharacter:
                    print(f'{Color.RED}{field.letter}{Color.ENDC}', end='\t')
                else:
                    print(f'{Color.GRE}{field.letter}{Color.ENDC}', end='\t')
            print('\n')

    def printTempBoard(self):
        for i in range(settings.boardSize+1):
            print(f'{Color.BOLD} {i} {Color.ENDC}', end="\t")
        print('\n')
        for i in range(settings.boardSize):
            print(f'{Color.BOLD} {fieldLet(i+1)}{Color.ENDC}', end="\t")
            for field in self._tempBoard.getBoard()[i]:
                middle = floor(settings.boardSize / 2)
                if field == self._tempBoard.getBoard()[middle][middle]:
                    if field.letter == settings.boardCharacter:
                        print(f'{Color.MID}{Color.BOLD}{field.letter}{Color.ENDC}', end='\t')  # noqa: E501
                    else:
                        print(f'{Color.MID}{Color.BOLD} {field.letter} {Color.ENDC}', end='\t')  # noqa: E501
                elif field.letter == settings.boardCharacter:
                    print(f'{Color.RED}{field.letter}{Color.ENDC}', end='\t')
                else:
                    print(f'{Color.GRE} {field.letter} {Color.ENDC}', end='\t')
            print('\n')

    def placeTilesTurn(self, currentPlayer):
        row = input("Choose row: ")
        column = int(input("Choose column: "))
        rows = []
        for i in range(settings.boardSize):
            rows.append(fieldLet(i+1))
        if column not in range(1, settings.boardSize + 1) or row not in rows:
            raise IndexError
        position = (row, column)
        word = input("Choose tile(s): ")
        word = word.upper()
        while True:
            direction = input("Direction => down/right: ")
            if direction == 'down':
                self.verticalWord(word, position)
                break
            elif direction == 'right':
                self.horizontalWord(word, position)
                break
            else:
                print("Wrong direction, choose again: ")
        while True:
            counter = 0
            for letter in word:
                if letter not in currentPlayer._tileLetters:
                    word = input("Invalid tiles, choose again: ")
                    continue
                else:
                    tileIndex = currentPlayer._tileLetters.index(letter)  # noqa: E501
                    del currentPlayer._tiles[tileIndex]
                    del currentPlayer._tileLetters[tileIndex]
                    counter += 1
            if counter == len(word):
                break

    def swapTilesTurn(self, currentPlayer):
        print("Format: '1,2,3' -> swap the first three tiles")
        chosen = input("Wchich tiles do you want to swap: ")
        positions = chosen.split(',')
        for number in positions:
            number = int(number)
        currentPlayer.swapTiles(positions, self._tiles)
        print(f'Your new tiles: {currentPlayer._tileLetters}')
        os.system('pause')

    def cancelMoveTurn(self, currentPlayer, tiles):
        self.turnBoards(self._tempBoard, self._board)
        currentPlayer._tiles = copy(tiles)
        currentPlayer.updateLetters()

    def turnBoards(self, board, finalBoard):
        for i in range(settings.boardSize):
            for o in range(settings.boardSize):
                board._fields[i][o]._letter = finalBoard._fields[i][o]._letter

    def checkNewWords(self):
        newWords = []
        boardWords = self._board.getWords()
        tempBoardWords = self._tempBoard.getWords()
        for word in tempBoardWords:
            if word not in boardWords:
                newWords.append(word)
        return newWords

    def play(self):
        for player in self.players:
            player.getStartingTiles(self._tiles)
        gameInProgress = True
        playerIndex = 0
        turnIndex = 0
        playerMoveCounter = 0
        while (gameInProgress):
            os.system('cls')
            print('.')
            os.system('cls')
            self.printTempBoard()
            endTurn = False
            currentPlayer = self._players[playerIndex]
            if playerMoveCounter == 0:
                cancelTurn = {
                    'tiles': copy(currentPlayer._tiles),
                    'board': copy(self._board)
                }
            print(f'{len(self._tiles)} tiles left in the bag.')
            print(f"{currentPlayer._name}'s turn")
            print(f'Your tiles: {currentPlayer._tileLetters}')
            while True:
                playerMoveCounter += 1
                if playerMoveCounter == 1:
                    turn = input("Choose a move => (s)-swap  (p)-place (e)-end turn: ")  # noqa: E501
                else:
                    turn = input("Choose a move => (p)-place (e)-end turn (c)-cancel turn: ")  # noqa: E501
                if turn == 's' and playerMoveCounter == 1:
                    self.swapTilesTurn(currentPlayer)
                    endTurn = True
                elif turn == 'p':
                    try:
                        self.placeTilesTurn(currentPlayer)
                    except IndexError:
                        print("Chosen row/column does not exist")
                        os.system('pause')
                    except FieldError:
                        print("Chosen field is occupied")
                        os.system('pause')
                    break
                elif turn == 'e':
                    endTurn = True
                elif turn == 'c':
                    self.cancelMoveTurn(currentPlayer, cancelTurn['tiles'])
                    playerMoveCounter = 0
                    break
                else:
                    print("Wrong move, choose again: ")
                if endTurn:
                    try:
                        if not self._tempBoard.validateBoard():
                            raise BoardError()
                        currentPlayer.givePoints(self.checkNewWords())
                        self.turnBoards(self._board, self._tempBoard)
                        currentPlayer.reloadTiles(self._tiles)
                        playerIndex = (playerIndex + 1) % len(self.players)
                        playerMoveCounter = 0
                        turnIndex += 1
                        if playerIndex == 0:
                            self.displayLeaderboard()
                        break
                    except BoardError:
                        print("Current board layout is incorrect")


scrabble = Game()
Jack = Player("Jack")
Bob = Player("Bob")
scrabble.addPlayer(Jack)
scrabble.addPlayer(Bob)
scrabble.play()

# scrabble.horizontalWord('kot', ("B", 2))
# scrabble.verticalWord("pies", ("C", 9))
# scrabble.verticalWord("krata", ("A", 6))
# scrabble.printBoard()
