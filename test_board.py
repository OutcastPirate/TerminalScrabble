from board import (
    Board,
    BoardError,
    WrongWordError
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
    board.insertHorizontal(word, ("A", 1), reference)
    assert word in board.getBoardWords()[0]


def test_insertVertical():
    board = Board()
    reference = Board()
    word = "SLOWO"
    board.insertVertical(word, ("A", 1), reference)
    assert word in board.getBoardWords()[0]


def test_insertOutOfBounds():
    board = Board()
    reference = Board()
    word = "SLOWO"
    with raises(WrongWordError):
        board.insertVertical(word, ("A", BSIZE + 1), reference)


def test_insertOccupied():
    board = Board()
    reference = Board()
    word = "SLOWO"
    board.insertVertical(word, ("A", 1), reference)
    secondWord = "DRUGIE"
    with raises(FieldError):
        board.insertHorizontal(secondWord, ("A", 1), reference)


def test_insertConnected():
    board = Board()
    reference = Board()
    word = "SLOWO"
    board.insertVertical(word, ("A", 1), reference)
    secondWord = "PAĆ"
    board.insertHorizontal(secondWord, ("A", 2), reference)
    assert "SPAĆ" in board.getBoardWords()


def test_emptyBoardValidation():
    board = Board()
    assert board.validateBoard() is True


def test_oneWordBoardValidation():
    board = Board()
    reference = Board()
    createDict()
    word = "SŁOWO"
    board.insertVertical(word, ("A", 1), reference)
    assert board.validateBoard() is True


def test_multiWordBoardValidation():
    board = Board()
    reference = Board()
    createDict()
    word = "SŁOWO"
    board.insertVertical(word, ("A", 1), reference)
    secondWord = "PAĆ"
    board.insertHorizontal(secondWord, ("A", 2), reference)
    thirdWord = "MA"
    board.insertVertical(thirdWord, ("B", 4), reference)
    assert board.validateBoard() is True


def test_failedBoardValidation():
    board = Board()
    reference = Board()
    createDict()
    word = "GHYUHD"
    board.insertVertical(word, ("A", 1), reference)
    assert board.validateBoard() is False
