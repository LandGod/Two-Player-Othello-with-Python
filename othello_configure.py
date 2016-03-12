# Daniel Gold (46043649)
# ICS 32 - Project #5: Othello (Part II)

# This module is responsible for creating a popup which takes the initial values which the game needs to set itslef
# up.


import tkinter
from othello_gui import DEFAULT_FONT
from othello_gui import TITLE_FONT
from othello_gui import SUBTITLE_FONT


class UnableToIdentifyWidget(Exception):
    """To be thrown when the tkinter widget specified cannot be identified as one of the expected types by a function"""


class StartupDialog:

    def __init__(self):
        self._all_choices = {'rows': None, 'cols': None, 'first': None, 'ne_player': None, 'win': None}
        self._all_choices_keys = ['rows', 'cols', 'first', 'ne_player', 'win']  # Order must match self._all_fields

        self._ok_clicked = False

        self._dialog_window = tkinter.Toplevel()

        self._dialog_window.wm_title("[FULL] Options")

        self._dialog_window.bind('<Configure>', self._dialog_window.after(10, self._dialog_window.lift))

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
        row_col_label = tkinter.Label(master=self._dialog_window, text='Please specify the number of rows and '
                                                                       'columns you would like to board to have.\n'
                                                                       'Each value must be an even number between 4 '
                                                                       'and 16 (inclusive).',
                                      font=DEFAULT_FONT)
        row_col_label.grid(row=1, column=0, columnspan=4, padx=10, pady=2, sticky=tkinter.W)

        # Row and column entry spaces with labels (both in the same row).
        # Row label
        rows_label = tkinter.Label(master=self._dialog_window, text='Rows:', font=SUBTITLE_FONT)
        rows_label.grid(row=3, column=0, padx=10, pady=5, sticky=tkinter.W)
        # Row entry box
        self._rows_entry = tkinter.Entry(master=self._dialog_window, width=10, font=SUBTITLE_FONT)
        self._rows_entry.grid(row=3, column=1, padx=10, pady=1, sticky=tkinter.W)
        self._rows_entry.bind('<FocusIn>', self._field_get_focus)
        self._rows_entry.bind('<FocusOut>', self._field_lose_focus)

        # Column label
        cols_label = tkinter.Label(master=self._dialog_window, text='Columns:', font=SUBTITLE_FONT)
        cols_label.grid(row=3, column=2, padx=10, pady=5, sticky=tkinter.W)
        # Column entry box
        self._cols_entry = tkinter.Entry(master=self._dialog_window, width=10, font=SUBTITLE_FONT)
        self._cols_entry.grid(row=3, column=3, padx=10, pady=1, sticky=tkinter.W)
        self._cols_entry.bind('<FocusIn>', self._field_get_focus)
        self._cols_entry.bind('<FocusOut>', self._field_lose_focus)

        # First player label
        self._first_label = tkinter.Label(master=self._dialog_window,
                                          text='Who goes first?', font=DEFAULT_FONT)
        self._first_label.grid(row=5, column=0, columnspan=4, padx=10, pady=10)
        # First player radio buttons
        self._first_player = tkinter.IntVar()  # Value should be retrieved using the get() method

        self._first_is_black = tkinter.Radiobutton(master=self._dialog_window, text='Black',
                                                   variable=self._first_player, value=1, indicatoron=0,
                                                   font=SUBTITLE_FONT, width=7)
        self._first_is_black.grid(row=6, column=0, columnspan=2, padx=5, pady=0)
        self._first_is_white = tkinter.Radiobutton(master=self._dialog_window, text='White',
                                                   variable=self._first_player, value=2, indicatoron=0,
                                                   font=SUBTITLE_FONT, width=7)
        self._first_is_white.grid(row=6, column=2, columnspan=2, padx=5, pady=0)

        # NE player label
        self._ne_label = tkinter.Label(master=self._dialog_window,
                                       text='Choose the starting layout of the board by specifying which player\'s\n'
                                            'piece will appear in the North-West corner of the 4 central tiles.',
                                       font=DEFAULT_FONT)
        self._ne_label.grid(row=8, column=0, columnspan=4, padx=10, pady=10)
        # NE player radio buttons
        self._ne_player_selection = tkinter.IntVar()  # Value should be retrieved using the get() method

        self._ne_is_black = tkinter.Radiobutton(master=self._dialog_window, text='Black',
                                                variable=self._ne_player_selection, value=1, indicatoron=0,
                                                font=SUBTITLE_FONT, width=7)
        self._ne_is_black.grid(row=9, column=0, columnspan=2, padx=5, pady=0)
        self._ne_is_white = tkinter.Radiobutton(master=self._dialog_window, text='White',
                                                variable=self._ne_player_selection, value=2, indicatoron=0,
                                                font=SUBTITLE_FONT, width=7)
        self._ne_is_white.grid(row=9, column=2, columnspan=2, padx=5, pady=0)

        # Win condition label
        self._win_label = tkinter.Label(master=self._dialog_window, text='Please specify the desired victory '
                                                                         'conditions:', font=DEFAULT_FONT)
        self._win_label.grid(row=11, column=0, columnspan=4, padx=10, pady=10)
        # Win radio buttons
        self._win_condition = tkinter.BooleanVar()  # Value should be retrieved using the get() method

        self._win_is_most = tkinter.Radiobutton(master=self._dialog_window, text='Most Pieces',
                                                variable=self._win_condition, value=True, indicatoron=0,
                                                font=SUBTITLE_FONT, width=14)
        self._win_is_most.grid(row=12, column=0, columnspan=2, padx=5, pady=0)
        self._win_is_least = tkinter.Radiobutton(master=self._dialog_window, text='Least Pieces',
                                                 variable=self._win_condition, value=False, indicatoron=0,
                                                 font=SUBTITLE_FONT, width=14)
        self._win_is_least.grid(row=12, column=2, columnspan=2, padx=5, pady=0)

        # List of all widget or variables in the class which take user input
        self._all_fields = [self._rows_entry, self._cols_entry, self._first_player,
                            self._ne_player_selection,  self._win_condition]  # Order must match self._all_choices_keys

        # Set defaults
        self._first_is_black.select()
        self._ne_is_black.select()
        self._win_is_most.select()
        self._rows_entry.insert(tkinter.END, '8')
        self._cols_entry.insert(tkinter.END, '8')

        # Buttons
        okay_button = tkinter.Button(master=self._dialog_window, text='Ok', font=SUBTITLE_FONT,
                                     command=self._on_ok_click)

        okay_button.grid(row=14, column=3, padx=10, pady=10, sticky=tkinter.S)

        quit_button = tkinter.Button(master=self._dialog_window, text='Quit', font=SUBTITLE_FONT,
                                     command=self._on_quit_click)

        quit_button.grid(row=14, column=4, padx=10, pady=10, sticky=tkinter.S)

    def rows(self):
        return int(self._all_choices['rows'])

    def cols(self):
        return int(self._all_choices['cols'])

    def first(self):
        return int(self._all_choices['first'])

    def ne_player(self):
        return int(self._all_choices['ne_player'])

    def win(self):
        if self._all_choices['win']:
            return '>'
        else:
            return '<'

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

        if self.validate_all():
            for i in range(len(self._all_choices)):
                self._all_choices[self._all_choices_keys[i]] = self._all_fields[i].get()

            self._dialog_window.destroy()
            self._ok_clicked = True

        else:
            self._dialog_window.focus_force()

    def _on_quit_click(self):
        self._dialog_window.destroy()
        self._ok_clicked = False

    def _field_get_focus(self, event):
        event.widget.config(background='#ffffff')

    def _field_lose_focus(self, event):
        if self._validate_startup_widget(event.widget):
            return
        else:
            event.widget.config(background='#ff8080')

    def _validate_startup_widget(self, widget: 'tkinter widget') -> bool:
        """
        Takes one of the widgets from an active instance of StartupDialog and checks that is contains a valid value.
        :param widget: A widget from an active instance of StartupDialog
        :return: True or False
        """

        if widget is self._rows_entry or widget is self._cols_entry:
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

        elif widget is self._first_player or widget is self._ne_player_selection:
            value = widget.get()

            if value != 1 and value != 2:
                return False
            else:
                return True
        elif widget is self._win_condition:
            value = widget.get()
            return type(value) == bool

        else:
            raise UnableToIdentifyWidget(widget)
