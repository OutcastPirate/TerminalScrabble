from field import Field, CharacterError, FieldError
from pytest import raises


def test_Field():
    a1 = Field()
    assert a1.letter is not None
    assert a1._bonus is not True


def test_CharacterError():
    a1 = Field()
    with raises(CharacterError):
        a1.setLetter('.')


def test_FieldError():
    a1 = Field()
    a1.setLetter("A")
    with raises(FieldError):
        a1.setLetter("B")
