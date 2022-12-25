from tileTable import tileTable
from settings import boardCharacter


class CharacterError(ValueError):
    pass


class FieldError(ValueError):
    pass


class Field:
    def __init__(self, bonus=False):
        self._letter = boardCharacter
        self._bonus = bonus

    @property
    def letter(self):
        return self._letter

    def setLetter(self, letter):
        if self._letter == boardCharacter or self._letter == letter:
            if letter in tileTable.keys():
                self._letter = letter
            else:
                raise CharacterError('Not all symbols are accepted letters')
        else:
            raise FieldError("Word doesn't match the letters on the board")
