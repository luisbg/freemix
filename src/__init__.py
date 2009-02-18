#!/usr/bin/python
#
# Copyright (c) 2009 Luis de Bethencourt <luisbg@ubuntu.com> 
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
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
# USA

"""
freemix is a free live video editing software, intended for and made by freedom loving live video artists.

Based on pygtk and gstreamer, freemix gives the video artist a videosources table and a sequencer to mix videos live. While handling the sequencer bpm, video pitch and much more.
"""

__author__ = "Luis de Bethencourt <luisbg@ubuntu.com>"
__copyright__ = "Luis de Bethencourt <luisbg@ubuntu.com>"
# Here you put the people who collaborate in the project
__credits__ = """
Luis de Bethencourt <luisbg@ubuntu.com>
Alberto Ruiz <aruiz@gnome.org>
Jan Schmidt <thaytan@noraisin.net>
Juanje Ojeda <jojeda@emergya.es>
"""
__license__ = "GPL-2"
__version__ = "0.2"

__all__ = ["freemix", "controller", "engine", "gui", "sequencer", "videosource"]

