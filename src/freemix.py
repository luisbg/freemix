#!/usr/bin/env python
 
# Copyright (C) 2008 Luis de Bethencourt
# <luisbg@ubuntu.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 1, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

"""freemix base class"""

import sys

import gobject
gobject.threads_init()

import os.path
 
import pygtk
pygtk.require('2.0')	# Must be before 'import gtk'
import gtk

from gui import Gui
from videotable import VideoTable
from sequencer import Sequencer 
from engine import Engine
from controller import Controller

TABLE_WIDTH = 5
TABLE_HEIGHT = 4
SEQUENCER_STEPS = 4

class Freemix:
    '''Freemix base class.
       Starts all classes:
           videotable -> videosource
           sequencer -> videosource
           gui'''

    def __init__(self, table_width, table_height, sequencer_steps):
        print "freemix 0.2 beta"

        if not(os.path.exists(os.environ["HOME"] + "/.freemix/")):
            os.mkdir(os.environ["HOME"] + "/.freemix/")

        engine = Engine()
        controller = Controller(engine)
        videotable = VideoTable(table_width, table_height, controller)
        sequencer = Sequencer(sequencer_steps, controller)

        gui = Gui(videotable, sequencer) 
        gui.main()

if __name__ == "__main__":
    try:
        freemix = Freemix(TABLE_WIDTH, TABLE_HEIGHT, SEQUENCER_STEPS)
    except SystemExit:
        raise
    
