from tileTable import tileTable
from settings import boardCharacter


class CharacterError(ValueError):
    pass


class FieldError(ValueError):
    pass


class Field:
    def __init__(self):
        self._letter = boardCharacter

    def get_letter(self):
        return self._letter

    def setLetter(self, letter):
        if self._letter == boardCharacter or self._letter == letter:
            if letter in tileTable.keys():
                self._letter = letter
            else:
                raise CharacterError('Not all symbols are accepted letters')
        else:
            raise FieldError("Word doesn't match the letters on the board")
