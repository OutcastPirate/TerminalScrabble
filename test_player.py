from player import Player, TileError
from tile import Tile
from pytest import raises
from copy import copy

testTiles = [
        Tile('A'),
        Tile('B'),
        Tile('C'),
        Tile('D'),
        Tile('E'),
        Tile('F'),
        Tile('G')
    ]

swapTiles = [
        Tile('H'),
        Tile('I')
    ]


def test_create_player():
    Jack = Player('Jack')
    assert Jack._name == 'Jack'


def test_player_points():
    Jack = Player('Jack')
    assert Jack._points == 0


def test_player_getTiles():
    Jack = Player('Jack')
    Jack.getStartingTiles(copy(testTiles))
    assert sorted(Jack._tileLetters) == ['A', 'B', 'C', 'D', 'E', 'F', 'G']


def test_check_tiles_swap(monkeypatch):

    def getTiles(tiles, amount):
        tempTiles = []
        for i in range(amount):
            tempTiles.append(tiles[i])
        return tempTiles

    monkeypatch.setattr('player.sample', getTiles)
    Jack = Player('Jack')
    Jack.getStartingTiles(copy(testTiles))
    Jack.swapTiles(['1', '2'], copy(swapTiles))
    assert Jack._tileLetters == ['C', 'D', 'E', 'F', 'G', 'H', "I"]


def test_check_tiles_swap_Error(monkeypatch):

    def getTiles(tiles, amount):
        tempTiles = []
        for i in range(amount):
            tempTiles.append(tiles[i])
        return tempTiles

    monkeypatch.setattr('player.sample', getTiles)
    Jack = Player('Jack')
    Jack.getStartingTiles(copy(testTiles))
    with raises(TileError):
        Jack.swapTiles(['1', '2', '3'], copy(swapTiles))


def test_give_player_points():
    Jack = Player('Jack')
    Jack.givePoints(['KAKTUS'])
    assert Jack._points == 11
