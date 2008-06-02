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

import gobject
gobject.threads_init() 
import gst

class Engine:
    def __init__(self, filesrc):
        def bus_handler(unused_bus, message):
            print message.type
            if message.type == gst.MESSAGE_ASYNC_DONE:
                if self.first:
                  print "Playback file."
                  #self.AsyncDone()
                  self.first = False
                  self.pipeline.set_state(gst.STATE_PLAYING)
            if message.type == gst.MESSAGE_SEGMENT_DONE:
                self.SeekToLocation(0)
            if message.type == gst.MESSAGE_ERROR:
                print "ERROR"
            return gst.BUS_PASS

        # create our pipeline
        self.pipeline = gst.Pipeline()
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect ('message', bus_handler)
        
        self.src = gst.element_factory_make("filesrc", "src")
        self.decodebin = gst.element_factory_make("decodebin", "decodebin")
        self.colorspace = gst.element_factory_make("ffmpegcolorspace", "colorspace")
        self.vqueue = gst.element_factory_make("queue", "vqueue")
        self.videoscale = gst.element_factory_make("videoscale", "videoscale")

        self.src2 = gst.element_factory_make("filesrc", "src2")
        self.decodebin2 = gst.element_factory_make("decodebin", "decodebin2")
        self.colorspace2 = gst.element_factory_make("ffmpegcolorspace", "colorspace2")
        self.vqueue2 = gst.element_factory_make("queue", "vqueue2")
        self.videoscale2 = gst.element_factory_make("videoscale", "videoscale2")

        self.mixer = gst.element_factory_make("videomixer", "mixer")
        self.imagesink = gst.element_factory_make("ximagesink", "imagesink")

        self.pipeline.add(self.src, self.decodebin, self.colorspace, \
                          self.vqueue, self.videoscale, \
                          self.src2, self.decodebin2, self.colorspace2, \
                          self.vqueue2, self.videoscale2, \
                          self.mixer, self.imagesink)

        self.src.set_property("location", filesrc)
        self.src2.set_property("location", "/home/luisbg/Desktop/poolSkating02.mov")

        self.decodebin.connect("new-decoded-pad", self.OnDynamicPad)
        self.src.link(self.decodebin)
        self.decodebin2.connect("new-decoded-pad", self.OnDynamicPad)
        self.src2.link(self.decodebin2)
	
	self.vqueue.set_property ("max-size-buffers", 3)
        self.colorspace.link(self.vqueue)
	self.vqueue2.set_property ("max-size-buffers", 3)
        self.colorspace2.link(self.vqueue2)

        self.vqueue.link(self.videoscale)
        self.vqueue2.link(self.videoscale2)

        self.spad = self.videoscale.get_static_pad('src')
        self.dpad = self.mixer.get_request_pad('sink_%d')
        self.spad2 = self.videoscale2.get_static_pad('src')
        self.dpad2 = self.mixer.get_request_pad('sink_%d')

        self.spad.link(self.dpad)
        self.spad2.link(self.dpad2)

        self.imagesink.set_property("force-aspect-ratio", True)
        self.imagesink.set_property("handle-expose", True)

        self.conv = gst.element_factory_make("ffmpegcolorspace", "conv")
        self.pipeline.add(self.conv)

        self.mixer.link(self.conv)
        self.conv.link(self.imagesink)

        self.control = gst.Controller(self.dpad, "alpha")
        self.control.set_interpolation_mode("alpha", gst.INTERPOLATE_LINEAR)

        self.control2 = gst.Controller(self.dpad2, "alpha")
        self.control2.set_interpolation_mode("alpha", gst.INTERPOLATE_LINEAR)

        self.control.set("alpha", 0, 0.5)
        self.control2.set("alpha", 0, 0.5)
 
        self.first = True
        self.link = True
        self.pipeline.set_state(gst.STATE_PAUSED)

    def OnDynamicPad(self, dbin, pad, islast):
        if self.link:
            print "*************** ONE"
            pad.link(self.colorspace.get_pad("sink"))
            self.link = False
        else:
            print "*************** TWO"
            pad.link(self.colorspace2.get_pad("sink"))
            self.AsyncDone()
        print "OnDynamicPad called"

    def AsyncDone(self):
        print self.pipeline.seek (1.0, gst.FORMAT_TIME, \
            gst.SEEK_FLAG_SEGMENT | gst.SEEK_FLAG_FLUSH | gst.SEEK_FLAG_ACCURATE, \
            gst.SEEK_TYPE_SET, 0, gst.SEEK_TYPE_NONE, 0)
        print "Async"

    def SeekToLocation(self, location):
        self.pipeline.seek (1.0, gst.FORMAT_TIME, \
            gst.SEEK_FLAG_SEGMENT | gst.SEEK_FLAG_ACCURATE, \
            gst.SEEK_TYPE_SET, 0, gst.SEEK_TYPE_NONE, location)
        print "seek to %r" % location


if __name__ == "__main__":
    import os, optparse

    usage = """ flickbook -i [file]"""

    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-i", "--input", action="store", type="string", dest="input", help="Input video file", default="")
    (options, args) = parser.parse_args()

    print "Playing: %r" % options.input

    engine = Engine(options.input)
    gobject.MainLoop().run()
