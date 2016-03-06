# Daniel Gold (46043649)
# ICS 32 - Project #4: Othello (Part I) -- Now being used for project #5 Othello (Part II)

# This module contains classes and functions which handle the rules/logic of Othello.

# A note on game board orientation: I mixed up my x and y axises and somehow managed to code this entire module all the
# way through to completion without realizing it. And I'll be damned if I'm going to go back and change it now, so
# if you just swap x and y in your head as well, everything should make a lot more sense. To put it another way,
# the rows of the game board (which you would expect to be referred to via the Y axis) are referred to via 'x', while
# columns are referred to via 'y'

# Also, while I'm talking about this, it's worth mentioning that the vertical axis of the game board is referenced with
# the top being 0 or 1, rather than the bottom as one might expect. The horizontal axis is referred to with 0 or 1 being
# to the left as one would expect.


B = 1  # Constant
W = 2  # Constant
DIRECTIONS = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']  # Constant (directions of the compass)


class OthelloLogicError(Exception):
    def __init__(self, value: int = 0):
        self.value = value


class InvalidPlayerError(OthelloLogicError):
    """To be raised when the value for which player is being referred to is neither 1 (B), 2 (W), or 0 (blank). May
    also be raised if blank player is not valid for the specific operation. See __str__ for details."""

    def __str__(self):
        if self.value == 0:
            return 'Values for \'player\' must be either 1 (B), 2 (W), or 0 (blank).'
        if self.value == 1:
            return 'Values for \'player\' must be either 1 (B), 2 (W), or 0 (blank). \n' \
                   'However, the player specified for this operation may not be blank.'


class IllegalMoveError(Exception):
    """
    To be raised when the specified Othello move is illegal or impossible.
    """


class BoardDimensionError(Exception):
    """
    To be raised when the game board is or would be too large or too small, or has or would have an odd number of
    rows or columns.
    """


class CorruptBoardError(Exception):
    """
    Raise if any of the rows or columns in the board become longer or shorter than their initial length, or if any
    of them go missing or become otherwise mixed up in a way that would disrupt the program ability to use them.
    """


class GameOver(OthelloLogicError):
    """
    Raise when the game has ended. See __str__ for explanations of values that can be passed with raise. If no value is
    passed, then the value is 0.
    """

    def __str__(self):
        if self.value == 0:
            return 'The game ended unexpectedly.'
        if self.value == 1:
            return 'No valid move exists for either player.'


class BoardModificationError(OthelloLogicError):
    def __str__(self):
        if self.value == 0:
            return 'The program may have modified the game board in an illegal way. The integrity ' \
                   'of the game can no longer be guaranteed. '
        if self.value == 1:
            return 'The program attempted to modify the game board in an illegal way, but was ' \
                   'stopped from doing so.'


