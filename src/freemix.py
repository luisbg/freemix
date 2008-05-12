#!/usr/bin/env python
 
# Copyright (C) 2008 Luis de Bethencourt
# <luisbg"ubuntu.com>
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

import sys

import gobject
# gobject.threads_init()

import os.path
 
import pygtk
pygtk.require('2.0')	# Must be before 'import gtk'
import gtk

from videotable import VideoTable

from sequencer import Sequencer 

class Freemix:
    def main(self):
        print "freemix 0.1 alpha"

        self.table_width = 5
        self.table_height = 4
        self.sequencer_steps = 4

        self.videotable = VideoTable(self.table_width, self.table_height)
        self.sequencer = Sequencer(self.sequencer_steps)    

        gtk.main()

if __name__ == "__main__":
    try:
        freemix = Freemix()
        freemix.main()
    except SystemExit:
        raise
    
