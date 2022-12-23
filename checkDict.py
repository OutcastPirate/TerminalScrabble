# -*- coding: utf-8 -*-

from settings import wordsDict


def getWords(letter):
    words = []
    with open(wordsDict, 'r', encoding="utf-8") as fileHandle:
        fileHandle.readline()
        for line in fileHandle:
            line = line.rstrip()
            if len(line) <= 5 and line[0] == letter:
                words.append(line)
    return words


# print(getWords('a'))