class GameBoard:
    def __init__(self, rows: int, cols: int):
        """
        Takes in as arguments the number of rows and number of columns that the game board should have, then generates
        the nested list which will house our board data with all spaces beginning with a value of '0'. The board must
        have an even number of rows and columns. It must also be no smaller than 4x4 and no larger than 16x16.
        :param rows: The number of rows that the game board should have
        :param cols: Short for columns. The number of columns the game board should have
        """

        # Establish the number of rows and columns as constants within the class object, check that they're valid
        self.ROWS = rows
        self.COLS = cols

        if rows % 2 != 0 or cols % 2 != 0:
            raise BoardDimensionError('Number of rows and number of columns must both be even numbers.')
        if rows < 4 or rows > 16 or cols < 4 or cols > 16:
            raise BoardDimensionError('The number of each for both rows and columns must be between 4 and 16')

        # Create a blank game board
        self.board = []

        for i in range(rows):
            column = []

            for h in range(cols):
                column.append(0)

            self.board.append(column)

        # Find the center 4 tiles of the board and save them as a list of coordinate dictionaries
        self.center_4 = [{'x': self.ROWS // 2 - 1, 'y': self.COLS // 2 - 1},
                         {'x': self.ROWS // 2, 'y': self.COLS // 2 - 1},
                         {'x': self.ROWS // 2 - 1, 'y': self.COLS // 2}, {'x': self.ROWS // 2, 'y': self.COLS // 2}]

        self.validate_board()

    def modify_board(self, cds: dict, player: int):
        """
        Modifies self.board by changing a single tile to hold a particular player's piece.
        WARNING: This method should never be used by itself to make a move in the game since it does not perform any
        checks against the legality of its modification to the board.
        :param cds: The specific tile on the board to be modified.
        :param player: The player who's piece will be placed on that tile.
        """

        self.board[cds['x']][cds['y']] = player

    def validate_board(self):
        try:
            assert len(self.board) == self.ROWS

            for i in range(len(self.board)):
                assert len(self.board[i]) == self.COLS
        except AssertionError:
            raise CorruptBoardError

    def __getitem__(self, key):
        return self.board[key]

    def __len__(self):
        return len(self.board)

    def __eq__(self, other):
        try:
            return self.board == other.board
        except AttributeError:
            return False

    def set_board(self, player: int):
        """
        Places the initial four pieces on the center of the board with either W or B in the upper left position.
        :param player: Either 1 (black) or 2 (white)
        """

        if player < 1 or player > 2:
            raise InvalidPlayerError

        self.modify_board(self.center_4[0], player)
        player = change_player(player)
        self.modify_board(self.center_4[1], player)
        self.modify_board(self.center_4[2], player)
        player = change_player(player)
        self.modify_board(self.center_4[3], player)


class GameState:
    """
    Contains a GameBoard as well as information on who's turn it is and what the score is.
    """

    def __init__(self, rows: int, cols: int, first: int, ne_player: int, win: str):
        self.board = GameBoard(rows, cols)
        self.turn = first
        self.center_4 = self.board.center_4

        self.board.set_board(ne_player)

        if win != '>' and win != '<':
            raise ValueError('{0} is not a valid win condition. Acceptable values are \'>\' for "the player with\n'
                             'the most discs on the board at the end of the game wins" or \'<\' for "the player\n'
                             'with the fewest discs on the board at the end of the game wins"'.format(win))
        else:
            self.win = win

    def player_score(self, player: int):
        """
        Returns the number of tiles owned by the player.
        :param player: 1 or 2. 0 to see number of blank tiles.
        """
        return len(self.player_tiles(player))

    def change_to_next_turn(self):
        """
        Changes self.turn to the opposite player, unless that player would have no valid moves. Returns the new value
        of self.turn.
        :return: Player integer. Or None, if no player has a valid move.
        """

        blank_tiles = self.player_tiles(0)

        if not len(blank_tiles):
            raise GameOver(1)

        for tile in blank_tiles:
            if self.is_legal_move(tile, change_player(self.turn)):
                self.turn = change_player(self.turn)
                return self.turn

        for tile in self.player_tiles(0):
            if self.is_legal_move(tile, self.turn):
                return self.turn

        raise GameOver(1)

    def make_move(self, tile: dict, player: int = None):
        """
        Calls various relevant functions to change ownership of the specified blank tile to the specified player, then
        change ownership of any other tiles that that move can legally flip. Then changes self.player to reflect that it
        is the next player's turn.
        :param tile: The tile that a piece will be placed on.
        :param player: Who will own that piece. This should normally left blank to allow the GameState object to simply
        supply the player who's turn it currently is.
        :return: Nothing is returned. The self.board is modified in place.
        """

        if player is None:
            player = self.turn

        if not self.is_legal_move(tile, player):
            raise IllegalMoveError

        self._propagate_move(tile, player)

    def _propagate_move(self, origin: dict, aggressor: int):
        """
        Modifies a GameBoard object to reflect the consequences of placing a particular tile. IE: Places a new tile,
        then flips all other occupied tiles which must legally be flipped.
        Note: This function should never be called without the result of is_legal_move first.
        :param origin: Tile upon which the new piece will be placed.
        :param aggressor: Player who will own the new piece.
        :return: Nothing is returned as the GameBoard object is modified in place.
        """

        if aggressor < 1 or aggressor > 2:
            raise InvalidPlayerError(1)

        self.board.modify_board(origin, aggressor)

        for direction in DIRECTIONS:
            if self._is_legal_slice(aggressor, self._get_slice(origin, direction)):
                self._crawl_slice(origin, direction)

    def is_legal_move(self, tile: dict, player: int) -> bool:
        """
        Checks if a move would be legal.
        :param tile: Which tile the new piece would be placed on.
        :param player: Which player would own the piece begin placed.
        :return: True if the move would be valid. False if the move would not be valid.
        """

        if self.board[tile['x']][tile['y']] != 0:
            return False

        if tile['x'] > self.board.ROWS or tile['x'] < 0:
            return False
        if tile['y'] > self.board.COLS or tile['y'] < 0:
            return False

        for direction in DIRECTIONS:
            if self._is_legal_slice(player, self._get_slice(tile, direction)):
                return True

        return False

    def player_tiles(self, player: int) -> [dict]:
        """
        Returns a list of all occupied tiles for a particular player, given the current GameBoard state. For all open
        tiles simply pass 0 for player.
        :param player: The player (1 or 2) who's tiles we want to find, or 0 to find blank tiles
        :return: A list containing dictionaries of 1 x and 1 y coordinate for each tile matching the player parameter
        """

        matching_tiles = []

        for x in range(self.board.ROWS):
            for y in range(self.board.COLS):
                if self.board[x][y] == player:
                    matching_tiles.append({'x': x, 'y': y})

        return matching_tiles

    def _is_legal_slice(self, aggressor: int, d_slice: [dict]) -> bool:
        """
        Returns whether or not placing a piece belonging to aggressor on the tile specified by origin could legally
        affect other pieces in the particular slice.
        :param aggressor: Player who would own the tile referenced by d_slice[0]
        :param d_slice: List of tile dictionaries describing a slice of the the game board from an origin tile to the
        edge of the board in a particular direction.
        :return: True if applying the value of aggressor to d_slice[0] could legally affect any other part of the slice.
        """

        for i in range(2, len(d_slice)):
            current_tile = d_slice[i]
            last_tile = d_slice[i - 1]
            if self.board[last_tile['x']][last_tile['y']] == aggressor:
                return False
            elif self.board[current_tile['x']][current_tile['y']] == aggressor and \
                            self.board[last_tile['x']][last_tile['y']] == change_player(aggressor):
                return True
            elif self.board[current_tile['x']][current_tile['y']] == 0 or \
                            self.board[last_tile['x']][last_tile['y']] == 0:
                return False
            elif self.board[current_tile['x']][current_tile['y']] == change_player(aggressor) and \
                            self.board[last_tile['x']][last_tile['y']] == change_player(aggressor):
                continue
            else:
                raise CorruptBoardError('The program encountered a tile value which should not exist.')
        return False

    def _crawl_slice(self, origin: dict, direction: str):
        """
        Increments along a 'slice' or list of tiles going in a particular direction away from the origin tile. Each tile
        following the origin tile changes ownership to the opposite player until a tile is found that is already owned
        by the same player as the origin tile. Note that this function should only be called after the origin tile has
        been modified to reflect new ownership. Attempting to call this function on a blank tile will simply result in
        an error.
        :param origin: Dictionary of 'x' and 'y' coordinate of a tile in the diagonal you want to look at
        :param direction: Compass direction to generate slice from. Either n, ne, e, se, sw, w, or nw
        :return: Nothing is returned as the GameBoard object is modified in place.
        """

        c_slice = self._get_slice(origin, direction)

        aggressor = self.board[c_slice[0]['x']][c_slice[0]['y']]
        if aggressor == 0:
            raise BoardDimensionError(1)

        for t in c_slice[1:]:
            if self.board[t['x']][t['y']] == aggressor:
                return

            elif self.board[t['x']][t['y']] == 0:
                raise BoardModificationError(0)

            elif self.board[t['x']][t['y']] == change_player(aggressor):
                self.board[t['x']][t['y']] = aggressor

    def _get_slice(self, origin: dict, direction: str) -> [dict]:
        """
        Returns a list of tiles in a diagonal on the game board
        :param origin: Dictionary of 'x' and 'y' coordinate of a tile in the diagonal you want to look at
        :param direction: Compass direction to generate slice from. Either n, ne, e, se, sw, w, or nw
        :return: A list of tile x/y coordinate dictionaries containing all tiles between the specified one and the edge
        of the board (inclusive of the original tile).
        """

        board_slice = [origin]

        temp_tile = origin

        while True:
            temp_tile = self._get_adjacent(temp_tile, direction)
            if temp_tile is not None:
                board_slice.append(temp_tile)
            else:
                return board_slice

    def _get_adjacent(self, tile: dict, direction: str) -> dict:
        """
        Returns the tile adjacent to the specified tile, using the specified direction.
        :param tile: The tile that you want to find a tile adjacent to.
        :param direction: Compass direction in which to look for adjacent tile (north = up). Must be one of these:
        'n' (north), 'ne' (north-east), 'e' (east), 'se' (southeast), 's' (south), 'sw' (south-west), 'w' (west),
        'nw' (north-west)
        :return: tile dictionary with one 'x' coordinate and one 'y' coordinate, or None if the tile doesn't exist
        """

        if len(direction.strip()) > 1:  # If direction will be a diagonal, call the function we already have for that.
            new_tile = self._diag_by_one(tile, direction)
        elif direction == 'n':
            new_tile = {'x': tile['x'], 'y': tile['y'] - 1}
        elif direction == 'e':
            new_tile = {'x': tile['x'] + 1, 'y': tile['y']}
        elif direction == 's':
            new_tile = {'x': tile['x'], 'y': tile['y'] + 1}
        elif direction == 'w':
            new_tile = {'x': tile['x'] - 1, 'y': tile['y']}
        else:
            raise ValueError("'{0}' is not a valid direction. Must use one of the following:\n "
                             "'n' (north), 'ne' (north-east), 'e' (east), 'se' (southeast), 's' (south), 'sw' "
                             "(south-west),\n 'w' (west), 'nw' (north-west)".format(direction))

        if new_tile['x'] > self.board.ROWS - 1 or new_tile['x'] < 0:
            return None
        elif new_tile['y'] > self.board.COLS - 1 or new_tile['y'] < 0:
            return None
        else:
            return new_tile

    @staticmethod
    def _diag_by_one(tile: dict, direction: str) -> dict:
        """
        Returns a tile diagonally adjacent to the the specified tile in the specified direction.
        :param tile: The tile we already know the coordinates
        :param direction: Direction we want to look in for the next tile. Options: 'nw' (up and to the left), 'sw' (down
        and to the left), 'ne' (up and to the right), 'se' (down and to the right).
        :return: A dictionary is the same form as the tile input containing the coordinates to the tile found in the
        specified direction. Or 'None' if there is no tile in that direction.
        """

        if direction == 'nw':
            new_tile = {'x': tile['x'] - 1, 'y': tile['y'] - 1}
        elif direction == 'ne':
            new_tile = {'x': tile['x'] + 1, 'y': tile['y'] - 1}
        elif direction == 'sw':
            new_tile = {'x': tile['x'] - 1, 'y': tile['y'] + 1}
        elif direction == 'se':
            new_tile = {'x': tile['x'] + 1, 'y': tile['y'] + 1}
        else:
            raise ValueError("'{0}' is not a valid direction. Must use one of the following:\n "
                             "'nw' (up and to the left), 'sw' (down and to the left), 'ne' (up and to the right), 'se' "
                             "(down and to the right)".format(direction))

        return new_tile


def encode_coordinates(x: int, y: int) -> dict:
    """
    Translates coordinates (starting at 1) to list index values (starting at 0)
    :param x: Row number
    :param y: Column number
    :return: Dictionary of 'x' and 'y' list indices for self.board.
    """

    return {'x': x - 1, 'y': y - 1}


def change_player(player: int) -> int:
    """
    Whichever player is entered, the opposite player is returned.
    :param player: Either 1 (which is B) or 2 (which is W)
    """
    if player == 1:
        return 2
    elif player == 2:
        return 1
    else:
        raise InvalidPlayerError(1)
