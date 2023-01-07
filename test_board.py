from board import (
    Board,
    BoardError,
    WrongWordError,
    NotConnectedError
    )
from settings import boardSize as BSIZE
from pytest import raises
from random import choice


def test_boardInit():
    board = Board()
    assert board._size == BSIZE


def test_boardInitError(monkeypatch):
    boardSizeTest = 8
    monkeypatch.setattr('board.boardSize', boardSizeTest)
    with raises(BoardError):
        Board()


def test_boardInitRows():
    board = Board()
    assert len(board._fields) == BSIZE


def test_boardInitFields():
    board = Board()
    chooseRow = choice(range(BSIZE))
    assert len(board._fields[chooseRow]) == BSIZE


def test_insertHorizontal():
    board = Board()
    reference = Board()
    word = "SLOWO"
    board.insertHorizontal(word, ("A", 1), reference)
    assert word in board.getBoardWords()[0]


def test_insertVertical():
    board = Board()
    reference = Board()
    word = "SLOWO"
    board.insertVertical(word, ("A", 1), reference)
    assert word in board.getBoardWords()[0]


def test_insertOccupied():
    board = Board()
    reference = Board()
    word = "SLOWO"
    with raises(WrongWordError):
        board.insertVertical(word, ("A", BSIZE + 1), reference)
