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
import gobject

class Sequencer:
    '''Sequencer class.
    Handles the steps and loop of the sequencer.'''

    def __init__(self, seq_steps, controller):
        '''Initialize sequencer variables.'''

        self.controller = controller

        self.step = 0
        self.running_step = 0
        self.bpm = 80
        self.old_bpm = 80
        self.tap_counter = 0

        self.sequencer_steps = seq_steps
        self.sequencer_sources = []
        
        for i in range(self.sequencer_steps):
            # create all sequencer elements
            self.sequencer_sources.append(VideoSource())

        # sequencer loop timeout
        self.timeout_id = gobject.timeout_add((60000/self.bpm), self.loop_callback)

    def load_file(self, step, file_src):
        '''Load file into sequencer step.'''

        self.sequencer_sources[step].set_file(file_src)
        print "loading " + file_src + " on step " + str(step)

    def empty_step(self, step):
        '''Empty sequencer step.'''

        self.sequencer_sources[step].empty()
        self.sequencer_sources[step].deactivate()

    def sequencer_pitch_tap(self):
        '''Sequencer pitch tap button clicked.'''

        if self.tap_counter == 0:
            # first tap, grab time
            self.start_time = gobject.get_current_time()
            self.tap_counter = 1
        else:
            if self.tap_counter == 1:
                # second tap, count up
                self.tap_counter = 2
            else:
                if self.tap_counter == 2:
                    # second tap, count up
                    self.tap_counter = 3
                else:
                    if self.tap_counter == 3:
                        # third tap, get time, set bpm 
                        self.end_time = gobject.get_current_time()
                        self.time = (self.end_time - self.start_time) / 3
                        if self.time < 2:
                            self.bpm = int(60.0 / self.time)
                            self.loop_callback()
                        self.tap_counter = 0

        # return bpm to gui to update it
        return self.bpm 

    def bpm_change(self, bpm):
        '''BPM changed, set new one.'''

        self.bpm = bpm
        print "bpm now: " + str(self.bpm)

    def loop_callback(self):
        '''Run step.'''

        # print self.step

        # if active play file
        if (self.sequencer_sources[self.step].is_active() == True):
            file = self.sequencer_sources[self.step].get_file()
            pitch = self.sequencer_sources[self.step].get_pitch()
            self.controller.play(file, pitch, 20 + self.step)

        # step up
        if (self.step != (self.sequencer_steps - 1)):        
            self.step += 1
        else:
            self.step = 0

        # if bpm has changed update sequencer loop timeout
        if self.old_bpm != self.bpm:
            gobject.source_remove(self.timeout_id)
            self.timeout_id = gobject.timeout_add(int(60000/self.bpm), self.loop_callback)
            self.bpm_old = self.bpm

        return True

    def step_play(self, step):
        '''Play the clicked step and set that step as current.'''

        self.step = step
        self.loop_callback()

    def switch_step_activeness(self, step):
        '''Activate or deactive step.'''

        if (self.sequencer_sources[step].is_active() == True):
            # if active, deactivate
            self.sequencer_sources[step].deactivate()
        else:
            # if unactive, activate
            self.sequencer_sources[step].activate()
        print str(step) + " now " \
            + str(self.sequencer_sources[step].is_active())

    def change_seq_video_pitch(self, step_number, pitch):
        '''Change the pitch of the video in the sequencer step.'''

        self.sequencer_sources[step_number].change_pitch(pitch)

    def get_file(self, step):
        '''Get file of sequencer step.'''

        return self.sequencer_sources[step].get_file()

if __name__ == "__main__":
    print "Sequencer testing..."
