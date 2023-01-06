from board import Board
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
from checkDict import createDict
from random import choice
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
        if (os.name == 'posix'):
            os.system('clear')
        else:
            os.system('cls')
        print('\n')
        print(f'\t{C.BOLD}{C.BLU}{"Leaderboard":^30}{C.ENDC}')
        print(f'\t{C.BOLD}{"Player":20}{"Points":>10}{C.ENDC}')
        print("\t" + f"{C.BOLD}-{C.ENDC}" * 30)
        for player in self._players:
            print(f'\t{player._name:20}{player._points:>10}')
        print('\n' * 5)
        input()

    def displayFinalPoints(self):
        if (os.name == 'posix'):
            os.system('clear')
        else:
            os.system('cls')
        print('\n')
        print(f'\t{C.BOLD}{C.RED}{"THE GAME ENDED":^30}{C.ENDC}')
        print('\n')
        print(f'\t{C.BOLD}{C.BLU}{"Leaderboard":^30}{C.ENDC}')
        print(f'\t{C.BOLD}{"Player":20}{"Points":>10}{C.ENDC}')
        print("\t" + f"{C.BOLD}-{C.ENDC}" * 30)
        for player in self._players:
            print(f'\t{player._name:20}{player._points:>10}')
        print('\n' * 2)
        if self._winner._points != 0:
            print(f'{C.MID}{self._winner._name} won! Congratulations!{C.ENDC}')
        else:
            print(f'{C.MID}It was a draw!{C.ENDC}')
        print('\n' * 4)
        input()

    def horizontalWord(self, content, position):
        self._tempBoard.insertHorizontal(content, position, self._board)
        # if not self._tempBoard.validateBoard():
        #     raise BoardError(f"{content} on {position} does not match board")
        #     # print(f"{content} on {position} does not match current board")
        # else:
        #     pass
        #     self._board.insertHorizontal(content, position)
        pass

    def verticalWord(self, content, position):
        self._tempBoard.insertVertical(content, position, self._board)
        # if not self._tempBoard.validateBoard():
        #     raise BoardError(f"{content} on {position} does not match board")
        #     # print(f"{content} on {position} does not match current board")
        # else:
        #     pass
        #     self._board.insertVertical(content, position)
        pass

    def printBoard(self):
        for i in range(BSIZE+1):
            print(f'{C.BOLD}{i}{C.ENDC}', end="")
        print('\n')
        for i in range(BSIZE):
            print(f'{C.BOLD}{fieldLet(i+1)}{C.ENDC}', end="\t")
            for field in self.gameBoard.getBoard()[i]:
                middle = floor(BSIZE / 2)
                if field == self.gameBoard.getBoard()[middle][middle]:
                    print(f'{C.MID}{C.BOLD}{field.letter}{C.ENDC}', end='\t')
                elif field.letter == BCHAR:
                    print(f'{C.RED}{field.letter}{C.ENDC}', end='\t')
                else:
                    print(f'{C.GRE}{field.letter}{C.ENDC}', end='\t')
            print('\n')

    def printTempBoard(self):
        for i in range(BSIZE+1):
            print(f'{C.BOLD} {i} {C.ENDC}', end="\t")
        print('\n')
        for i in range(BSIZE):
            print(f'{C.BOLD} {fieldLet(i+1)}{C.ENDC}', end="\t")
            for field in self._tempBoard.getBoard()[i]:
                middle = floor(BSIZE / 2)
                if field == self._tempBoard.getBoard()[middle][middle]:
                    if field.letter == BCHAR:
                        print(f'{C.MID}{C.BOLD}{field.letter}{C.ENDC}', end='\t')  # noqa: E501
                    else:
                        print(f'{C.MID}{C.BOLD} {field.letter} {C.ENDC}', end='\t')  # noqa: E501
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
        # except IndexError:
        #     print("Chosen field out of bounds")
        #     self.cancelMoveTurn(currentPlayer, cancelTurn['tiles'])
        #     input()
        except FieldError:
            print("Chosen field is occupied")
            input()
        except TileError:
            print("\nAvailable tiles don't match the input.\n")
            input()
        except NotConnectedError:
            print("\nAll tiles have to be connected.\n")
            input()

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
            tileIndex = currentPlayer._tileLetters.index(letter)  # noqa: E501
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
        boardWords = self._board.getWords()
        tempBoardWords = self._tempBoard.getWords()
        for word in tempBoardWords:
            if word not in boardWords:
                newWords.append(word)
        return newWords

    def beginGame(self):
        createDict()
        players = []
        while (True):
            if (os.name == 'posix'):
                os.system('clear')
            else:
                os.system('cls')
            print(f'{C.BOLD}{C.BLU}{"SCRABBLE":^40}{C.ENDC}\n')
            print('p - Add player')
            print('b - Add AI player (bot)')
            print('d - Delete player')
            print('s - Start Game\n')
            print(f'\t{C.BOLD}{C.BLU}{"Players":^20}{C.ENDC}')
            print("\t" + f"{C.BOLD}-{C.ENDC}" * 20)
            for index, player in enumerate(self._players):
                if isinstance(player, Bot):
                    print(f'\t{index + 1:>2}.{player._name:>14} {C.GRE}AI{C.ENDC}')  # noqa: E501
                else:
                    print(f'\t{index + 1:>2}.{player._name:>17}')
            print('\n' * 5)
            option = input("Choose option: ")
            if option == 'p' or option == 'b':
                if len(self._players) == 4:
                    print("\nCannot add more than 4 players.\n")
                    input()
                    continue
                playerName = input(f"Player {len(self._players) + 1}: ")
                if playerName == '':
                    print("\nPlayer's name cannot be empty\n")
                    input()
                    continue
                elif playerName in players:
                    print("\nPlayer's name has to be unique\n")
                    input()
                    continue
                players.append(playerName)
                if option == 'p':
                    newPlayer = Player(playerName)
                else:
                    newPlayer = Bot(playerName)
                self.addPlayer(newPlayer)
            elif option == 's':
                if (len(self._players) <= 1):
                    print('\nCannot start without at least 2 players\n')
                    input()
                    continue
                break
            elif option == 'd':
                if len(self._players) == 0:
                    print("\nThere are no players to remove\n")
                    input()
                    continue
                removeName = input("Remove player: ")
                if removeName not in players:
                    print("\nNo such player in game\n")
                    input()
                    continue
                else:
                    for x in range(len(players)):
                        if players[x] == removeName:
                            del players[x]
                            break
                    for player in self._players:
                        if player._name == removeName:
                            self.removePlayer(player)
                            break
                    continue
            else:
                print("\nWrong option. Choose again.\n")
                input()

    def endTurn(self, currentPlayer):
        if not self._tempBoard.validateBoard():
            raise BoardError()
        currentPlayer.givePoints(self.checkNewWords())
        self.turnBoards(self._board, self._tempBoard)
        currentPlayer.reloadTiles(self._tiles)
        if isinstance(currentPlayer, Bot):
            if (os.name == 'posix'):
                os.system('clear')
            else:
                os.system('cls')
            self.printTempBoard()
            input()

    def play(self):
        self.beginGame()
        for player in self.players:
            player.getStartingTiles(self._tiles)
        turnsSkipped = 0
        gameInProgress = True
        playerIndex = 0
        turnIndex = 0
        playerMoveCounter = 0
        ENDGAME = False
        while (gameInProgress):
            if ENDGAME:
                break
            if (os.name == 'posix'):
                os.system('clear')
            else:
                os.system('cls')
            self.printTempBoard()
            endTurn = False
            botCancel = False
            currentPlayer = self._players[playerIndex]
            if playerMoveCounter == 0:
                cancelTurn = {
                    'tiles': copy(currentPlayer._tiles),
                    'board': copy(self._board)
                }
            endTerm1 = len(currentPlayer._tiles) == 0
            endTerm2 = len(self._tiles) == 0
            if endTerm1 and endTerm2:
                ENDGAME = True
            print(f'{len(self._tiles)} tiles left in the bag.')
            print(f"{currentPlayer._name}'s turn")
            print(f'Your tiles: {currentPlayer._tileLetters}')
            while True:
                if ENDGAME:
                    break
                playerMoveCounter += 1
                if isinstance(currentPlayer, Bot):
                    if playerMoveCounter >= 2:
                        if botCancel:
                            turn = 'c'
                        else:
                            turn = 'e'
                    else:
                        turn = 'p'
                elif playerMoveCounter == 1:
                    turn = input("Choose a move => (s)-swap  (p)-place (e)-end turn: ")  # noqa: E501
                else:
                    turn = input("Choose a move => (p)-place (e)-end turn (c)-cancel turn: ")  # noqa: E501
                if turn == 's' and playerMoveCounter == 1:
                    try:
                        self.swapTilesTurn(currentPlayer)
                    except (ValueError, IndexError):
                        print('\nWrong format of input\n')
                        input()
                        self.cancelMoveTurn(currentPlayer, cancelTurn['tiles'])
                        playerMoveCounter = 0
                        break
                    endTurn = True
                elif turn == 'p':
                    if isinstance(currentPlayer, Bot):
                        currentPlayer.makeMove(self._tempBoard, self._board)
                        if len(currentPlayer._moves) == 0:
                            endTurn = True
                            break
                    self.placeTilesCheck(currentPlayer, cancelTurn)
                    break
                elif turn == 'e':
                    if playerMoveCounter == 1:
                        turnsSkipped += 1
                    endTurn = True
                elif turn == 'c':
                    self.cancelMoveTurn(currentPlayer, cancelTurn['tiles'])
                    playerMoveCounter = 0
                    botCancel = False
                    if isinstance(currentPlayer, Bot):
                        playerMoveCounter = 2
                        endTurn = True
                    break
                else:
                    print("Wrong move, choose again: ")
                if endTurn:
                    if turnsSkipped == len(self._players) * 2:
                        ENDGAME = True
                    try:
                        self.endTurn(currentPlayer)
                        playerIndex = (playerIndex + 1) % len(self.players)
                        playerMoveCounter = 0
                        turnIndex += 1
                        if playerIndex == 0:
                            self.displayLeaderboard()
                        break
                    except BoardError:
                        if isinstance(currentPlayer, Bot):
                            self.turnBoards(self._tempBoard, self._board)
                            botCancel = True
                        else:
                            print("Current board layout is incorrect")
                            input()
        self._winner = Player('')
        for player in self._players:
            if player._points > self._winner._points:
                self._winner = player
            elif player._points == self._winner._points:
                self._winner._points = 0
        self.displayFinalPoints()


scrabble = Game()
scrabble.play()
