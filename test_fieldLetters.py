from fieldLetters import fieldInt, fieldLet


def test_fieldInt():
    assert fieldInt('A') == 1


def testFieldLet():
    assert fieldLet(15) == 'O'
