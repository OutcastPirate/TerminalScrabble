from game import Game
from board import Board
from player import Player
# from io import StringIO


def test_gameInit():
    scrabble = Game()
    assert isinstance(scrabble.gameBoard, Board)


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


# def test_swapTiles(monkeypatch):
#     scrabble = Game()
#     Jack = Player("Jack")
#     Jack.getStartingTiles(scrabble._tiles)
#     position = StringIO('1\n')
#     monkeypatch.setattr('sys.stdin', position)
#     prevTile = Jack._tiles[0]
#     scrabble.swapTilesTurn(Jack)
#     assert prevTile != Jack._tiles[0]
