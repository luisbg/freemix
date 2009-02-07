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

from engine import Engine

class VideoSource:
    '''VideoSource is each element of the video sources table/sequencer.
    Handles file, pitch, if its in use, and playback of the element.'''

    def __init__(self):
        '''Initialize videosource variables.'''

        self.file = ""
        self.used = False
        self.pitch = 1.0
        self.active = False

    def set_file(self, file_src):
        '''If element not used set video file.'''

        if (self.used == False):
            self.file = file_src
            self.used = True

    def get_file(self):
        '''Get video file.'''

        return self.file

    def change_pitch(self, pitch):
        '''Change video pitch.'''

        if (self.used == True):
            self.pitch = pitch
            print "new pitch: %r" % pitch
            # To Do: send new pitch to engine

    def get_pitch(self):
        '''Get video pitch.'''

        return self.pitch

    def empty(self):
        '''Empty the element if used.'''

        if (self.used == True):
            print "emptying: " + self.file
            self.used = False
            self.file = ""
            self.pitch = 1.0

    def is_used(self):
        '''Is the element used?'''

        return self.used

    def activate(self):
        '''Activate element.'''

        self.active = True

    def deactivate(self):
        '''Deactivate element.'''

        self.active = False

    def is_active(self):
        '''Is element active?'''

        return self.active


if __name__ == "__main__":
     print "VideoSource testing..."
