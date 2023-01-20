from game import Game
from board import Board, BoardError
from player import Player
from pytest import raises
from checkDict import createDict
from field import FieldError
from tile import Tile, TileError
from copy import copy
from testSettings import BSIZE
from fieldLetters import fieldLet


def test_gameInit():
    scrabble = Game()
    assert isinstance(scrabble._board, Board)


def test_gameBoard():
    scrabble = Game()
    assert scrabble._board == scrabble.gameBoard


def test_gameAddPlayer():
    scrabble = Game()
    Jack = Player("Jack")
    scrabble.addPlayer(Jack)
    assert Jack in scrabble._players


def test_gameAddPlayerError():
    scrabble = Game()
    with raises(ValueError):
        scrabble.addPlayer('Jack')


def test_gameRemovePlayer():
    scrabble = Game()
    Jack = Player("Jack")
    scrabble.addPlayer(Jack)
    scrabble.removePlayer(Jack)
    assert Jack not in scrabble._players


def test_gameRemovePlayerError():
    scrabble = Game()
    Jack = Player("Jack")
    with raises(ValueError):
        scrabble.removePlayer(Jack)


def test_players():
    scrabble = Game()
    Jack = Player("Jack")
    Julie = Player("Annabeth")
    scrabble.addPlayer(Jack)
    scrabble.addPlayer(Julie)
    assert scrabble.players == [Jack, Julie]


def test_verticalWord():
    scrabble = Game()
    word = "ŁOŚ"
    position = ('H', 8)
    scrabble.verticalWord(word, position)
    assert scrabble.checkNewWords() == ["ŁOŚ"]


def test_verticalWordFail():
    scrabble = Game()
    word = "ŁOŚ"
    position = ('H', 8)
    scrabble.verticalWord(word, position)
    secondWord = "KOT"
    secondPos = ('J', 8)
    with raises(FieldError):
        scrabble.verticalWord(secondWord, secondPos)


def test_horizontalWord():
    scrabble = Game()
    word = "ŻABA"
    position = ('H', 8)
    scrabble.horizontalWord(word, position)
    assert scrabble.checkNewWords() == ["ŻABA"]


def test_horizontalWordFail():
    scrabble = Game()
    word = "ZEBRA"
    position = ('H', 8)
    scrabble.horizontalWord(word, position)
    secondWord = "PIES"
    secondPos = ('H', 11)
    with raises(FieldError):
        scrabble.horizontalWord(secondWord, secondPos)


def test_cancelTurn():
    scrabble = Game()
    word = "ŻABA"
    position = ('H', 8)
    Jack = Player("Jack")
    scrabble.horizontalWord(word, position)
    scrabble._cancelTurn = {'tiles': copy(Jack._tiles)}
    scrabble.cancelMoveTurn(Jack)
    assert scrabble.checkNewWords() == []


def test_placeTilesTurnLetters():
    scrabble = Game()
    word = "ŻABA"
    position = ('H', 8)
    Jack = Player("Jack")
    createDict()
    Jack._tiles = [
        Tile('Ż'),
        Tile('A'),
        Tile('B'),
        Tile('A'),
        Tile('U'),
        Tile('E'),
        Tile('O')
    ]
    Jack.updateLetters()
    scrabble.placeTilesTurn(Jack, word, position, 'right')
    Jack.updateLetters()
    assert 'Ż' not in Jack._tileLetters


def test_placeTilesTurnWord():
    scrabble = Game()
    word = "KROWA"
    position = ('H', 8)
    Jack = Player("Jack")
    createDict()
    Jack._tiles = [
        Tile('K'),
        Tile('A'),
        Tile('R'),
        Tile('W'),
        Tile('O'),
        Tile('E'),
        Tile('B')
    ]
    Jack.updateLetters()
    scrabble.placeTilesTurn(Jack, word, position, 'right')
    Jack.updateLetters()
    assert 'KROWA' in scrabble.checkNewWords()


def test_insertNotConnected():
    scrabble = Game()
    word = "KROWA"
    position = ('H', 8)
    Jack = Player("Jack")
    createDict()
    Jack._tiles = [
        Tile('K'),
        Tile('A'),
        Tile('R'),
        Tile('W'),
        Tile('O'),
        Tile('E'),
        Tile('B')
    ]
    Jack.updateLetters()
    scrabble.placeTilesTurn(Jack, word, position, 'right')
    assert Jack._tileLetters == ['E', 'B']


def test_checkNewWords():
    scrabble = Game()
    scrabble.horizontalWord("ŻABA", ('H', 8))
    scrabble.verticalWord("RKA", ('I', 9))
    scrabble.horizontalWord("ONIK", ('J', 10))
    assert scrabble.checkNewWords() == ['ŻABA', 'KONIK', 'ARKA']


