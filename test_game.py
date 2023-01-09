from game import Game
from board import Board, BoardError
from player import Player
from pytest import raises
from checkDict import createDict
from field import FieldError
from tile import Tile


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


def test_gameRemovePlayer():
    scrabble = Game()
    Jack = Player("Jack")
    scrabble.addPlayer(Jack)
    scrabble.removePlayer(Jack)
    assert Jack not in scrabble._players


def test_players():
    scrabble = Game()
    Jack = Player("Jack")
    Violet = Player("Violet")
    scrabble.addPlayer(Jack)
    scrabble.addPlayer(Violet)
    assert scrabble.players == [Jack, Violet]


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
    position = ('A', 8)
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
    position = ('A', 8)
    Jack = Player("Jack")
    scrabble.horizontalWord(word, position)
    scrabble.cancelMoveTurn(Jack, Jack._tiles)
    assert scrabble.checkNewWords() == []


def test_placeTilesTurnLetters():
    scrabble = Game()
    word = "ŻABA"
    position = ('A', 8)
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


def test_checkNewWords():
    pass


def test_endTurnFail():
    scrabble = Game()
    word = "PIYES"
    position = ('A', 8)
    Jack = Player("Jack")
    scrabble.horizontalWord(word, position)
    createDict()
    with raises(BoardError):
        scrabble.endTurn(Jack)


def test_turnBackBoards():
    pass


def test_confirmBoard():
    pass


def test_endTurn():
    pass
