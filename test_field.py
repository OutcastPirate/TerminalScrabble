from field import Field, CharacterError, FieldError
from testSettings import boardCharacter as BCHAR
from pytest import raises


def test_field_init_letter():
    field = Field()
    assert field._letter == BCHAR


def test_letterSet():
    field = Field()
    field.setLetter('A')
    assert field._letter == 'A'


def test_letterSetError():
    field = Field()
    with raises(CharacterError):
        field.setLetter('*')


def test_letterSetOccupiedError():
    field = Field()
    field.setLetter('A')
    with raises(FieldError):
        field.setLetter('B')


def test_letter():
    field = Field()
    field.setLetter('H')
    assert field.letter == 'H'
