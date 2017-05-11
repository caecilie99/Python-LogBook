#!/usr/bin/python
# -*- coding: utf-8 -*-

from gi import require_version

require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk


class LogBookWindow(gtk.Window):
    '''
    main window for logbook
    '''

    def __init__(self):
        gtk.Window.__init__(self)
        gtk.Window.set_title(self, "Dat issen Test")
        gtk.Window.set_default_size(self, 600, 400)
        self.set_border_width(10)
        self.mainGrid = gtk.Grid()
        self.add(self.mainGrid)

        # create label
        self.label = gtk.Label()
        self.label.set_markup("<b>Your entry</b>")
        self.mainGrid.attach(self.label)

        self.entry = gtk.Entry()
        self.mainGrid.attach(self.entry)

        # create button1
        self.button1 = gtk.Button(label="Save")
        self.button1.connect('clicked', self.change_label, self.entry)
        self.mainGrid.attach(self.button1)

        # create button2
        self.button2 = gtk.Button(label="Quit")
        self.button2.connect("clicked", gtk.main_quit)
        self.mainGrid.attach(self.button2)

    def change_label(self):
        self.label.set_markup(self.entry.g)


logBookWindow = LogBookWindow()
logBookWindow.connect('delete-event', gtk.main_quit)
logBookWindow.show_all()
gtk.main()
