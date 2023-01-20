# LAUNCHING THE GAME

    Launch possibilities:
        1. Running 'startGame.py' file while inside it
        2. launch with 'python3 startGame.py' in terminal while inside 'pythonscrabble' folder

    To propely launch the game with code:
        - initiate an instance 'Scrabble' class located in startGame.py file
        - initiate play() function on previously created instance of the Scrabble class

    ! - The game should be started with the console in fullscreen mode in order to prevent incorrect display.

    ! - Changing certain settings will result in the game not starting properly (see 'Main files and their content / Config files' chapter)

    Sample code for starting up the game is already included in startGame.py file, running it will also begin the game.

# Additional corrections and decisions made during the project:

    - the player will not receive points for creating a word that is already on the board
        (second instance of the same word)
    - there have to be at least 2 players for the game to start
    - maximum number of players in game is 4
        * - adding more players would result in limited possibilities of creating words and distributing tiles

# Main files and their content

## Main files
    - game.py => main game logic and backend functions
    - startGame.py => interface file with its logic and functions

## Classes
    - Player:
        • file: player.py
        • Includes all functions dealing with player's tiles distribution
    - Bot:
        • file: bot.py
        • Includes all functions dealing with bot's move making decision
        • Is a child class of Player
    - Board:
        • file: board.py
        • Includes functions dealing with board layout and validation
    - Tile:
        • file: tile.py
        • Includes functions dealing with single tile's properties and changes
    - Field:
        • file: field.py
        • Includes functions used to modify a single board field
    - Game:
        • file: game.py
        • Includes main game logic and backend functions
    - Scrabble:
        • file: startGame.py
        • Includes all interface functions

## Config files

    Settings are located in the settings.py file.
    Those include:
        • boardSize -> the number of rows and columns on the board
                ? - standard value = 15, lowest possible value = 15 (Smaller boards wouldn't make sense)
                ! - ALWAYS has to be an odd number for the game to work, if set to an even value the game won't start
                !! - Changing this setting is not recommended as it may interfere with the game's original purpose
                * changing this to one bigger than 15 may result in wrong display on monitors smaller than 17 inches

        • wordsDict -> location of the game dictionary with all accepted words
        • basicTileNumber -> Number of tiles assigned to each player
                ? - standard value = 7
        • boardCharacter - purely cosmetic, changes what the board field looks like without any letters assigned to it
                ! - some suggested symbols might not display properly on all devices and terminal versions
        • maxWordLength - maximum length of a word that will be accepted and awarded with points
                ? - standard value compatibile with project assigment content -> 5

    Additional configuration files include:
        - tileTable.py -> The type and amount of available tiles (originally sums to 100 tiles total)
        - pointTable.py -> Amount of points awarded for using each letter in a word

# GAME

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


    Illegal moves:
    - placing tiles on tiles already occupied
    - placing tiles out of bounds of the board
    - placing first tile outside of the middle field

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

        It is important to stick to the assigned format (indexes separated with commas).
        If put into any other format the program will reject the input and ask the player to make his move again


### Skipping a turn

    If a player chooses 'e' as their move their turn is skipped with no consequences.

    However, if all players skip their turns twice in a row (in example: there are 4 players and there were 8 consequtive turn skips) the game ends.

## GAME END

    There are two possibilities to end the game

        - all player's skipped two turns back to back (see 'Game'/'Main Game Course'/'Skipping a turn' Chapter)

        - there are no tiles left in the bag and one whole turn has passed
            (if the player who ends each turn depletes the bag the game ends, if not one more turn is played)

