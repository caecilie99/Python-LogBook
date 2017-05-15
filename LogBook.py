#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sqlite3
from time import strftime, gmtime
from gi import require_version

require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk


class LogBookWindow(gtk.Window):
    '''
    main window for logbook
    '''

    def __init__(self):
        # init window
        gtk.Window.__init__(self)

        # set tittle & size for window
        gtk.Window.set_title(self, "Logbuch der USS Enterprise")
        gtk.Window.set_default_size(self, 600, 400)
        self.set_border_width(10)

        # load css-style
        self.__load_style()

        # create grid for grid layout
        self.mainGrid = gtk.Grid()
        self.add(self.mainGrid)

        # create label for iinput field
        self.label = gtk.Label()
        self.label.set_markup("<b>Your entry</b>")
        # add label to maingrid
        self.mainGrid.add(self.label)

        # create input field for logbook entry
        self.entry = gtk.Entry()
        # attach
        self.mainGrid.attach(self.entry, 0, 1, 1, 1)

        # create save-button
        self.btn_save = gtk.Button(label="Save")
        self.btn_save.connect('clicked', self.__new_entry)
        self.mainGrid.attach(self.btn_save, 1, 1, 1, 1)

        # create quit-button
        self.btn_quit = gtk.Button(label="Quit")
        self.btn_quit.connect("clicked", self.quit)
        self.mainGrid.attach(self.btn_quit, 2, 1, 1, 1)

        # create liststore to save entries
        self.store = gtk.ListStore(str, str)

        # connect db
        self.__connect_db()
        # load data from db
        self.__load_data_from_db()

        # create list view
        self.__create_view()

    def __load_style(self):
        '''
        load css-file and set styling for window
        :return:
        '''
        # read css setting from file
        css = open('./style.css', 'rb')
        css_data = css.read()
        css.close()

        # create CssProvider
        style_provider = gtk.CssProvider()
        # set css-stylings to style_provider
        style_provider.load_from_data(css_data)
        # add provider to screen
        gtk.StyleContext.add_provider_for_screen(
        gdk.Screen.get_default(), style_provider,
        gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def __create_view(self):
        '''
        create tree view to show entries from logbook
        :return:
        '''
        # create tree view
        self.view = gtk.TreeView(self.store)
        # set renderer
        renderer = gtk.CellRendererText()
        # create column
        column = gtk.TreeViewColumn('Sternzeit', renderer, text=0)
        # set sort
        column.set_sort_column_id(0)
        # add column to view
        self.view.append_column(column)
        # create next column
        column = gtk.TreeViewColumn('Eintrag', renderer, text=1)
        # add column to view
        self.view.append_column(column)
        # add view to main grid
        self.mainGrid.attach(self.view, 0, 2, 3, 4)

    def __new_entry(self, widget):
        '''

        :param widget:
        :return:
        '''

        # create timestamp
        tmp_time = strftime('%d.%m.%Y %H:%M:%S', gmtime())
        # get text from input
        tmp_text = self.entry.get_text()
        # append entry to store
        self.store.append((tmp_time, tmp_text))
        # inssert entry in db
        self.cur.execute('INSERT INTO logbook VALUES (?,?)', (tmp_time, tmp_text))
        self.conn.commit()

    def __connect_db(self):
        '''
        connect to db
        :return:
        '''
        # set current directory to dbpath
        self.dbPath = os.path.abspath(os.curdir)
        # set sqlite connection
        self.conn = sqlite3.connect(self.dbPath + '/USSEnterprise.db')
        # create cursor
        self.cur = self.conn.cursor()
        # create table if not exists
        self.cur.execute('CREATE TABLE IF NOT EXISTS logbook (sternzeit VARCHAR(32), logeintrag VARCHAR(512))')
        self.conn.commit()

    def __load_data_from_db(self):
        '''
        load all entries from db, add entries to store
        :return:
        '''
        # load entries from db
        log_etnries = self.cur.execute('SELECT * FROM logbook')
        # add all entries to store
        for ds in log_etnries:
            self.store.append((ds[0], ds[1]))

    def __disconnect(self):
        '''
        close db connection
        :return:
        '''
        self.conn.close()

    def main_quit(self, widget, event):
        '''
        close db-connection and quit
        :param event:
        :param data:
        :return:
        '''
        self.__disconnect()
        gtk.main_quit()

    def quit(self, widget):
        '''
        close db-connection and quit
        :param event:
        :param data:
        :return:
        '''
        self.__disconnect()
        gtk.main_quit()

logBookWindow = LogBookWindow()
logBookWindow.connect('delete-event', logBookWindow.main_quit)
logBookWindow.show_all()
gtk.main()
