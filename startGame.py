from game import Game
from os import system, name as osName
from colors import Color as C
from board import BoardError, NotConnectedError
from player import Player
from bot import Bot
from fieldLetters import fieldLet
from checkDict import createDict
from settings import boardCharacter as BCHAR
from settings import boardSize as BSIZE
from math import floor
from board import WrongWordError
from field import FieldError
from tile import TileError


class Scrabble(Game):

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

    def displayLeaderboard(self):
        if (osName == 'posix'):
            system('clear')
        else:
            system('cls')
        print('\n')
        print(f'\t{C.BD}{C.BLU}{"Leaderboard":^30}{C.ENDC}')
        print(f'\t{C.BD}{"Player":20}{"Points":>10}{C.ENDC}')
        print("\t" + f"{C.BD}-{C.ENDC}" * 30)
        for player in self._players:
            print(f'\t{player._name:20}{player._points:>10}')
        print('\n' * 5)
        input()

    def displayFinalPoints(self):
        self.setWinner()
        if (osName == 'posix'):
            system('clear')
        else:
            system('cls')
        print('\n')
        print(f'\t{C.BD}{C.RED}{"THE GAME ENDED":^30}{C.ENDC}')
        print('\n')
        print(f'\t{C.BD}{C.BLU}{"Leaderboard":^30}{C.ENDC}')
        print(f'\t{C.BD}{"Player":20}{"Points":>10}{C.ENDC}')
        print("\t" + f"{C.BD}-{C.ENDC}" * 30)
        for player in self._players:
            print(f'\t{player._name:20}{player._points:>10}')
        print('\n' * 2)
        if self._winner is not None:
            print(f'{C.MID}{self._winner._name} won! Congratulations!{C.ENDC}')
        else:
            print(f'{C.MID}It was a draw!{C.ENDC}')
        print('\n' * 4)
        input()

    def placeTilesInput(self, currentPlayer):
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
        else:
            word = ''
            coords = ''
            direction = ''
        self.placeTilesTurn(currentPlayer, word, coords, direction)

    def placeTilesCheck(self, currentPlayer):
        try:
            self.placeTilesInput(currentPlayer)
            middle = floor(BSIZE / 2)
            if self._tempBoard.getBoard()[middle][middle]._letter == BCHAR:
                self.cancelMoveTurn(currentPlayer)
                print('\nFirst tile has to be placed on the middle field. \n')
                input()
        except IndexError:
            print("Chosen field out of bounds")
            self.cancelMoveTurn(currentPlayer)
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
            self.cancelMoveTurn(currentPlayer, self._cancelTurn['tiles'])

    def beginGame(self):
        createDict()
        players = []
        while (True):
            if (osName == 'posix'):
                system('clear')
            else:
                system('cls')
            print(f'{C.BD}{C.BLU}{"SCRABBLE":^40}{C.ENDC}\n')
            print('p - Add player')
            print('b - Add AI player (bot)')
            print('d - Delete player')
            print('s - Start Game\n')
            print(f'\t{C.BD}{C.BLU}{"Players":^20}{C.ENDC}')
            print("\t" + f"{C.BD}-{C.ENDC}" * 20)
            for index, player in enumerate(self._players):
                if isinstance(player, Bot):
                    name = player._name
                    print(f'\t{index + 1:>2}.{name:>14} {C.GRE}AI{C.ENDC}')
                else:
                    print(f'\t{index + 1:>2}.{player._name:>17}')
            print('\n' * 5)
            option = input("Choose option: ")
            if option == 'p' or option == 'b':
                if self.validatePlayerCount() == 0:
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
                if (self.validatePlayerCount() == 1):
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
        for player in self.players:
            player.getStartingTiles(self._tiles)
        self.setGameVariables()

    def swapTilesTurn(self, currentPlayer):
        print("Format: '1,2,3' -> swap the first three tiles")
        chosen = input("Wchich tiles do you want to swap: ")
        positions = chosen.split(',')
        currentPlayer.swapTiles(positions, self._tiles)
        print(f'Your new tiles: {currentPlayer._tileLetters}')
        input()

    def endTurnInterface(self):
        termOne = self._turnsSkipped == len(self._players) * 2
        if termOne or self._botEnd == 20:
            self._ENDGAME = True
        try:
            self.endTurnDisplay(self._currentPlayer)
            if self._playerIndex == 0:
                self.displayLeaderboard()
        except BoardError:
            if isinstance(self._currentPlayer, Bot):
                self.turnBoards(self._tempBoard, self._board)
                self._botEnd += 1
                self._botCancel = True
            else:
                print("Current board layout is incorrect")
                input()

    def placeTilesInterface(self):
        if isinstance(self._currentPlayer, Bot):
            self._currentPlayer.makeMove(self._tempBoard, self._board)  # noqa: E501
            if len(self._currentPlayer._moves) == 0:
                self._endTurn = True
                return
        self.placeTilesCheck(self._currentPlayer)
        if (len(self._currentPlayer._tiles) == 7):
            self.cancelMoveTurn(self._currentPlayer)

    def swapTurnInferface(self):
        try:
            self.swapTilesTurn(self._currentPlayer)
        except (ValueError, IndexError):
            print('\nWrong format of input\n')
            input()
            self.cancelMoveTurn(self._currentPlayer)
            self._playerMoveCounter = 0
            return
        self._endTurn = True

    def cancelTurnInterface(self):
        self.cancelMoveTurn(self._currentPlayer)
        self._playerMoveCounter = 0
        self._botCancel = False
        if isinstance(self._currentPlayer, Bot):
            self._playerMoveCounter = 2
            self._endTurn = True

    def startTurn(self):
        while True:
            if self._ENDGAME:
                break
            self._playerMoveCounter += 1
            if isinstance(self._currentPlayer, Bot):
                turn = self.defineBotTurn()
            elif self._endTurn:
                turn = 'e'
            elif self._playerMoveCounter == 1:
                print("Choose a move => ", end="")
                turn = input("(s)-swap    (p)-place   (e)-end turn:  ")
            else:
                print("Choose a move => ", end="")
                turn = input("(p)-place (e)-end turn (c)-cancel turn: ")
            if turn == 's' and self._playerMoveCounter == 1:
                self.swapTurnInferface()
            elif turn == 'p':
                self.placeTilesInterface()
                break
            elif turn == 'e':
                self.verifyEndTurn()
                self.endTurnInterface()
                break
            elif turn == 'c':
                self.cancelTurnInterface()
                break
            else:
                print("Wrong move, choose again: ")

    def play(self):
        self.beginGame()
        while (self._gameInProgress):
            if self._ENDGAME:
                break
            if (osName == 'posix'):
                system('clear')
            else:
                system('cls')
            self.printTempBoard()
            self.preparePlayer()
            self.checkGameEnd()
            print(f'{len(self._tiles)} tiles left in the bag.')
            print(f"{self._currentPlayer._name}'s turn")
            print(f'Your tiles: {self._currentPlayer._tileLetters}')
            self.startTurn()
        self.displayFinalPoints()

    def endTurnDisplay(self, currentPlayer):
        self.endTurn(currentPlayer)
        if isinstance(currentPlayer, Bot):
            if (osName == 'posix'):
                system('clear')
            else:
                system('cls')
            self.printTempBoard()
            input()


if __name__ == '__main__':
    scrabble = Scrabble()
    scrabble.play()
