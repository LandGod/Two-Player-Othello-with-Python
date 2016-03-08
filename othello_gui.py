# Daniel Gold (46043649)
# ICS 32 - Project #5: Othello (Part II)

# This is the main gui module which will run the Othello program and harness other modules such as othello_logic
# and point.

import othello_logic
import point
import tkinter


DEFAULT_FONT = ('Helvetica', 12)
TITLE_FONT = ('Helvetica', 18)
SUBTITLE_FONT = ('Helvetica', 16)


class UserQuit(Exception):
    """To be thrown when the user elects to quit the program."""


class UnableToIdentifyWidget(Exception):
    """To be thrown when the tkinter widget specified cannot be identified as one of the expected types by a function"""


class OthelloApplication:

    def __init__(self):
        self._state = None

        self._root_window = tkinter.Tk()

        self._root_window.wm_title("[FULL] Othello")

        self._canvas = tkinter.Canvas(master=self._root_window, width=800, height=800, background='#00802b')

        self._canvas.grid(row=0, column=0, padx=10, pady=10, sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)

        #self._canvas.bind('<Configure>', self._on_canvas_resized)
        self._canvas.bind('<Button-1>', self._on_canvas_clicked)
        self._canvas.bind('<Button-2>', self._on_canvas_right_clicked)

        self._root_window.rowconfigure(0, weight=1)
        self._root_window.columnconfigure(0, weight=1)

        startup = StartupDialog()
        startup.show()

        if not startup.validate_all:
            raise UserQuit("User x'd out of the startup dialogue.")

        state = othello_logic.GameState(startup.rows(), startup.cols(), startup.first(), startup.ne_player(),
                                        startup.win())

    def start(self):
        self._root_window.mainloop()


    def _on_canvas_resized(self):
        pass

    def _on_canvas_clicked(self):
        pass

    def _on_canvas_right_clicked(self):
        pass

    def _redraw_all(self):
        """Delete and re-draw all elements on the canvas"""

        self._canvas.delete(tkinter.ALL)

        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()

        #re-draw everything


