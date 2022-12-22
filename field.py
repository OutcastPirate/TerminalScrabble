class CharacterError(ValueError):
    pass


class Field:
    def __init__(self, bonus=False):
        self._letter = '▢'
        self._bonus = bonus

    @property
    def letter(self):
        return self._letter

    def setLetter(self, letter):
        if ord(letter) > 64 and ord(letter) < 91:
            self._letter = letter
        else:
            raise CharacterError('Not all symbols are accepted letters')
