from bot import Bot
from tile import Tile
from checkDict import createDict
from board import Board


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
    assert Optimus._moves[0][0][1:] == " BALON"
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
