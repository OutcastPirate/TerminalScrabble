from field import Field, CharacterError
from pytest import raises


def test_Field():
    a1 = Field()
    assert a1.letter is not None
    assert a1._bonus is not True


def test_Field_Error():
    a1 = Field()
    with raises(CharacterError):
        a1.setLetter('.')
