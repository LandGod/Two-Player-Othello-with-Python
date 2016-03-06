import unittest

import othello_logic


class BoardImportError(Exception):
    """To be raised when the board import function runs across a tile that it cannot translate"""


class TestSetUpBoard(unittest.TestCase):

    def setUp(self):
        self.board_object4 = othello_logic.GameBoard(4, 4)
        self.board_object6 = othello_logic.GameBoard(6, 6)
        self.board_object10 = othello_logic.GameBoard(10, 10)
        self.board_object16 = othello_logic.GameBoard(16, 16)
        self.board_objectA = othello_logic.GameBoard(4, 16)
        self.board_objectB = othello_logic.GameBoard(16, 4)
        self.board_objectC = othello_logic.GameBoard(8, 10)

        self.all_board_objects = [self.board_object4, self.board_object6, self.board_object10, self.board_object16,
                                  self.board_objectA, self.board_objectB, self.board_objectC]

        self.all_game_objects = []

        for b in self.all_board_objects:
            x = othello_logic.GameState(b.ROWS, b.COLS, 1, 1, '>')
            x.board = b
            self.all_game_objects.append(x)

    def tearDown(self):
        self.board_object4 = None
        self.board_object6 = None
        self.board_object10 = None
        self.board_object16 = None
        self.board_objectA = None
        self.board_objectB = None
        self.board_objectC = None
        self.all_board_objects = None

    def test_instantiation(self):
        with self.assertRaises(othello_logic.BoardDimensionError):
            othello_logic.GameBoard(1, 1)
        with self.assertRaises(othello_logic.BoardDimensionError):
            othello_logic.GameBoard(0, 0)
        with self.assertRaises(othello_logic.BoardDimensionError):
            othello_logic.GameBoard(4, 3)
        with self.assertRaises(othello_logic.BoardDimensionError):
            othello_logic.GameBoard(8, 5)
        with self.assertRaises(othello_logic.BoardDimensionError):
            othello_logic.GameBoard(18, 18)

    def test_starts_blank(self):
        for b in self.all_board_objects:
            self.assertTrue(self._board_is_blank(b))

    def test_set_board_wrong(self):
        for b in self.all_board_objects:
            with self.assertRaises(othello_logic.InvalidPlayerError):
                b.set_board(0)
            with self.assertRaises(othello_logic.InvalidPlayerError):
                b.set_board(3)
            with self.assertRaises(othello_logic.InvalidPlayerError):
                b.set_board(False)
            with self.assertRaises(othello_logic.InvalidPlayerError):
                b.set_board(-1)

    def test_set_board_correctly(self):
        for i in [1, 2]:
            for b in self.all_board_objects:
                b.set_board(i)
                self.assertEqual(b.board[b.ROWS//2 - 1][b.COLS//2], othello_logic.change_player(i))
                self.assertEqual(b.board[b.ROWS//2][b.COLS//2], i)
                self.assertEqual(b.board[b.ROWS//2 - 1][b.COLS//2 - 1], i)
                self.assertEqual(b.board[b.ROWS//2][b.COLS//2 - 1], othello_logic.change_player(i))

    def test_legal_moves_on_blank_boards(self):
        for b in self.all_game_objects:
            for i in [1, 2]:
                for x in range(b.board.ROWS):
                    for y in range(b.board.COLS):
                        self.assertFalse(b.is_legal_move({'x': x, 'y': y}, i))

    def test_legal_moves_on_set_board(self):
        for player in [1, 2]:
            for b in self.all_game_objects:
                b.board.set_board(player)
                self.assertTrue(b.is_legal_move({'x': b.board.ROWS//2 - 1, 'y': b.board.COLS//2 - 2},
                                                othello_logic.change_player(player)))
                self.assertTrue(b.is_legal_move({'x': b.board.ROWS//2 + 1, 'y': b.board.COLS//2},
                                                othello_logic.change_player(player)))
                self.assertTrue(b.is_legal_move({'x': b.board.ROWS//2, 'y': b.board.COLS//2 + 1},
                                                othello_logic.change_player(player)))
                self.assertTrue(b.is_legal_move({'x': b.board.ROWS//2 - 2, 'y': b.board.COLS//2 - 1},
                                                othello_logic.change_player(player)))

                self.assertTrue(b.is_legal_move({'x': b.board.ROWS//2 - 1, 'y': b.board.COLS//2 + 1},
                                                player))
                self.assertTrue(b.is_legal_move({'x': b.board.ROWS//2 - 2, 'y': b.board.COLS//2},
                                                player))
                self.assertTrue(b.is_legal_move({'x': b.board.ROWS//2, 'y': b.board.COLS//2 - 2},
                                                player))
                self.assertTrue(b.is_legal_move({'x': b.board.ROWS//2 + 1, 'y': b.board.COLS//2 - 1},
                                                player))

                for tile in b.board.center_4:
                    self.assertFalse(b.is_legal_move(tile, player))
                    self.assertFalse(b.is_legal_move(tile, othello_logic.change_player(player)))

    def test_all_open_tiles_on_blank(self):
        for b in self.all_game_objects:
            self.assertEqual(len(b.player_tiles(0)), b.board.ROWS * b.board.COLS)

    def test_all_open_tiles_on_set(self):
        for b in self.all_game_objects:
            b.board.set_board(1)
            self.assertEqual(len(b.player_tiles(0)), b.board.ROWS * b.board.COLS - 4)

            for each in b.center_4:
                self.assertFalse(each in b.player_tiles(0))

    def _board_is_blank(self, b):
        for x in b.board:
            for y in x:
                if y != 0:
                    return False
        return True


class TestSpecificCases(unittest.TestCase):

    def test_validity_of_import_board_printout(self):
        self.assertEqual(othello_logic.GameBoard(4, 4), self.import_board_printout(self.test_case_0).board,
                         msg='Failed to import a blank board properly')

        self.assertEqual(self.import_board_printout(self.test_case_1, 2).board.board, self.test_case_1a)

    def test_testcase_1(self):
        """Attempts to reproduce illegal behavior"""

        game = self.import_board_printout(self.test_case_1, 2)
        game.make_move({'x': 4, 'y': 5})

        p_game = othello_logic.GameState(4, 4, 1, 1, '>')
        p_game.board = self.import_board_printout(self.test_case_1b, 2).board

        for y in range(len(game.board.board)):
            self.assertEqual(game.board.board[y], p_game.board.board[y], msg='Failed at index {}'.format(y))

    def test_testcase_1c(self):
        """Attempts to reproduce illegal behavior"""

        game = self.import_board_printout(self.test_case_1, 1)
        game.make_move({'x': 4, 'y': 5})

        p_game = othello_logic.GameState(4, 4, 1, 1, '>')
        p_game.board = self.import_board_printout(self.test_case_1c, 1).board

        for y in range(len(game.board.board)):
            self.assertEqual(game.board.board[y], p_game.board.board[y], msg='Failed at index {}'.format(y))

    def test_testcase_2(self):
        """Attempts to make an illegal move"""
        game = self.import_board_printout(self.test_case_4, 1)

        with self.assertRaises(othello_logic.IllegalMoveError):
            game.make_move({'x': 1, 'y': 1})

    def test_case_3(self):
        game_a = self.import_board_printout(self.tc3a, 2)
        game_a.make_move({'x': 0, 'y': 2})
        game_b = self.import_board_printout(self.tc3b)

        self.assertEqual(game_a.board, game_b.board)

    def setUp(self):

        # Test Cases:

        self.test_case_1 = ['. . W B W W',  # next_turn = W
                            'B B B B W W',  # Win = '>'
                            'B B B W W W',
                            'B W B W B W',
                            '. B W B W .',
                            '. . B B B W']

        self.test_case_1a = [[0, 0, 2, 1, 2, 2],
                             [1, 1, 1, 1, 2, 2],
                             [1, 1, 1, 2, 2, 2],
                             [1, 2, 1, 2, 1, 2],
                             [0, 1, 2, 1, 2, 0],
                             [0, 0, 1, 1, 1, 2]]

        self.test_case_1b = ['. . W B W W',  # What should happen when placing a B at '5 6' in test_case_1
                             'B B B B W W',
                             'B B B W W W',
                             'B W B W W W',
                             '. B W B W W',
                             '. . B B B W']

        self.test_case_1c = ['. . W B W W',  # What should happen when placing a B at '5 6' in test_case_1
                             'B B B B W W',
                             'B B B W W W',
                             'B W B W B W',
                             '. B W B B B',
                             '. . B B B W']

        self.test_case_0 = ['. . . .',
                            '. . . .',
                            '. . . .',
                            '. . . .']

        self.test_case_4 = ['W . . . . W',  # Next turn W
                            'W . . . . W',
                            'W B B B B W',
                            'W W W W B W',
                            'W W W B W W',
                            'B B B W W W']

        self.tc3a = ['. . . . . .',
                     '. B B B . .',
                     'W B B B B B',
                     'B W W W B B',
                     '. . W . B .',
                     '. . . . . .']

        self.tc3b = ['. . W . . .',
                     '. W W B . .',
                     'W B W B B B',
                     'B W W W B B',
                     '. . W . B .',
                     '. . . . . .']

    @staticmethod
    def import_board_printout(printout: [str], next_turn: int = 1, win: str = '>') -> othello_logic.GameState:
        """
        Here is a template for importing printed boards:
        ['',
        '',
        '',
        '']
        :param printout: List containing each row of the board as a string, just copy/pasted from a printout.
        :param next_turn: Who goes next (the integer value)
        :param win: Whether the game win state is specified by '>' or '<'. Default is '>'.
        :return: othello_logic.GameState object
        """

        for x in range(len(printout)):
            new_row = printout[x]
            new_row = new_row.strip()
            new_row = new_row.split()
            for y in range(len(new_row)):
                if new_row[y] == '.':
                    new_row[y] = 0
                elif new_row[y] == 'B':
                    new_row[y] = 1
                elif new_row[y] == 'W':
                    new_row[y] = 2
                else:
                    raise BoardImportError('{0} Is an unrecognized value and could not be imported.'.format(y))
            printout[x] = new_row

        new_state = othello_logic.GameState(len(printout), len(printout[0]), next_turn, 1, win)

        new_state.board.board = printout

        return new_state


if __name__ == '__main__':
    unittest.main()
