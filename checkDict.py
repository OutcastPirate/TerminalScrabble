# -*- coding: utf-8 -*-
from tileTable import tileTable
from settings import wordsDict, maxWordLength

newDict = {}


def createDict():
    for key in tileTable.keys():
        newDict[key] = []
    with open(wordsDict, 'r', encoding="utf-8") as fileHandle:
        fileHandle.readline()
        for line in fileHandle:
            line = line.rstrip()
            if len(line) <= maxWordLength:
                newDict[line[0].upper()].append(line)


def getWords(letter):
    letter = letter.upper()
    return newDict[letter]
