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

from videosource import VideoSource 
from engine import Engine

class VideoTable:
    '''VideoTable class is the man in the middle between the gui and the engine.
    It stores and handles the video sources table.'''

    def __init__(self, table_width, table_height, engine):
        '''Initialize variables and fill table with videosources.'''

        self.engine = engine

        self.source_table_width = table_width
        self.source_table_height = table_height
        self.source_table_range = \
            self.source_table_width * self.source_table_height
        self.source_table = []

        # fill
        for i in range(self.source_table_range):
            self.source_table.append(VideoSource())

    def import_file(self, file_src):
        '''Import file to first empty cell.'''

        i = 0
        filled = False
        while ((i < 20) and (filled == False)):
            if (self.source_table[i].is_used() == False):
                self.source_table[i].set_file(file_src)
                filled = True
                cell = i
            i+=1

        return cell

    def video_play(self, video_number):
        '''Play video file of videotable cell.'''

        file = self.source_table[video_number].get_file()
        pitch = self.source_table[video_number].get_pitch()
        self.engine.play(file, pitch)

    def empty_element(self, video_number):
        '''Empty videotbale cell.'''

        self.source_table[video_number].empty()

    def change_video_pitch(self, video_number, pitch):
        '''Change the pitch of the videotable cell.'''

        self.source_table[video_number].change_pitch(pitch)

    def get_pitch(self, cell):
        '''Get the pitch of the videotable cell.'''

        return self.source_table[cell].get_pitch()

    def get_file(self, cell):
        '''Get file of the videotable cell.'''

        return self.source_table[cell].get_file()


if __name__ == "__main__":
    print "Videotable testing..."
    videotable = VideoTable(5, 4)
    videotable.import_file("test_1.avi")
    videotable.import_file("test_2.avi")
    print videotable.source_table[0].file
    print videotable.source_table[1].file
    print videotable.source_table[0].is_used()
    videotable.change_video_pitch(1, 1.2)
    print videotable.source_table[1].pitch
