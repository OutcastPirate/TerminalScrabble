from board import Board
import settings
from colors import Color
from fieldLetters import fieldLet
from board import BoardError
from tiles import tiles
from player import Player


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
        self._tempBoard.insertHorizontal(content, position)
        if not self._tempBoard.validateBoard():
            raise BoardError(f"{content} on {position} does not match board")
            # print(f"{content} on {position} does not match current board")
        else:
            self._board.insertHorizontal(content, position)

    def verticalWord(self, content, position):
        self._tempBoard.insertVertical(content, position)
        if not self._tempBoard.validateBoard():
            raise BoardError(f"{content} on {position} does not match board")
            # print(f"{content} on {position} does not match current board")
        else:
            self._board.insertVertical(content, position)

    def printBoard(self):
        for i in range(settings.boardSize+1):
            print(f'{Color.BOLD}{i}{Color.ENDC}', end="\t")
        print('\n')
        for i in range(settings.boardSize):
            print(f'{Color.BOLD}{fieldLet(i+1)}{Color.ENDC}', end="\t")
            for field in self.gameBoard.getBoard()[i]:
                if field.letter == '▢':
                    print(f'{Color.RED}{field.letter}{Color.ENDC}', end='\t')
                else:
                    print(f'{Color.GRE}{field.letter}{Color.ENDC}', end='\t')
            print('\n')

    def play(self):
        for player in self.players:
            player.getStartingTiles(self._tiles)
        gameInProgress = True
        playerIndex = 0
        turnIndex = 0
        while (gameInProgress):
            currentPlayer = self._players[playerIndex]
            print(f'{len(self._tiles)} tiles left in the bag.')
            print(f"{currentPlayer._name}'s turn")
            print(f'Your tiles: {currentPlayer._tileLetters}')
            while True:
                turn = input("Choose a move => (s)-swap  (p)-place: ")
                if turn == 's':
                    print("Format: '1,2,3' -> swap the first three tiles")
                    chosen = input("Wchich tiles do you want to swap: ")
                    positions = chosen.split(',')
                    for number in positions:
                        number = int(number)
                    currentPlayer.swapTiles(positions, self._tiles)
                    print(f'Your new tiles: {currentPlayer._tileLetters}')
                    break
                if turn == 'p':
                    word = input("Choose tiles / word: ")
                    word = word.upper()
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
                                currentPlayer.reloadTiles(self._tiles)
                                counter += 1

                        if counter == len(word):
                            break
                    row = input("Choose row: ")
                    column = int(input("Choose column: "))
                    position = (row, column)
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
                    self.printBoard()
                    break
                else:
                    print("Wrong move, choose again: ")

            playerIndex = (playerIndex + 1) % len(self.players)
            turnIndex += 1
            if turnIndex == 10:
                gameInProgress = False
            print('\n' + " - " * 20 + "\n")


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
