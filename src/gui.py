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

import pygtk
pygtk.require('2.0')
import gtk
import os

from videotable import VideoTable
from sequencer import Sequencer

class Gui:
    VIDTABLE_COLUMNS = 5
    VIDTABLE_ROWS = 4
    NUM_SEQ_STEPS = 4
    NUM_MAX_VIDEOS = VIDTABLE_COLUMNS * VIDTABLE_ROWS

    attach_detach_mode = True

    button_src = []
    video_image = []
    video_pitch = []
    video_pitch_adj = []
    seq_active_checkbox = []
    button_seq_step = []
    seq_step_image = []
    seq_step_pitch = []
    seq_step_pitch_adj = []

    source_video_drag_number = 0

    thumbnail_width = 120
    thumbnail_height = 90

    HOME = os.getenv("HOME")

    def __init__(self, videotable, sequencer):
        self.videotable = videotable
        self.sequencer = sequencer

        self.accel_group = gtk.AccelGroup()
        self.empty_pixbuf = gtk.gdk.pixbuf_new_from_file("img/empty.png")
        
        ### Gui separated into pieces
        self.window()
        self.import_file_frame()
        self.video_sources_frame()
        self.sequencer_frame()
        self.accelerators()

        self.window.show_all()


### window

    def window(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)        
        self.window.set_title("freemix")
       
        self.window.set_border_width(20) 
        icon = gtk.gdk.pixbuf_new_from_file("img/freemix_small.png")
        self.window.set_icon(icon)

        self.window.connect("delete_event", self.delete_event)

        self.hbox1 = gtk.HBox(False, 0)
        self.window.add(self.hbox1)       


### import file

    def import_file_frame(self):
        import_frame = gtk.Frame("import file")
        self.hbox1.pack_start(import_frame, False, False, 0)
        self.file_chooser = gtk.FileChooserWidget()
        import_frame.add(self.file_chooser)
        self.file_chooser.connect("file-activated", self.file_chosen, None)

        self.vbox1 = gtk.VBox(False, 0)
        self.hbox1.pack_start(self.vbox1, False, False, 0)

    def file_chosen(self, widget, data=None):
        file = self.file_chooser.get_filename()
        print file

        cell = self.videotable.import_file(file)
        print cell
        # "mplayer -really-quiet -vo png -frames 1 %s" file_src
        # "mkdir -p %s/.freemix%s", HOME, dirname

        thumbfile = self.HOME + "/.freemix" + file
        print thumbfile

        thumbnail = gtk.gdk.pixbuf_new_from_file_at_size (thumbfile, \
            self.thumbnail_width, self.thumbnail_height)
        self.video_image[cell].set_from_pixbuf(thumbnail)


