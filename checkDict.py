# -*- coding: utf-8 -*-
from tileTable import tileTable
from settings import WORDSDICT, MAXWORDLENGTH

newDict = {}


def createDict():
    for key in tileTable.keys():
        newDict[key] = []
    with open(WORDSDICT, 'r', encoding="utf-8") as fileHandle:
        fileHandle.readline()
        for line in fileHandle:
            line = line.rstrip()
            if len(line) <= MAXWORDLENGTH:
                newDict[line[0].upper()].append(line)


def getWords(letter):
    letter = letter.upper()
    return newDict[letter]
