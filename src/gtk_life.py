#!/usr/bin/python
"""
This file-module provides a view of the Conway "Game of Life" grid.
It uses the GTK user interface framework.
"""
import gtk
import gobject
 
import sys
 
import grid
 
class life_ui(object):
    cell_size =  16
    cell_border = 2
 
    def __init__(self, file_name):
 
        self.grid = grid.LifeGrid(file_name)
 
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title(file_name)
        self.window.connect('delete_event', self.program_exit)
        self.window.show()
 
        self.drawing = gtk.DrawingArea()
        self.drawing.set_size_request(self.
            grid.width * (self.cell_size + self.cell_border), 
            self.grid.height * (self.cell_size + self.cell_border))
        self.drawing.connect('expose-event', self.expose_cb)
        self.drawing.show()
 
 
        self.hbox = gtk.HBox()
        self.hbox.add(self.drawing)
        self.hbox.show()
 
        self.window.add(self.hbox)
 
        style = self.drawing.get_style()
        self.gc_on = style.fg_gc[gtk.STATE_NORMAL]
        self.gc_off = style.bg_gc[gtk.STATE_NORMAL]
 
    def expose_cb(self, window, event):
        self.draw_grid()
 
 
    def loop(self):
        gobject.timeout_add(1000, self.next_grid)
        gtk.main()
 
    def next_grid(self):
        self.grid = self.grid.nextGeneration()
        self.draw_grid()
        return True
 
    def draw_grid(self):
        for x in xrange(self.grid.width):
            for y in xrange(self.grid.height):
                self.draw_cell(x, y, self.grid.rows[y][x])
 
    def draw_cell(self, x, y, state):
        if state:
            gc = self.gc_on
        else:
            gc = self.gc_off
 
        self.drawing.window.draw_rectangle(gc, True, 
            x * (self.cell_size + self.cell_border), 
            y * (self.cell_size + self.cell_border), self.cell_size, self.cell_size)
     
 
    def program_exit(self, widget, event):
        gtk.main_quit()
        return False
 
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "gtk_life.py [file-name]"
        exit(0)
 
    game = life_ui(sys.argv[1])
    game.loop()
    
