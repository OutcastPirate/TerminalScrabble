from tileTable import tileTable
from tile import Tile
tiles = []

tileKeys = tileTable.keys()


for key in tileKeys:
    for i in range(tileTable[key]):
        tiles.append(Tile(key))

print(tiles)
