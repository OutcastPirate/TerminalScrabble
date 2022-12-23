from tileTable import tileTable
from tile import Tile


tileKeys = tileTable.keys()

tiles = []

for key in tileKeys:
    for i in range(tileTable[key]):
        tiles.append(Tile(key))
