from board import (
    Board,
    BoardError,
    NotConnectedError
    )
from settings import boardSize as BSIZE
from pytest import raises
from random import choice
from field import FieldError
from checkDict import createDict


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
    board.insertHorizontal(word, ("H", 8), reference)
    assert word in board.getBoardWords()[0]


def test_disconnectedHorizontalStart():
    board = Board()
    reference = Board()
    word = "SLOWO"
    with raises(NotConnectedError):
        board.insertHorizontal(word, ("A", 8), reference)


def test_insertVertical():
    board = Board()
    reference = Board()
    word = "SLOWO"
    board.insertVertical(word, ("H", 8), reference)
    assert word in board.getBoardWords()[0]


def test_disconnectedVerticalStart():
    board = Board()
    reference = Board()
    word = "SLOWO"
    with raises(NotConnectedError):
        board.insertVertical(word, ("A", 8), reference)


def test_insertOutOfBounds():
    board = Board()
    reference = Board()
    word = "SLOWO"
    with raises(IndexError):
        board.insertVertical(word, ("A", BSIZE + 1), reference)


def test_insertHorizontalOutOfBounds():
    board = Board()
    reference = Board()
    word = "SLOWO"
    with raises(IndexError):
        board.insertHorizontal(word, ("A", BSIZE - 3), reference)


def test_insertOccupied():
    board = Board()
    reference = Board()
    word = "SLOWO"
    board.insertVertical(word, ("H", 8), reference)
    secondWord = "DRUGIE"
    with raises(FieldError):
        board.insertHorizontal(secondWord, ("H", 8), reference)


def test_insertConnected():
    board = Board()
    reference = Board()
    word = "SLOWO"
    board.insertVertical(word, ("H", 8), reference)
    secondWord = "PAĆ"
    board.insertHorizontal(secondWord, ("H", 9), reference)
    assert "SPAĆ" in board.getBoardWords()


def test_emptyBoardValidation():
    board = Board()
    assert board.validateBoard() is True


def test_oneWordBoardValidation():
    board = Board()
    reference = Board()
    createDict()
    word = "SŁOWO"
    board.insertVertical(word, ("H", 8), reference)
    assert board.validateBoard() is True


def test_multiWordBoardValidation():
    board = Board()
    reference = Board()
    createDict()
    word = "SŁOWO"
    board.insertVertical(word, ("H", 8), reference)
    secondWord = "PAĆ"
    board.insertHorizontal(secondWord, ("H", 9), reference)
    thirdWord = "MA"
    board.insertVertical(thirdWord, ("I", 11), reference)
    assert board.validateBoard() is True


def test_failedBoardValidation():
    board = Board()
    reference = Board()
    createDict()
    word = "GHYUHD"
    board.insertVertical(word, ("H", 8), reference)
    assert board.validateBoard() is False


def test_disconnectedVertical():
    board = Board()
    reference = Board()
    word = "SLOWO"
    board.insertVertical(word, ("H", 8), reference)
    secondWord = "JELEŃ"
    with raises(NotConnectedError):
        board.insertVertical(secondWord, ("A", 3), reference)


def test_disconnectedHorizontal():
    board = Board()
    reference = Board()
    word = "SLOWO"
    board.insertVertical(word, ("H", 8), reference)
    secondWord = "JELEŃ"
    with raises(NotConnectedError):
        board.insertHorizontal(secondWord, ("A", 3), reference)