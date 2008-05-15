#!/usr/bin/env python
 
# Copyright (C) 2008 Luis de Bethencourt
# <luis.debethencourt@sun.com>
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


class VideoSource:
    '''VideoSource is each element of the video sources table/sequencer.
    Handles file, pitch, if its in use, and playback of the element.'''
    def __init__(self):
        self.file = ""
        self.used = False
        self.pitch = 1.0
        self.active = False

    def set_file(self, file_src):
        if (self.used == False):
            self.file = file_src
            self.used = True

    def change_pitch(self, pitch):
        if (self.used == True):
            self.pitch = pitch

    def play_file(self):
        if (self.used == True):
            pass
            # To Do: send file and pitch to engine

    def empty(self):
        if (self.used == True):
            self.used = False
            self.file = ""
            self.pitch = 1.0

    def is_used(self):
        return self.used

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def is_active(self):
        return self.active
