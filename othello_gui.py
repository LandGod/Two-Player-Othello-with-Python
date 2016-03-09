# Daniel Gold (46043649)
# ICS 32 - Project #5: Othello (Part II)

# This is the main gui module which will run the Othello program and harness other modules such as othello_logic
# and point.

import othello_logic
import othello_configure
import point
import tkinter

DEFAULT_FONT = ('Helvetica', 12)
TITLE_FONT = ('Helvetica', 18)
SUBTITLE_FONT = ('Helvetica', 16)


class UserQuit(Exception):
    """To be thrown when the user elects to quit the program."""


class OthelloApplication:

    def __init__(self):
        self._state = None

        self._root_window = tkinter.Tk()

        self._root_window.wm_title("[FULL] Othello")

        self._canvas = tkinter.Canvas(master=self._root_window, width=800, height=800, background='#00802b')

        self._canvas.grid(row=0, column=0, padx=10, pady=10, sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)

        self._canvas.bind('<Configure>', self._on_canvas_resized)
        self._canvas.bind('<Button-1>', self._on_canvas_clicked)
        self._canvas.bind('<Button-2>', self._on_canvas_right_clicked)

        self._root_window.rowconfigure(0, weight=1)
        self._root_window.columnconfigure(0, weight=1)

        startup = othello_configure.StartupDialog()
        startup.show()

        if not startup.was_ok_clicked():
            raise UserQuit

        state = othello_logic.GameState(startup.rows(), startup.cols(), startup.first(), startup.ne_player(),
                                        startup.win())

        self._root_window.lift()

    def start(self):
        self._root_window.mainloop()

    def _on_canvas_resized(self, event: 'Tkinter Event'):
        pass

    def _on_canvas_clicked(self, event: 'Tkinter Event'):
        pass

    def _on_canvas_right_clicked(self, event: 'Tkinter Event'):
        pass

    def _redraw_all(self):
        """Delete and re-draw all elements on the canvas"""

        self._canvas.delete(tkinter.ALL)

        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()

        #re-draw everything


if __name__ == '__main__':
    try:
        OthelloApplication().start()
    except UserQuit:
        pass