def test_endTurnFail():
    scrabble = Game()
    word = "PIYES"
    position = ('H', 8)
    Jack = Player("Jack")
    scrabble.horizontalWord(word, position)
    createDict()
    with raises(BoardError):
        scrabble.endTurn(Jack)


def test_turnBackBoards():
    scrabble = Game()
    scrabble.horizontalWord("ŻABA", ('H', 8))
    scrabble.verticalWord("RKA", ('I', 9))
    scrabble.horizontalWord("ONIK", ('J', 10))
    scrabble.turnBoards(scrabble._tempBoard, scrabble._board)
    assert scrabble.checkNewWords() == []


def test_confirmBoard():
    scrabble = Game()
    scrabble.horizontalWord("ŻABA", ('H', 8))
    scrabble.verticalWord("RKA", ('I', 9))
    scrabble.horizontalWord("ONIK", ('J', 10))
    scrabble.turnBoards(scrabble._board, scrabble._tempBoard)
    assert scrabble._tempBoard.getBoardWords() == ['ŻABA', 'KONIK', 'ARKA']


def test_endTurnPoints():
    createDict()
    scrabble = Game()
    Julie = Player('Julie')
    scrabble.addPlayer(Julie)
    scrabble._currentPlayer = Julie
    scrabble.horizontalWord("ŻABA", ('H', 8))
    scrabble.endTurn(scrabble._currentPlayer)
    assert Julie._points == 10


def test_endTurnPlayerIndex():
    createDict()
    scrabble = Game()
    Julie = Player('Julie')
    Jack = Player('Jack')
    scrabble.addPlayer(Julie)
    scrabble.addPlayer(Jack)
    scrabble._currentPlayer = Julie
    scrabble.horizontalWord("WRONA", ('H', 8))
    scrabble.endTurn(scrabble._currentPlayer)
    assert scrabble._playerIndex == 1


def test_endTurnPlayerTurnCouter():
    createDict()
    scrabble = Game()
    Julie = Player('Julie')
    Jack = Player('Jack')
    scrabble.setGameVariables()
    scrabble.addPlayer(Julie)
    scrabble.addPlayer(Jack)
    scrabble._currentPlayer = Julie
    scrabble.horizontalWord("WRONA", ('H', 8))
    scrabble.endTurn(scrabble._currentPlayer)
    scrabble._currentPlayer = Jack
    scrabble.endTurn(scrabble._currentPlayer)
    assert scrabble._turnIndex == 3


def test_noReload():
    scrabble = Game()
    word = "WRONA"
    position = ('H', 8)
    Julie = Player("Julie")
    scrabble.addPlayer(Julie)
    scrabble._currentPlayer = Julie
    createDict()
    Julie._tiles = [
        Tile('W'),
        Tile('R'),
        Tile('B'),
        Tile('A'),
        Tile('O'),
        Tile('E'),
        Tile('N')
    ]
    Julie.updateLetters()
    scrabble.placeTilesTurn(Julie, word, position, 'right')
    assert len(Julie._tiles) == 2


def test_endTurnTiles():
    scrabble = Game()
    word = "WRONA"
    position = ('H', 8)
    Julie = Player("Julie")
    scrabble.addPlayer(Julie)
    scrabble._currentPlayer = Julie
    createDict()
    Julie._tiles = [
        Tile('W'),
        Tile('R'),
        Tile('B'),
        Tile('A'),
        Tile('O'),
        Tile('E'),
        Tile('N')
    ]
    Julie.updateLetters()
    scrabble.placeTilesTurn(Julie, word, position, 'right')
    scrabble.endTurn(scrabble._currentPlayer)
    assert len(Julie._tiles) == 7


def test_notMatchingTiles():
    scrabble = Game()
    word = "RAVEN"
    position = ('H', 8)
    Julie = Player("Julie")
    scrabble.addPlayer(Julie)
    scrabble._currentPlayer = Julie
    Julie._tiles = [
        Tile('W'),
        Tile('R'),
        Tile('B'),
        Tile('A'),
        Tile('O'),
        Tile('E'),
        Tile('N')
    ]
    Julie.updateLetters()
    with raises(TileError):
        scrabble.placeTilesTurn(Julie, word, position, 'right')


def test_occupiedTile():
    scrabble = Game()
    word = "WRONA"
    position = ('H', 8)
    Julie = Player("Julie")
    scrabble.addPlayer(Julie)
    scrabble._currentPlayer = Julie
    Julie._tiles = [
        Tile('W'),
        Tile('R'),
        Tile('B'),
        Tile('A'),
        Tile('O'),
        Tile('E'),
        Tile('N')
    ]
    Julie.updateLetters()
    scrabble.placeTilesTurn(Julie, word, position, 'right')
    with raises(FieldError):
        scrabble.placeTilesTurn(Julie, 'EB', position, 'right')