class StartupDialog:

    def __init__(self):
        self._rows = None
        self._cols = None
        self._first = None
        self._ne_player = None
        self._win = None

        self._ok_clicked = False

        self._dialog_window = tkinter.Toplevel()

        # Windows top title (not window 'bar' title)
        prompt_label = tkinter.Label(master=self._dialog_window,
                                     text='What kind of Othello game would you like to play?', font=TITLE_FONT)
        prompt_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky=tkinter.W+tkinter.E)

        self._dialog_window.columnconfigure(0, weight=1)
        self._dialog_window.columnconfigure(1, weight=1)
        self._dialog_window.columnconfigure(2, weight=1)
        self._dialog_window.columnconfigure(3, weight=1)
        self._dialog_window.columnconfigure(4, weight=1)

        # Instructions for entering a row and column value
        row_col_label_1 = tkinter.Label(master=self._dialog_window, text='Please specify the number of rows and '
                                                                         'columns you would like to board to have.',
                                        font=DEFAULT_FONT)
        row_col_label_1.grid(row=1, column=0, columnspan=4, padx=10, pady=2, sticky=tkinter.W)
        row_col_label_2 = tkinter.Label(master=self._dialog_window, text='Each value must be an even number between 4 '
                                                                         'and 16 (inclusive).', font=DEFAULT_FONT)
        row_col_label_2.grid(row=2, column=0, columnspan=4, padx=10, pady=2, sticky=tkinter.W)

        # Row and column entry spaces with labels (both in the same row).
        # Row label
        rows_label = tkinter.Label(master=self._dialog_window, text='Rows:',
                                   font=SUBTITLE_FONT)
        rows_label.grid(row=3, column=0, padx=10, pady=5, sticky=tkinter.W)
        # Row entry box
        self._rows_entry = tkinter.Entry(master=self._dialog_window, width=10, font=SUBTITLE_FONT)
        self._rows_entry.grid(row=3, column=1, padx=10, pady=1, sticky=tkinter.W)
        self._rows_entry.bind('<FocusIn>', self._field_get_focus)
        self._rows_entry.bind('<FocusOut>', self._field_lose_focus)
        self._rows_entry.is_valid = False

        # Column label
        cols_label = tkinter.Label(master=self._dialog_window,
                                   text='Columns:', font=SUBTITLE_FONT)
        cols_label.grid(row=3, column=2, padx=10, pady=5, sticky=tkinter.W)
        # Column entry box
        self._cols_entry = tkinter.Entry(master=self._dialog_window, width=10, font=SUBTITLE_FONT)
        self._cols_entry.grid(row=3, column=3, padx=10, pady=1, sticky=tkinter.W)
        self._cols_entry.bind('<FocusIn>', self._field_get_focus)
        self._cols_entry.bind('<FocusOut>', self._field_lose_focus)
        self._cols_entry.is_valid = False

        # First player label
        self.first_label = tkinter.Label(master=self._dialog_window,
                                         text='Who goes first?', font=DEFAULT_FONT)
        self.first_label.grid(row=5, column=0, columnspan=4, padx=10, pady=10)
        # First player radio buttons
        first_player = tkinter.IntVar()  # Value should be retrieved using the get() method
        self._first_is_black = tkinter.Radiobutton(master=self._dialog_window, text='Black', variable=first_player,
                                                   value=1, indicatoron=0, font=SUBTITLE_FONT, width=7)
        self._first_is_black.grid(row=6, column=0, columnspan=2, padx=5, pady=0)
        self._first_is_white = tkinter.Radiobutton(master=self._dialog_window, text='White', variable=first_player,
                                                   value=2, indicatoron=0, font=SUBTITLE_FONT, width=7)
        self._first_is_white.grid(row=6, column=2, columnspan=2, padx=5, pady=0)

        # NE player label
        self.ne_label = tkinter.Label(master=self._dialog_window,
                                      text='Choose the starting layout of the board by specifying which player\'s\n'
                                           'piece will appear in the North-West corner of the 4 central tiles.',
                                      font=DEFAULT_FONT)
        self.ne_label.grid(row=8, column=0, columnspan=4, padx=10, pady=10)
        # NE player radio buttons
        ne_player = tkinter.IntVar()  # Value should be retrieved using the get() method
        self._ne_is_black = tkinter.Radiobutton(master=self._dialog_window, text='Black', variable=ne_player,
                                                value=1, indicatoron=0, font=SUBTITLE_FONT, width=7)
        self._ne_is_black.grid(row=9, column=0, columnspan=2, padx=5, pady=0)
        self._ne_is_white = tkinter.Radiobutton(master=self._dialog_window, text='White', variable=ne_player,
                                                value=2, indicatoron=0, font=SUBTITLE_FONT, width=7)
        self._ne_is_white.grid(row=9, column=2, columnspan=2, padx=5, pady=0)

        # Dictionary of all widget or variables in the class which take user input
        self._all_fields = {'rows': self._rows_entry, 'cols': self._cols_entry, 'first': first_player,
                            'ne_player': ne_player}  # <-- INCOMPLETE!


    def rows(self):
        return self._rows

    def cols(self):
        return self._cols

    def first(self):
        return self._first

    def ne_player(self):
        return self._ne_player

    def win(self):
        return self._win

    def was_ok_clicked(self):
        return self._ok_clicked

    def validate_all(self):
        for each in self._all_fields:
            if not self._validate_startup_widget(each):
                return False

        return True

    def show(self):
        self._dialog_window.grab_set()
        self._dialog_window.wait_window()

    def _on_ok_click(self):
        self._ok_clicked = True
        self._rows = self._rows_entry.get()
        self._cols = self._cols_entry.get()
        #first
        #neplayer
        #win

        self._dialog_window. destroy()

    def _on_quit_click(self):
        self._dialog_window.destroy()
        raise UserQuit

    def _field_get_focus(self, event):
        event.widget.config(background='#ffffff')

    def _field_lose_focus(self, event):
        event.widget.is_valid = self._validate_startup_widget(event.widget)
        if event.widget.is_valid:
            return
        else:
            event.widget.config(background='#ff8080')

    def _validate_startup_widget(self, widget: 'tkinter widget') -> bool:
        """
        Takes one of the widgets from an active instance of StartupDialog and checks that is contains a valid value.
        :param widget: A widget from an active instance of StartupDialog
        :return: True or False
        """

        if widget == self._rows_entry or widget == self._cols_entry:
            try:
                value = int(widget.get())
            except ValueError:
                return False

            if value % 2 != 0:
                return False
            elif not 4 <= value <= 16:
                return False
            else:
                return True

        raise UnableToIdentifyWidget


if __name__ == '__main__':
    try:
        OthelloApplication().start()
    except UserQuit:
        pass
