# Daniel Gold (46043649)
# ICS 32 - Project #5: Othello (Part II)

# This is the main gui module which will run the Othello program and harness other modules such as othello_logic
# and point.

import othello_logic
import point
import tkinter


DEFAULT_FONT = ('Helvetica', 14)


class OthelloApplication:

    def __init__(self):
        self._state = None

        self._root_window = tkinter.Tk()

        self._canvas = tkinter.Canvas( master=self._root_window, width=800, height=800, background='#0082b')

        self._canvas.grid(row=0, column=0, padx=10, pady=10, sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)

        self._canvas.bind('<Configure>', self._on_canvas_resized)
        self._canvas.bind('<Button-1>', self._on_canvas_clicked)
        self._canvas.bind('<Button-2>', self._on_canvas_right_clicked)

        self._root_window.rowconfigure(0, weight=1)
        self._root_window.columnconfigure(0, weight=1)

        dialog_info = None
        dialog_error = None

        while True:
            startup = StartupDialog()
            startup.show()

            if startup.was_ok_clicked:

                dialog_error, dialog_info = self._validate_startup_parameters(startup)
                if dialog_error is not None:
                    continue

                self.state = othello_logic.GameState(dialog_info[0], dialog_info[1], dialog_info[2], dialog_info[3],
                                                     dialog_info[4])





    def start(self):
        self._root_window.mainloop()

    def _on_canvas_resized(self):
        pass

    def _on_canvas_clicked(self):
        pass

    def _on_canvas_right_clicked(self):
        pass

    def _redraw_all(self):
        """Delete and re-draw all elements on the canvas element"""

        self._canvas.delete(tkinter.ALL)

        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()

    def _get_startup_parameters(self):
        """
        Opens a dialogue box to query the user for startup parameters.
        :return: tuple containing all startup parameters.
        """
        pass

    def _validate_startup_parameters(self, dialog: StartupDialog) -> (str, list):
        """
        Looks at the values stored in the StartupDialog object to see if they are all valid.
        :param dialog: StartupDialog object that has already been called and which the user is now finished with.
        :return: Two values as a tuple. A text string specifying what was wrong with the input (which can be passed to
        the user). Also, a list of the values which the user entered to re-populate the dialogue box with for their
        next attempt. The there is no error, the value of the first returned value will be None.
        """
        pass


class StartupDialog:

    def __init__(self):
        self._rows = None
        self._cols = None
        self._first = None
        self._ne_player = None
        self._win = None

        self._ok_clicked = False

        self._dialog_window = tkinter.Toplevel()

        who_label = tkinter.Label(master=self._dialog_window, text='What kind of Othello game would you like to play?',
                                  font=DEFAULT_FONT)

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


if __name__ == '__main__':
    pass
