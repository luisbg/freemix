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


class VideoTable:
    '''VideoTable class is the man in the middle between the gui and the engine.
    It stores and handles the video sources table.'''

    def __init__(self, table_width, table_height):
        self.source_table_width = table_width
        self.source_table_height = table_height
        self.source_table_range = \
            self.source_table_width * self.source_table_height
        self.source_table = []

        for i in range(self.source_table_range):
            self.source_table.append(VideoSource())

    def file_import(self, file_src):
        i = 0
        filled = False
        while ((i < 20) and (filled == False)):
            if (self.source_table[i].is_used() == False):
                self.source_table[i].set_file(file_src)
                filled = True
                print i
            i+=1
        # To Do: missing thumbnail handling

    def video_play(self, video_number):
        self.source_table[video_number].play_file
        print "video_play"

    def empty_element(self, video_number):
        self.source_table[video_number].empty

    def change_video_pitch(self, video_number, pitch):
        self.source_table[video_number].change_pitch(pitch)


if __name__ == "__main__":
    print "testing..."
    videotable = VideoTable(5, 4)
    videotable.file_import("test_1.avi")
    videotable.file_import("test_2.avi")
    print videotable.source_table[0].file
    print videotable.source_table[1].file
    print videotable.source_table[0].is_used()
    videotable.change_video_pitch(1, 1.2)
    print videotable.source_table[1].pitch