def test_outOfBounds():
    scrabble = Game()
    word = "WRONA"
    position = ('H', 8)
    Julie = Player("Julie")
    Jack = Player("Jack")
    scrabble.addPlayer(Julie)
    scrabble.addPlayer(Jack)
    scrabble._currentPlayer = Julie
    Julie._tiles = [
        Tile('W'),
        Tile('R'),
        Tile('B'),
        Tile('A'),
        Tile('O'),
        Tile('E'),
        Tile('N')
    ]
    Jack._tiles = [
        Tile('W'),
        Tile('R'),
        Tile('B'),
        Tile('A'),
        Tile('O'),
        Tile('E'),
        Tile('N')
    ]
    Julie.updateLetters()
    scrabble.placeTilesTurn(Julie, word, position, 'right')
    coords = (fieldLet(BSIZE-2), BSIZE)
    with raises(TileError):
        scrabble.placeTilesTurn(Jack, 'WRONA', coords, 'right')


def test_winner():
    scrabble = Game()
    Julie = Player('Julie')
    Jack = Player('Jack')
    scrabble.setGameVariables()
    scrabble.addPlayer(Julie)
    scrabble.addPlayer(Jack)
    Julie._points = 10
    Jack._points = 40
    scrabble.setWinner()
    assert scrabble._winner == Jack


def test_winnerDraw():
    scrabble = Game()
    Julie = Player('Julie')
    Jack = Player('Jack')
    scrabble.setGameVariables()
    scrabble.addPlayer(Julie)
    scrabble.addPlayer(Jack)
    Julie._points = 711
    Jack._points = 711
    scrabble.setWinner()
    assert scrabble._winner is None


def test_endgameCheck():
    scrabble = Game()
    Ginny = Player('Ginny')
    Jack = Player('Jack')
    scrabble.setGameVariables()
    scrabble.addPlayer(Ginny)
    scrabble.addPlayer(Jack)
    scrabble.setGameVariables()
    scrabble._tiles = []
    scrabble.checkGameEnd()
    assert scrabble._ENDGAME is True


def test_endgameCheckFalse():
    scrabble = Game()
    Ginny = Player('Ginny')
    Jack = Player('Jack')
    scrabble.setGameVariables()
    scrabble.addPlayer(Ginny)
    scrabble.addPlayer(Jack)
    scrabble.setGameVariables()
    scrabble.checkGameEnd()
    assert scrabble._ENDGAME is not True


def test_preparePlayerCheckPlayer():
    scrabble = Game()
    Ginny = Player('Ginny')
    Jack = Player('Jack')
    scrabble.setGameVariables()
    scrabble.addPlayer(Ginny)
    scrabble.addPlayer(Jack)
    scrabble.setGameVariables()
    scrabble._playerIndex = 0
    scrabble.preparePlayer()
    assert scrabble._currentPlayer == Ginny


def test_preparePlayerCheckBotControl():
    scrabble = Game()
    Ginny = Player('Ginny')
    Jack = Player('Jack')
    scrabble.setGameVariables()
    scrabble.addPlayer(Ginny)
    scrabble.addPlayer(Jack)
    scrabble.setGameVariables()
    scrabble._playerIndex = 0
    scrabble.preparePlayer()
    assert scrabble._botCancel is False


def test_preparePlayerCheckEndTurn():
    scrabble = Game()
    Violet = Player('Violet')
    Jack = Player('Jack')
    scrabble.setGameVariables()
    scrabble.addPlayer(Violet)
    scrabble.addPlayer(Jack)
    scrabble._playerIndex = 0
    scrabble.preparePlayer()
    assert scrabble._endTurn is False


def test_verifyEndTurnSkipped():
    scrabble = Game()
    Violet = Player('Violet')
    scrabble.setGameVariables()
    scrabble.addPlayer(Violet)
    scrabble._playerMoveCounter = 1
    scrabble.verifyEndTurn()
    assert scrabble._turnsSkipped == 1


def test_verifyEndTurn():
    scrabble = Game()
    scrabble.setGameVariables()
    Violet = Player('Violet')
    scrabble.addPlayer(Violet)
    scrabble._playerMoveCounter = 2
    scrabble.verifyEndTurn()
    assert scrabble._turnsSkipped == 0


def test_defineBotTurnPlace():
    scrabble = Game()
    scrabble._playerMoveCounter = 1
    assert scrabble.defineBotTurn() == 'p'


def test_defineBotTurnEnd():
    scrabble = Game()
    scrabble._playerMoveCounter = 2
    assert scrabble.defineBotTurn() == 'e'


def test_defineBotTurnCancel():
    scrabble = Game()
    scrabble._playerMoveCounter = 9
    scrabble._botCancel = True
    assert scrabble.defineBotTurn() == 'c'
