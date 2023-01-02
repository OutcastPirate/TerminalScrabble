from tile import Tile
from pointTable import pointTable


def test_create_tile():
    zTile = Tile('Z')
    assert zTile._letter == 'Z'


def test_tile_points():
    zTile = Tile('Z')
    assert zTile._points == pointTable['Z']
