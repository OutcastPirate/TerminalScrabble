from bot import Bot
from tile import Tile
from checkDict import createDict
from board import Board
from game import Game
from player import Player


def test_checkOwnWords():
    createDict()
    Optimus = Bot('Optimus')
    Optimus._tiles = [
        Tile('B'),
        Tile('A'),
        Tile('L'),
        Tile('A'),
        Tile('O'),
        Tile('E'),
        Tile('N')
    ]
    Optimus.updateLetters()
    assert "BALON" in Optimus.checkOwnWords()


def test_bestWord():
    createDict()
    Optimus = Bot('Optimus')
    scrabble = Board()
    referenceBoard = Board()
    Optimus._tiles = [
        Tile('B'),
        Tile('A'),
        Tile('L'),
        Tile('A'),
        Tile('O'),
        Tile('E'),
        Tile('N')
    ]
    Optimus.updateLetters()
    Optimus.makeMove(scrabble, referenceBoard)
    assert Optimus._moves[0][0][1:] == "BALON"
    assert "BALON" in Optimus.checkOwnWords()


def test_verticalMove():
    createDict()
    Optimus = Bot('Optimus')
    scrabble = Board()
    referenceBoard = Board()
    scrabble.insertHorizontal("BANAN", ('H', 8), referenceBoard)
    Optimus._tiles = [
        Tile('B'),
        Tile('A'),
        Tile('L'),
        Tile('A'),
        Tile('O'),
        Tile('E'),
        Tile('N')
    ]
    Optimus.updateLetters()
    Optimus.makeMove(scrabble, referenceBoard)
    assert ['BALON', 8, (8, 7), 'down'] in Optimus._moves


def test_horizontalMove():
    createDict()
    Optimus = Bot('Optimus')
    scrabble = Board()
    referenceBoard = Board()
    scrabble.insertVertical("BANAN", ('H', 8), referenceBoard)
    Optimus._tiles = [
        Tile('N'),
        Tile('A'),
        Tile('L'),
        Tile('K'),
        Tile('R'),
        Tile('O'),
        Tile('N')
    ]
    Optimus.updateLetters()
    Optimus.makeMove(scrabble, referenceBoard)
    assert ['NORKA', 6, (9, 8), 'right'] in Optimus._moves


def test_reverseHorizontalMove():
    createDict()
    Optimus = Bot('Optimus')
    scrabble = Board()
    referenceBoard = Board()
    scrabble.insertVertical("BANAN", ('H', 8), referenceBoard)
    Optimus._tiles = [
        Tile('N'),
        Tile('A'),
        Tile('L'),
        Tile('K'),
        Tile('R'),
        Tile('O'),
        Tile('N')
    ]
    Optimus.updateLetters()
    Optimus.makeMove(scrabble, referenceBoard)
    assert [' NORK', 6, (8, 3), 'right'] in Optimus._moves


def test_reverseVerticalMove():
    createDict()
    Optimus = Bot('Optimus')
    scrabble = Board()
    referenceBoard = Board()
    scrabble.insertHorizontal("PTAKI", ('H', 8), referenceBoard)
    Optimus._tiles = [
        Tile('W'),
        Tile('I'),
        Tile('L'),
        Tile('K'),
        Tile('R'),
        Tile('O'),
        Tile('N')
    ]
    Optimus.updateLetters()
    Optimus.makeMove(scrabble, referenceBoard)
    assert [' WILK', 7, (3, 11), 'down'] in Optimus._moves


def test_invertedVerMoveWordCheck():
    createDict()
    Optimus = Bot('Optimus')
    Jack = Player('Jack')
    scrabble = Game()
    Jack._tiles = [
        Tile('P'),
        Tile('T'),
        Tile('A'),
        Tile('K'),
        Tile('I'),
        Tile('O'),
        Tile('N')
    ]
    Optimus._tiles = [
        Tile('W'),
        Tile('I'),
        Tile('L'),
        Tile('K'),
        Tile('R'),
        Tile('O'),
        Tile('N')
    ]
    Optimus.updateLetters()
    Jack.updateLetters()
    scrabble.addPlayer(Jack)
    scrabble.addPlayer(Optimus)
    scrabble.setGameVariables()
    scrabble._currentPlayer = Jack
    scrabble.placeTilesTurn(Jack, "PTAKI", ('H', 8), 'right')
    scrabble.endTurn(Jack)
    Optimus._moves = [[' WILK', 7, (3, 11), 'down']]
    scrabble.placeTilesTurn(Optimus, 'a', 'b', 'down')
    assert "WILKI" in scrabble._tempBoard.getBoardWords()
