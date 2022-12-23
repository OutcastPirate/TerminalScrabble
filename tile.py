from pointTable import pointTable


class Tile:
    def __init__(self, letter):
        self._letter = letter
        self._points = pointTable[letter]
