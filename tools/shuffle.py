#!/usr/bin/env python

# Copyright (C) 2008 Luis de Bethencourt
# <luisbg@ubuntu.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
# USA


"""play videos randomly"""

import sys, os
sys.path.insert(0, "../src")

import gobject
gobject.threads_init()

import time
import optparse
import random

from engine import Engine
from controller import Controller

class Shuffle:
    def __init__(self):
        usage = """shuffle.py [input_folder]"""
        parser = optparse.OptionParser(usage = usage)
        (options, args) = parser.parse_args()

        if len(args) == 0:
            print "A video folder needs to be specified."
            exit()
        else:
            self.folder = args[0]
            if self.folder.endswith("/"):
                self.folder = self.folder[:-1]

        self.engine = Engine()
        self.controller = Controller(self.engine)
        self.bpm = 30

        self.tree = []
        ls = os.listdir(self.folder)

        # Populating database of files in input directory.
        self.browse_folder(ls, self.folder, self.tree)

        self.length = len(self.tree)
        print ""
        print "Found " + str(self.length) + " videos."
        print ""

        self.timeout_id = gobject.timeout_add((60000/self.bpm), self.loop_callback)
        loop = gobject.MainLoop()
        loop.run()

    def loop_callback(self):
            video = random.choice(self.tree)
            self.controller.play(video, 1.0, 0)

            return True

    def browse_folder(self, folder, dir, tree):
        '''Creates a tree of all the files and folder inside the in    put dir.'''

        for files in folder:
            if not files.startswith(".") and (not files == folder):
                files = dir + "/" + files
                tree.append(files)
                if os.path.isdir(files):
                    temp = files[files.find(self.folder_short):]
                    temp = "".join("%s/" % (n) for n in \
                    temp.split("/")[1:])
                    new = os.listdir(files)
                    self.browse_folder(new, files, tree)
        

if __name__ == "__main__":
    try:
        print "Welcome to freemix shuffle... enjoy!"
        shuffle = Shuffle()

    except SystemExit:
        raise
