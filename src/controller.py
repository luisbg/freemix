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

"""freemix controller class"""

from engine import Engine

class Controller:
    '''freemix controller class. Acts like a man in the middle between
       interfaces and the gstreamer engine.''' 

    def __init__(self, engine):
        self.engine = engine
        self.max_video_number = 20  # from gui.py
        self.running_vid = 0

    def play(self, file, speed, vid_number):
        self.engine.play(file, speed)
        self.running_vid = vid_number

if __name__ == "__main__":
    import os, optparse

    usage = """ controller.py"""

    parser = optparse.OptionParser(usage=usage)
    (options, args) = parser.parse_args()

    controller = Controller(options.input)
    gobject.MainLoop().run()