### video sources table

    def video_sources_frame(self):
        video_cell_box = []

        vidsrc_frame = gtk.Frame("video sources")
        self.vbox1.pack_start(vidsrc_frame, False, False, 0)
        
        vid_table_box = gtk.VBox(False, 0)
        vidsrc_frame.add(vid_table_box)

        free_vid_box = gtk.HBox(False, 0)
        vid_table_box.pack_start(free_vid_box, True, True, 0)

        empty_label = gtk.Label("")
        free_vid_box.pack_start(empty_label, True, True, 0)
        
        self.attach_detach_button = gtk.ToggleButton("  empty videos  ")
        self.attach_detach_button.connect("clicked", self.switch_attach_detach_mode, None)
        free_vid_box.pack_start(self.attach_detach_button, False, False, 0)

        separator = gtk.HSeparator()
        vid_table_box.pack_start(separator, True, True, 0)

        sources_table = gtk.Table(self.VIDTABLE_COLUMNS - 1, self.VIDTABLE_ROWS - 1, True)
        
        target_table = [( "text/plain", 0, 80 )]

        n_row = 0
        i = 0
        while (n_row < self.VIDTABLE_ROWS):
            n_column = 0
            while (n_column < self.VIDTABLE_COLUMNS):
                video_cell_box.append(gtk.HBox(False, 0))
                
                self.button_src.append(gtk.Button())
                self.video_image.append(gtk.Image())
                self.video_image[i].set_from_pixbuf(self.empty_pixbuf)
                self.button_src[i].set_image(self.video_image[i])

                self.button_src[i].drag_source_set(gtk.gdk.BUTTON1_MASK, target_table, gtk.gdk.ACTION_COPY)
                
                self.button_src[i].connect ("clicked", self.vid_button_clicked, i)
                self.button_src[i].connect ("drag_begin", self.source_drag_begin, i)

                video_cell_box[i].pack_start(self.button_src[i])

                self.video_pitch_adj.append (gtk.Adjustment(1, 0.1, 5, 0.1, 0.1, 0.0))
                self.video_pitch.append(gtk.VScale(self.video_pitch_adj[i]))
                self.video_pitch[i].connect ("value_changed", self.video_pitch_changed, i)
                video_cell_box[i].pack_start(self.video_pitch[i])
                
                sources_table.attach(video_cell_box[i], n_column, n_column + 1, \
                             n_row, n_row + 1)

                n_column += 1
                i += 1
            n_row += 1 

        vid_table_box.pack_start(sources_table, False, False, 0)

    def switch_attach_detach_mode(self, widget, data=None):
        self.attach_detach_mode = not self.attach_detach_mode
        print self.attach_detach_mode

    def vid_button_clicked(self, widget, number):
        if self.attach_detach_mode:
            print self.videotable.get_file(number)
            self.videotable.video_play(number)
        else:
            self.videotable.empty_element(number) 
            self.video_image[number].set_from_pixbuf(self.empty_pixbuf)
            self.video_pitch_adj[number].set_value(1.0)

    def video_pitch_changed(self, widget, number):
        if number < self.NUM_MAX_VIDEOS:
            pitch = self.video_pitch_adj[number].get_value()
            self.videotable.change_video_pitch(number, pitch)
        else:
            number -=self.NUM_MAX_VIDEOS
            pitch = self.seq_step_pitch_adj[number].get_value()
            self.sequencer.change_seq_video_pitch(number, pitch)

    def source_drag_begin(self, widget, event, number):
        self.source_video_drag_number = number


