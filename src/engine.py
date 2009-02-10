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

"""freemix engine class"""

import gobject
gobject.threads_init() 
import gst
import time

class Engine:
    '''freemix engine class. Encapsulates all the core gstreamer work
       in nice function per feature for the frontend.''' 

    def __init__(self):
        self.running = False
        # print "init engine"
        self.speed = 1.0

    def start(self, filesrc):
        self.running = True 

        def bus_handler(unused_bus, message):
            # print message.type
            if message.type == gst.MESSAGE_SEGMENT_DONE:
                self.SeekToLocation(0)
            if message.type == gst.MESSAGE_EOS:
                self.AsyncDone()
            if message.type == gst.MESSAGE_TAG:
                self.SeekToLocation(0)
            if message.type == gst.MESSAGE_ERROR:
                print "ERROR"
            return gst.BUS_PASS

        # create our pipeline
        self.pipeline = gst.Pipeline()
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect ('message', bus_handler)

        self.bin1 = self.VideoBin(filesrc)

        self.imagesink = gst.element_factory_make("xvimagesink", "imagesink")
        self.imagesink.set_property("force-aspect-ratio", True)
        self.imagesink.set_property("handle-expose", True)
        self.pipeline.add(self.bin1, self.imagesink)

        self.bin1.link(self.imagesink)

        self.first = True
        self.pipeline.set_state(gst.STATE_PLAYING)

    def VideoBin(self, filesrc):
        self.bin = gst.Bin()
        self.src = gst.element_factory_make("filesrc", "src")
        self.bin.add(self.src)
        self.src.set_property("location", filesrc)
        
        self.decodebin = gst.element_factory_make("decodebin", "decodebin")
        self.decodebin.connect("new-decoded-pad", self.OnDynamicPad)
        self.bin.add(self.decodebin)
        
        self.src.link(self.decodebin)

        self.colorspace = gst.element_factory_make("ffmpegcolorspace", "colorspace")

        self.vqueue = gst.element_factory_make("queue", "vqueue")
	self.vqueue.set_property ("max-size-buffers", 3)
        
        self.videoscale = gst.element_factory_make("videoscale", "videoscale")

        self.bin.add(self.colorspace, self.vqueue, self.videoscale)

        self.colorspace.link(self.vqueue)
        self.vqueue.link(self.videoscale)

        target = self.videoscale.get_pad("src")
        self.sinkpad = gst.GhostPad("sink", target)
        self.sinkpad.set_active(True)
        self.bin.add_pad(self.sinkpad)
 
        return self.bin

    def OnDynamicPad(self, dbin, pad, islast):
        pad.link(self.colorspace.get_pad("sink"))
        # print "OnDynamicPad called"

    def AsyncDone(self):
        seek = self.pipeline.seek (self.speed, gst.FORMAT_TIME, \
            gst.SEEK_FLAG_SEGMENT | gst.SEEK_FLAG_FLUSH | gst.SEEK_FLAG_ACCURATE, \
            gst.SEEK_TYPE_SET, 0, gst.SEEK_TYPE_NONE, 0)
        # print "Async " + str(self.speed) 

    def SeekToLocation(self, location):
        self.pipeline.seek(self.speed, gst.FORMAT_TIME, \
            gst.SEEK_FLAG_SEGMENT, gst.SEEK_TYPE_SET, 0, gst.SEEK_TYPE_NONE, \
            location)
        # print "seek to %r" % location

    def switchVideo(self, filesrc):
        self.pipeline.set_state(gst.STATE_READY)
        self.src.set_property("location", filesrc)
        self.pipeline.set_state(gst.STATE_PLAYING)
        self.SeekToLocation(0)

    def play(self, filesrc, speed):
        # print "engine got call to play: " + filesrc
        self.speed = speed
        if self.running == False:
           self.start(filesrc)
        else:
           self.switchVideo(filesrc) 


if __name__ == "__main__":
    import os, optparse

    usage = """ engine.py -i [file]"""

    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-i", "--input", action="store", type="string", dest="input", help="Input video file", default="")
    (options, args) = parser.parse_args()

    print "Playing: %r" % options.input

    engine = Engine(options.input)
    gobject.MainLoop().run()
