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

from videosource import VideoSource


class Sequencer:
    '''Sequencer class.
    Handles the steps and loop of the sequencer.'''
    def __init__(self, seq_steps):
        self.step = 0
        self.running_step = 0
        self.tap_counter = 0

        self.sequencer_steps = seq_steps - 1
        self.sequencer_sources = []
        
        for i in range(self.sequencer_steps):
            self.sequencer_sources.append(VideoSource())

    def import_file(self, file_src):
        pass
        # To Do: Drag and drop files from table to sequencer

    def sequencer_pitch_tap(self):
        pass
        #To Do: catch taps and count/clock them to get bpm

    def loop_callback(self):
        pass
        # To Do: send to engine active steps

        if (self.step != self.sequencer_steps):        
           self.step += 1
        else:
           self.step = 0

    def de_activate_step(self, step_number):
        if (self.sequencer_sources[step_number].is_active == True):
            self.sequencer_sources[step_number].deactivate
        else:
            self.sequencer_sources[step_number].activate

    def change_seq_video_pitch(self, step_number, pitch):
        self.sequencer_sources[step_number].change_pitch(pitch)