### sequencer

    def sequencer_frame(self):
        self.seq_active = []
        sequencer_cell_box = []

        sequencer_frame = gtk.Frame("sequencer")
        self.vbox1.pack_start(sequencer_frame, False, False, 0)

        sequencer_box = gtk.HBox(False, 0)
        sequencer_frame.add(sequencer_box)

        sequencer_table = gtk.Table(self.NUM_SEQ_STEPS + 1, 3, False)

        target_table = [( "text/plain", 0, 80 )]

        i = 0
        while (i < self.NUM_SEQ_STEPS):
            self.seq_active_checkbox.append(gtk.CheckButton())
            sequencer_table.attach(self.seq_active_checkbox[i], i, i + 1, 0, 1)
            self.seq_active_checkbox[i].connect("clicked", self.seq_step_active, i)
            self.seq_active.append(False)
            i += 1

        i = 0
        while (i < self.NUM_SEQ_STEPS):
            sequencer_cell_box.append(gtk.HBox(False, 0))
                
            self.button_seq_step.append(gtk.ToggleButton())
            self.seq_step_image.append(gtk.Image())
            self.seq_step_image[i].set_from_pixbuf(self.empty_pixbuf)
            self.button_seq_step[i].set_image(self.seq_step_image[i])

            self.button_seq_step[i].drag_dest_set(gtk.DEST_DEFAULT_ALL, target_table, gtk.gdk.ACTION_COPY)

            self.button_seq_step[i].connect("clicked", self.seq_button_clicked, i)
            self.button_seq_step[i].connect("drag_drop", self.sequencer_drag_drop, i)

            sequencer_cell_box[i].pack_start(self.button_seq_step[i])

            self.seq_step_pitch_adj.append (gtk.Adjustment(1, 0.1, 5, 0.1, 0.1, 0.0))
            self.seq_step_pitch.append(gtk.VScale(self.seq_step_pitch_adj[i]))
            self.seq_step_pitch[i].connect ("value_changed", self.video_pitch_changed, self.NUM_MAX_VIDEOS + i)
            sequencer_cell_box[i].pack_start(self.seq_step_pitch[i])
                
            sequencer_table.attach(sequencer_cell_box[i], i, i + 1, 1, 2)

            i += 1 

        sequencer_box.pack_start(sequencer_table, True, True, 0)

        vseparator = gtk.VSeparator()
        sequencer_box.pack_start(vseparator, True, True, 0)

        self.seq_pitch_adj = gtk.Adjustment(80, 30, 130, 1, 1, 0.0)
        self.seq_pitch = gtk.VScale(self.seq_pitch_adj)
        self.seq_pitch.connect ("value_changed", self.sequencer_bpm_changed, None)
        self.seq_pitch.set_digits(0)
        sequencer_box.pack_start(self.seq_pitch)

        self.seq_pitch_tap = gtk.Button(" tap ")
        self.seq_pitch_tap.connect("clicked", self.seq_pitch_tap_cb, None)
        sequencer_box.pack_start(self.seq_pitch_tap)

    def seq_pitch_tap_cb(self, widget, data=None):
        self.sequencer.sequencer_pitch_tap()

    def seq_button_clicked(self, widget, number):
        if self.attach_detach_mode:
            print self.sequencer.get_file(number)
            self.sequencer.step_play(number)
        else:
            self.seq_active_checkbox[number].set_active(False)
            self.sequencer.empty_step(number)
            self.seq_step_image[number].set_from_pixbuf(self.empty_pixbuf)
            self.seq_step_pitch_adj[number].set_value(1.0)

    def seq_step_active(self, widget, number):
        self.seq_active[number] = not (self.seq_active[number])
        self.sequencer.switch_step_activeness(number)

    def sequencer_drag_drop(self, widget, context, x, y, time, number):
        file_src = self.videotable.get_file(self.source_video_drag_number)
        self.sequencer.load_file(number, file_src)

        thumbfile = self.HOME + "/.freemix" + file_src

        thumbnail = gtk.gdk.pixbuf_new_from_file_at_size (thumbfile, \
            self.thumbnail_width, self.thumbnail_height)
        self.seq_step_image[number].set_from_pixbuf(thumbnail)

        pitch = self.videotable.get_pitch(self.source_video_drag_number)
        self.seq_step_pitch_adj[number].set_value(pitch)

    def sequencer_bpm_changed(self, widget, data=None):
            bpm = self.seq_pitch_adj.get_value()
            self.sequencer.bpm_change(bpm)


### accelerators

    def accelerators(self):
        self.window.add_accel_group(self.accel_group)

        lista = [ord("1"), ord("2"), ord("3"), ord("4"), ord("5"), \
                 ord("Q"), ord("W"), ord("E"), ord("R"), ord("T"), \
                 ord("A"), ord("S"), ord("D"), ord("F"), ord("G"), \
                 ord("Z"), ord("X"), ord("C"), ord("V"), ord("B")]
        for i in (range(self.NUM_MAX_VIDEOS)):
            self.button_src[i].add_accelerator("clicked", self.accel_group, \
                lista[i], gtk.gdk.LOCK_MASK, gtk.ACCEL_VISIBLE)

#        self.seq_pitch_tap.add_accelerator("clicked", self.accel_group, \
#            space, gtk.gdk.LOCK_MASK, gtk.ACCEL_VISIBLE)
#        self.attach_detach_button.add_accelerator("clicked", self.accel_group, \
#            delete, gtk.gdk.LOCK_MASK, gtk.ACCEL_VISIBLE)

### main and events 

    def main(self):
        gtk.main()

    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        print "\m/ see ya"
        return False


if __name__ == "__main__":
    gui = Gui()
    gui.main()
