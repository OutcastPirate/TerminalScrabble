# main files and their content

    - game.py => main game logic and backend functions
    - startGame.py => interface file with its logic and functions

## Game Start

After launching 'startGame.py' file the user is presented with a starting screen with option selection:
    - add Player
    - add Bot
    - delete Player
    - start Game

Basic rules:
    - user has to add at least 2 players/bots in order to begin the game
    - there cannot be more than 4 players
    - players and bots are deleted using their nametag
    - both bots' and players' names have to be unique


## Main Game course

    At the beggining of the game, each player is assigned 7 letter tiles from the tiles' pool.
    The amount of letters on tiles and points assigned to them are as follows:

        1 point: A (x9), E (x8), I (x8), N (x5), O (x7), R (x4), S (x4), W (x4), Z (x5)
        2 points: C (x3), D (x3), K(x3), L(x3), M(x3), P (x3), T (x3), Y (x4)
        3 points: B (x2), G(x2), H(x2), J (x2), Ł (x2), U (x2)
        5 points: Ą (x1), Ę (x1), F (x1), Ó (x1), Ś (x1), Ż (x1)
        6 points: Ć (x1)
        6 points: Ć (x1)
        7 points: Ń (x1)
        9 points: Ź (x1)

    The total number of letter tiles is 100.

    After getting their tiles, the first player is presented with 3 options of making a move:
        - placing tiles on the board
        - swapping his tiles (swapping tiles doesn't count as skipping a turn)
        - skipping his turn

    If the player has already placed some tiles on the board, the last option changes
        from skipping a turn, to cancelling his tile placement on the board.


### Placing tiles

    If the player opts to place his tiles on the board, he chooses 'p' as his move option.

    The board has rows and columns, rows are described with letters starting with 'A' and columns have numbers assigned to them starting with '1'.

    The player is asked to input the beggining coordinates of his tile placement and tiles he wants to place.

    If the player opts to input multiple tiles at once, he specifies the direction with the format of coordinated input:
        - selecting the row first, for example 'H 8' and numerous tiles will result in placing them to the right, starting with field
        "H8" and then placing next letters at "H9" "H10"...
        - selecting the column first, for example '8 H' and multiple tiles will respectivly place them downwards, starting with field
        "H8" and then at "I8" "J8"...
        - while placing only one tile the format of the input doesn't matter


### Swapping tiles

    If the player chooses to swap their tiles, he inputs 's'.

    The player can swap tiles at any point of the game, as long as there are enough tiles for him to swap left in the tiles' pool.

    The tiles which he swaps are put to the side, he is assigned random new tiles from the pool and his old tiles are put back in the pool.

    Swapping tiles does not count as skipping a turn and can be done any number of times during the game.

    If the player chooses this option he uses his move to ONLY swap his tiles and cannot place any tiles on the board after that.

    While swapping tiles the player is asked to input indexes of the tiles he wishes to swap

    For example:

        If the player tiles are as follows ['A', 'B', 'C', 'D', 'E', 'F', 'G']

        And he inputs 3,4,7

        Tiles 'C', 'D' and 'G' will be swapped.

        It is important to stick to the assigned format (indexes separated with commas), if put into any other format the program will reject the input and ask the player to make his move again


### Skipping a turn

    If a player chooses 'e' as their move their turn is skipped with no consequences.

    However, if all players skip their turns twice in a row (in example: there are 4 players and there were 8 consequtive turn skips) the game ends.

## GAME END

    There are two possibilities to end the game

        - all player's skipped two turns back to back [link](#main-game-course)