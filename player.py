from random import sample
from settings import basicTileNumber


class Player:
    def __init__(self, name):
        self._name = name
        self._points = 0
        self._tiles = []
        self._tileLetters = []

    def getStartingTiles(self, tiles):
        self._tiles = sample(tiles, basicTileNumber)
        for tile in self._tiles:
            tiles.remove(tile)
        self.updateLetters()

    def swapTiles(self, positions, tiles):
        tempTiles = sample(tiles, len(positions))
        for i in range(len(positions)):
            del self._tiles[int(positions[i]) - 1 - i]
        for tile in tempTiles:
            self._tiles.append(tile)
            tiles.remove(tile)
        self.updateLetters()

    def reloadTiles(self, tiles):
        tempTiles = sample(tiles, (basicTileNumber - len(self._tiles)))
        for tile in tempTiles:
            self._tiles.append(tile)
        for tile in tempTiles:
            tiles.remove(tile)
        self.updateLetters()

    def updateLetters(self):
        self._tileLetters = []
        for i in range(basicTileNumber):
            self._tileLetters.append(self._tiles[i]._letter)
