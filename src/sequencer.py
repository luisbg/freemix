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


class Sequencer:
    '''Sequencer class.
    Handles the steps and loop of the sequencer.'''
    def __init__(self, seq_steps):
        self.step = 0
        self.running_step = 0
        self.bpm = 80
        self.tap_counter = 0

        self.sequencer_steps = seq_steps
        self.sequencer_sources = []
        
        for i in range(self.sequencer_steps):
            self.sequencer_sources.append(VideoSource())

    def load_file(self, step, file_src):
        self.sequencer_sources[step].set_file(file_src)
        print "loading " + file_src + " on step " + str(step)

    def empty_step(self, step):
        self.sequencer_sources[step].empty()
        self.sequencer_sources[step].deactivate()

    def sequencer_pitch_tap(self):
        if (self.tap_counter != 3):        
            self.tap_counter += 1
        else:
            self.tap_counter = 0

        print "tap takk"
        #To Do: catch taps and count/clock them to get bpm

    def bpm_change(self, bpm):
        self.bpm = bpm
        print "bpm now: " + str(self.bpm)

    def loop_callback(self):
        #To Do: time loop

        if (self.sequencer_sources[self.step].is_active() == True):
           self.sequencer_sources[self.step].play_file()

        if (self.step != self.sequencer_steps):        
            self.step += 1
        else:
            self.step = 0

    def step_play(self, step):
        print "play " + str(step)

    def switch_step_activeness(self, step):
        if (self.sequencer_sources[step].is_active() == True):
            self.sequencer_sources[step].deactivate()
        else:
            self.sequencer_sources[step].activate()
        print str(step) + " now " \
            + str(self.sequencer_sources[step].is_active())

    def change_seq_video_pitch(self, step_number, pitch):
        self.sequencer_sources[step_number].change_pitch(pitch)

    def get_file(self, step):
        return self.sequencer_sources[step].get_file()

if __name__ == "__main__":
    print "Sequencer testing..."
