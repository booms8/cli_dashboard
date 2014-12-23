#!/usr/bin/env python2.7

# Useful links:
# http://www.tldp.org/HOWTO/Bash-Prompt-HOWTO/x361.html

import time
import sys

# Dict for picking element colors
# TODO: Expand? Darks/lights?
bcolors = {
    'K' : '\033[90m',
    'R' : '\033[91m',
    'G' : '\033[92m',
    'B' : '\033[94m',
    'C' : '\033[96m',
    'M' : '\033[95m',
    'Y' : '\033[93m',
    'N' : '\033[0m'}

class ProgressBar(object):
    """ This is a super simple progress bar for the command line.  """

    # TODO: Testing.
    # TODO: Threshold coloring
    def __init__(self, steps, pos = 0, width = 0.25, ansi = False, fillchar = '|'):
        """
        The number of steps until the bar gets to 100%
        width: Fraction of the terminal width to use (must be less than one)
        ansi: Enables/disables use of ANSI color codes (disabled by default for Windows support)
        steps: Number of times the object's update_progress() can be called
        fillchar: The character to fill the bar with.
        """
        self._curr = 0
        self._steps = steps
        self._msg = None
        self._pos = pos

        if width > 1:
            raise Exception("Width cannot be greater than 100%")

        self._width = width
        self._ansi = ansi

        self._bcol = bcolors['N']
        self._pcol = bcolors['N']
        self._mcol = bcolors['N']

        if len(fillchar) != 1 or not fillchar:
            raise Exception("Invalid value for fillchar")
        else:
            self._fillchar = fillchar

### Manipulate
    def add_progress(self, msg = None):
        """ Adds one tick to the progress bar and redraws """
        if self._curr > self._steps:
            raise Exception("Progress bar already completed")
        self.inc_curr()
        self.draw(msg)

    def lose_progress(self, msg = None):
        """ Removes one tick from the progress bar and redraws """
        if self._curr == 0:
            raise Exception("Progress bar already empty")
        self.dec_curr()
        self.draw(msg)

    def change_progress(self, pnt, msg = None):
        """
        Moves the progress bar to the specified tick and redraws
        pnt: Point to set the new current position
        """
        if self._steps < pnt:
            raise Exception("Point is outside the bounds of the progress bar")
        self.rep_curr(pnt)
        self.draw(msg)

    def inc_curr(self):
        """ Adds one tick to the progress bar """
        self._curr += 1

    def dec_curr(self):
        """ Removes one tick from the progress bar """
        self._curr -= 1

    def rep_curr(self, pnt):
        """
        Moves the progress bar to the specified tick
        pnt: Point to set the new current position
        """
        self._curr = pnt

### Create
    def draw(self, msg = None):
        """ 
        Draws the progress bar as it currently exists or with the specified message
        msg: Optional new message for the progress bar """
        if self._ansi:
            self._msg = self._mcol + msg + bcolors['N'] if msg != None else self._msg
        else:
            self._msg = msg if msg != None else self._msg

        self.move_up_as_needed()
        self.move_to_start_of_line()

        self.clear_curr_line()
        print self.get_progress_bar()
        if self._msg:
            self.clear_curr_line()
            print self._msg
        sys.stdout.flush()

    def get_progress_bar(self):
        """
        Outputs the progress bar string.
        """
        reserved_char_count = 2     # For start and ending character of the progress bar.
        progress_chars_max = self.get_terminal_width() - reserved_char_count
        progress_chars_max = int(self._width * progress_chars_max)    # Arbitrarily make it 1/4th the number of chars that can fit onscreen.
        percent_done = float(self._curr) / self._steps
        progress = int(percent_done * progress_chars_max)
        if self._ansi:
            bar = "[" + self._bcol.ljust(progress_chars_max, ' ') + bcolors['N'] + "]"
            return bar.replace(' ', self._fillchar, progress) + self._pcol + ' {}%'.format(percent_done*100) + bcolors['N']
        else:
            bar = "[".ljust(progress_chars_max, ' ') + "]"
            return bar.replace(' ', self._fillchar, progress) + ' {}%'.format(percent_done*100)

### Move
    def move_up_as_needed(self):
        """
        Move up in the term once or twice, depending on if you have a message.
        """
        if self._pos == 0:
            if self._curr != 0:
                self.move_up_one_line()
                if self._msg != None:
                    self.move_up_one_line()
        else:
            print "\033[{};1f".format(self._pos * 2)

    def get_terminal_width(self):
        """
        Get the width of the terminal.
        """
        import os
        rows, columns = os.popen('stty size', 'r').read().split()
        return int(columns)

    def move_to_start_of_line(self):
        """
        Moves to the start of the current line.
        """
        print "\r",

    def move_up_one_line(self):
        """
        Moves up one line in the terminal.
        """
        print "\033[1A",

    def clear_curr_line(self):
        """
        Clears the current line by filling with spaces then moves to the start.
        """
        print ' '.ljust(self.get_terminal_width()-1), '\r',

### Colors
    def set_bar_color(self, col):
        """
        Sets the progress bar color
        col: key for the bcolors dict; if not found, no color is set
        """
        if col in bcolors:
            self._bcol = bcolors[col]

    def set_perc_color(self, col):
        """
        Sets the progress percentage color
        col: key for the bcolors dict; if not found, no color is set
        """
        if col in bcolors:
            self._pcol = bcolors[col]

    def set_msg_color(self, col):
        """
        Sets the message color
        col: key for the bcolors dict; if not found, no color is set
        """
        if col in bcolors:
            self._mcol = bcolors[col]
