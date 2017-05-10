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
        gtk.Window.set_title(self, "Logbuch des Captains")
        gtk.Window.set_default_size(self, 600, 400)
        self.set_border_width(10)
        self.mainbox = gtk.Box(orientation=gtk.Orientation.HORIZONTAL)
        self.add(self.mainbox)

        self.leftbox = gtk.Box(orientation=gtk.Orientation.VERTICAL)
        self.mainbox.pack_start(self.leftbox, True, True, 0)

        self.rightbox = gtk.Box(orientation=gtk.Orientation.VERTICAL)
        self.mainbox.pack_start(self.rightbox, True, True, 0)

        # create label
        self.label = gtk.Label()
        self.label.set_markup("<b>Neuer Eintrag</b>")
        self.leftbox.pack_start(self.label, True, True, 0)

        self.entry = gtk.Entry()
        self.leftbox.pack_start(self.entry, True, True, 0)

        # create button1
        self.button1 = gtk.Button(label="Save")
        self.button1.connect('clicked', self.__change_label)
        self.leftbox.pack_start(self.button1, True, True, 0)

        # create button2
        self.button2 = gtk.Button(label="Quit")
        self.button2.connect("clicked", gtk.main_quit)
        self.leftbox.pack_start(self.button2, True, True, 0)

        self.store = gtk.ListStore(str, str)
        self.store.append(("First", "Entry 1"))
        self.store.append(("Second", "Entry 2"))
        self.store.append(("Third", "Entry 3"))

        self.__create_view()

    def __create_view(self):
        self.view = gtk.TreeView(self.store)
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Sternzeit', renderer, text=0)
        column.set_sort_column_id(0)
        self.view.append_column(column)

        column = gtk.TreeViewColumn('Eintrag', renderer, text=1)
        self.view.append_column(column)

        self.rightbox.pack_start(self.view, True, True, 0)

    def __change_label(self, widget):
        self.store.append(("neu", self.entry.get_text()))


logBookWindow = LogBookWindow()
logBookWindow.connect('delete-event', gtk.main_quit)
logBookWindow.show_all()
gtk.main()
