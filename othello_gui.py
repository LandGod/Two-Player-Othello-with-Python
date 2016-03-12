# Daniel Gold (46043649)
# ICS 32 - Project #5: Othello (Part II)

# This is the main gui module which will run the Othello program and harness other modules such as othello_logic
# and point.

import othello_logic
import othello_configure
import point
from point import Point
import tkinter

DEFAULT_FONT = ('Helvetica', 12)
TITLE_FONT = ('Helvetica', 18)
SUBTITLE_FONT = ('Helvetica', 16)


class UserQuit(Exception):
    """To be thrown when the user elects to quit the program."""


class OthelloApplication:

    def __init__(self):

        self._state = None
        self._debug = False

        self._root_window = tkinter.Tk()

        self._root_window.wm_title("[FULL] Othello")

        self._score = tkinter.StringVar(self._root_window)

        self._score_board = tkinter.Label(master=self._root_window, textvariable=self._score, width=800,
                                          font=TITLE_FONT)
        self._score_board.grid(row=0, column=0, padx=10, pady=5, sticky=tkinter.N + tkinter.E + tkinter.W)

        self._board_canvas = tkinter.Canvas(master=self._root_window, width=800, height=800, background='#00802b')

        self._board_canvas.grid(row=1, column=0, padx=10, pady=10, sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        self._turn = tkinter.StringVar()
        self._turn.set('Turn: NONE')

        self._turn_label = tkinter.Label(master=self._root_window, textvariable=self._turn,
                                         font=TITLE_FONT)
        self._turn_label.grid(row=2, column=0, padx=10, pady=5, sticky=tkinter.S + tkinter.E + tkinter.W)

        self._root_window.rowconfigure(0, weight=0)
        self._root_window.rowconfigure(1, weight=1)
        self._root_window.rowconfigure(2, weight=0)
        self._root_window.columnconfigure(0, weight=1)

        self._root_window.bind('<Configure>', self._root_window.geometry("800x800"))

        startup = othello_configure.StartupDialog()
        startup.show()

        if not startup.was_ok_clicked():
            raise UserQuit

        self._state = othello_logic.GameState(startup.rows(), startup.cols(), startup.first(), startup.ne_player(),
                                              startup.win())

        self._update_turn_label()

        self._quadrant_size = (1 / self._state.board.COLS, 1 / self._state.board.ROWS)

        geo_string = '{}x{}'.format(int(self._state.board.COLS * 100), int(self._state.board.ROWS * 100))

        self._root_window.bind('<Configure>', self._root_window.geometry(geo_string))

        self._canvas_width = self._board_canvas.winfo_width()
        self._canvas_height = self._board_canvas.winfo_height()

        self._board_point_index = self._create_board_point_index()

        self._root_window.after(50, self._root_window.lift())

        self._draw_board()

        self._draw_all_pieces()

        self._update_score()

        self._root_window.bind('<Configure>', self._root_window.after(50, self._root_window.lift))

        self._board_canvas.bind('<Configure>', self._on_canvas_resized)
        self._board_canvas.bind('<Button-1>', self._on_canvas_clicked)
        self._board_canvas.bind('<Button-3>', self._on_canvas_right_clicked)

    def start(self):

        self._root_window.mainloop()

    def _on_canvas_resized(self, event:tkinter.Event):

        self._update_canvas_size()

        self._redraw_all()

    def _on_canvas_clicked(self, event: tkinter.Event):

        if self._debug:
            self._debug_mode_clicked(event)
            return

        self._board_canvas.config(background='#00802b')
        self._update_canvas_size()
        click_location = point.from_pixel(event.x, event.y, self._canvas_width, self._canvas_height)
        previous_turn = self._state.turn

        click_was_in = None, None

        for y in range(self._state.board.ROWS):
            for x in range(self._state.board.COLS):
                if self._is_in_quadrant(self._board_point_index[y][x], click_location):
                    click_was_in = y, x

        if None in click_was_in:
            return
        else:
            try:
                self._state.make_move({'x': click_was_in[0], 'y': click_was_in[1]})
            except othello_logic.IllegalMoveError:
                return
            else:
                self._redraw_all()
                try:
                    self._state.change_to_next_turn()
                except othello_logic.GameOver:
                    game_over = GameOverPopup(self._decide_winner())
                    game_over.show()
                    self._root_window.destroy()
                else:
                    self._update_turn_label()
                    if self._state.turn == previous_turn:
                        warning = NoMovePopup(previous_turn)
                        warning.show()

    def _on_canvas_right_clicked(self, event: 'Tkinter Event'):
        pop_up = DebugPopup(self._debug)
        pop_up.show()
        self._debug = pop_up.get()
        if self._debug:
            self._board_canvas.config(background='pink')
            self._root_window.wm_title("[FULL] Othello -- !!DEBUG MODE ENABLED!!")
        else:
            self._board_canvas.config(background='#00802b')
            self._root_window.wm_title("[FULL] Othello")
        self._root_window.lift()

    def _redraw_all(self):
        """Delete and re-draw all elements on the canvas"""

        self._board_canvas.delete(tkinter.ALL)
        self._draw_board()
        self._draw_all_pieces()
        self._update_score()

    def _draw_board(self):
        """Draws the game board."""

        # Vertical lines
        for x in range(self._state.board.COLS - 1):
            x += 1
            a, b = Point(self._quadrant_size[0] * x, 0).pixel(self._canvas_width, self._canvas_height)
            c, d = Point(self._quadrant_size[0] * x, 1).pixel(self._canvas_width, self._canvas_height)

            self._board_canvas.create_line(a, b, c, d)

        # Horizontal lines
        for y in range(self._state.board.ROWS - 1):
            y += 1
            a, b = Point(0, self._quadrant_size[1] * y).pixel(self._canvas_width, self._canvas_height)
            c, d = Point(1, self._quadrant_size[1] * y).pixel(self._canvas_width, self._canvas_height)

            self._board_canvas.create_line(a, b, c, d)

    def _draw_piece(self, p: Point, color: str):
        """Draws a piece, either black or white, at the specified location"""

        x, y = p.frac()

        a = x - (self._quadrant_size[0] / 2 - (self._quadrant_size[0] - 0.01))
        b = y + (self._quadrant_size[1] / 2 - (self._quadrant_size[1] - 0.01))
        c = x + (self._quadrant_size[0] / 2 - (self._quadrant_size[0] - 0.01))
        d = y - (self._quadrant_size[1] / 2 - (self._quadrant_size[1] - 0.01))

        a, b = Point(a, b).pixel(self._canvas_width, self._canvas_height)
        c, d = Point(c, d).pixel(self._canvas_width, self._canvas_height)

        self._board_canvas.create_oval(a, b, c, d, outline='gray', fill=color, width=2)

    def _draw_all_pieces(self):
        """Draws all pieces present in the game state"""
        for y in range(self._state.board.ROWS):
            for x in range(self._state.board.COLS):

                if self._state.board[y][x] == 0:
                    continue
                elif self._state.board[y][x] == 1:
                    self._draw_piece(self._board_point_index[y][x], 'black')
                elif self._state.board[y][x] == 2:
                    self._draw_piece(self._board_point_index[y][x], 'white')
                else:
                    raise othello_logic.CorruptBoardError

    def _create_board_point_index(self):
        """Creates a nested list of Points, which corresponds to an othello_logic.GameBoard object."""

        index = []

        for y in range(self._state.board.ROWS):
            row_index = []

            y_coordinate = self._quadrant_size[1] / 2 + y * self._quadrant_size[1]

            for x in range(self._state.board.COLS):
                x_coordinate = self._quadrant_size[0] / 2 + x * self._quadrant_size[0]

                row_index.append(Point(x_coordinate, y_coordinate))

            index.append(row_index)

        return index

    def _update_canvas_size(self):
        """Updates the width and height variables for the class based on the actual current canvas size."""
        self._canvas_width = self._board_canvas.winfo_width()
        self._canvas_height = self._board_canvas.winfo_height()

    def _is_in_quadrant(self, quadrant: Point, click: Point):
        quadrant_upper_x = quadrant.frac()[0] + self._quadrant_size[0] / 2
        quadrant_lower_x = quadrant.frac()[0] - self._quadrant_size[0] / 2
        quadrant_upper_y = quadrant.frac()[1] + self._quadrant_size[1] / 2
        quadrant_lower_y = quadrant.frac()[1] - self._quadrant_size[1] / 2

        click_x, click_y = click.frac()

        return quadrant_lower_x < click_x < quadrant_upper_x and quadrant_lower_y < click_y < quadrant_upper_y

    def _update_score(self):
        """Updates the tkinter.StringVar variable with a formatted text string containing the current score."""""
        self._score.set('Black: {}   |   White: {}'.format(self._state.player_score(1), self._state.player_score(2)))

    def _debug_mode_clicked(self, event: tkinter.Event):
        self._update_canvas_size()
        click_location = point.from_pixel(event.x, event.y, self._canvas_width, self._canvas_height)

        click_was_in = None, None

        for y in range(self._state.board.ROWS):
            for x in range(self._state.board.COLS):
                if self._is_in_quadrant(self._board_point_index[y][x], click_location):
                    click_was_in = y, x

        if None in click_was_in:
            return
        else:
            occupier = self._state.board[click_was_in[0]][click_was_in[1]]
            if occupier <= 1:
                player = occupier + 1
            else:
                player = 0

            self._state.board.modify_board({'y': click_was_in[1], 'x': click_was_in[0]}, player)

        self._redraw_all()

    def _decide_winner(self):
        if self._state.player_score(1) > self._state.player_score(2):
            if self._state.win == '>':
                return 1
            else:
                return 2
        elif self._state.player_score(1) == self._state.player_score(2):
            return 0
        else:
            if self._state.win == '>':
                return 2
            else:
                return 1

    def _update_turn_label(self):
        if self._state.turn == 1:
            self._turn.set('Turn: Black')
        elif self._state.turn == 2:
            self._turn.set('Turn: White')


class GameOverPopup:
    def __init__(self, winner):
        if winner == 1:
            winner = 'Black'
        elif winner == 2:
            winner = 'White'
        elif winner == 0:
            winner = None
        else:
            raise othello_logic.InvalidPlayerError

        self._pop_up = tkinter.Toplevel()
        self._pop_up.wm_title("GAME OVER")

        self._pop_up.bind('<Configure>', self._pop_up.after(10, self._pop_up.lift))
        self._pop_up.geometry("240x110")
        if winner is not None:
            self._win_label = tkinter.Label(master=self._pop_up, text='{} is the winner!'.format(winner),
                                            font=TITLE_FONT)
        else:
            self._win_label = tkinter.Label(master=self._pop_up, text='TIE!', font=TITLE_FONT)
        self._win_label.grid(row=0, column=0, padx=10, pady=10, sticky=tkinter.N + tkinter.S + tkinter.E + tkinter. W)

        quit_button = tkinter.Button(master=self._pop_up, text='Quit', font=SUBTITLE_FONT,
                                     command=self._on_quit_click)

        quit_button.grid(row=1, column=0, padx=10, pady=10, sticky=tkinter.N + tkinter.S + tkinter.E + tkinter. W)

        self._pop_up.rowconfigure(0, weight=1)
        self._pop_up.columnconfigure(0, weight=1)

        self._pop_up.bind('<Configure>', lambda event: None)

    def _on_quit_click(self):
        self._pop_up.destroy()

    def show(self):
        self._pop_up.grab_set()
        self._pop_up.wait_window()


class NoMovePopup:
    def __init__(self, player):
        if player == 1:
            player = 'Black'
        elif player == 2:
            player = 'White'
        else:
            raise othello_logic.InvalidPlayerError

        self._pop_up = tkinter.Toplevel()
        self._pop_up.wm_title("[FULL] Othello")

        self._pop_up.bind('<Configure>', self._pop_up.after(10, self._pop_up.lift))
        self._pop_up.geometry("300x150")

        self._text = tkinter.Label(master=self._pop_up, text='{} has no valid moves.\nTheir turn will be skipped.'.
                                   format(player), font=TITLE_FONT)
        self._text.grid(row=0, column=0, padx=10, pady=10, sticky=tkinter.N + tkinter.S + tkinter.E + tkinter. W)

        okay_button = tkinter.Button(master=self._pop_up, text='Okay', font=SUBTITLE_FONT,
                                     command=self._on_okay_click)

        okay_button.grid(row=1, column=0, padx=10, pady=10, sticky=tkinter.N + tkinter.S)

        self._pop_up.rowconfigure(0, weight=1)
        self._pop_up.columnconfigure(0, weight=1)

        self._pop_up.bind('<Configure>', lambda event: None)

    def _on_okay_click(self):
        self._pop_up.destroy()

    def show(self):
        self._pop_up.grab_set()
        self._pop_up.wait_window()


class DebugPopup:
    def __init__(self, current_value: bool):
        self._pop_up = tkinter.Toplevel()
        self._pop_up.wm_title("Debug")

        self._pop_up.bind('<Configure>', self._pop_up.after(10, self._pop_up.lift))

        self._debug_label = tkinter.Label(master=self._pop_up, text='Enable Debug Mode?', font=DEFAULT_FONT)
        self._debug_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self._debug_value = tkinter.BooleanVar()

        self._debug_on = tkinter.Radiobutton(master=self._pop_up, text='Enabled', variable=self._debug_value,
                                             value=True, indicatoron=0, font=SUBTITLE_FONT, width=14)
        self._debug_on.grid(row=1, column=0, columnspan=2, padx=5, pady=0)

        self.debug_off = tkinter.Radiobutton(master=self._pop_up, text='Disabled', variable=self._debug_value,
                                             value=False, indicatoron=0, font=SUBTITLE_FONT, width=14)
        self.debug_off.grid(row=2, column=0, columnspan=2, padx=5, pady=0)

        self._debug_value.set(current_value)

    def get(self):
        return self._debug_value.get()

    def show(self):
        self._pop_up.grab_set()
        self._pop_up.wait_window()

if __name__ == '__main__':
    try:
        OthelloApplication().start()
    except UserQuit:
        pass
