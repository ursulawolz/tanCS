#!/usr/bin/env python

import pygtk
pygtk.require("2.0")
import gtk
import gtksourceview2

class SyntaxTest(object):       
	def __init__(self):
	    builder = gtk.Builder()
	    builder.add_from_file("gladetest.glade")
	    builder.connect_signals({ "on_window_destroy" : gtk.main_quit })
	    self.window = builder.get_object("window")
	    self.window.show()

	    self.scroll = builder.get_object("scrolledwindow1")
	    
	    #self.box = builder.get_object("vbox2")

	    #self.sview = builder.get_object("sview")
	    #self.sbuff = builder.get_object("textbuffer1")
	    
	    self.sbuff = gtksourceview2.Buffer()
	    self.sview = gtksourceview2.View(self.sbuff)
	    #self.sbuff.set_highlight(True)
	    self.lang = gtksourceview2.language_manager_get_default().get_language('python')
	    self.sbuff.set_language(self.lang)
	    gtk.ScrolledWindow.add(self.scroll,self.sview)
	    #self.box.pack_start(self.sview,True,True,0)
	    self.sbuff.set_text('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed et enim vitae augue dictum vehicula. Duis sit amet velit ipsum. Donec nibh leo, blandit et porttitor quis, aliquet sed est. Nam mollis pellentesque orci id pharetra. Curabitur eros arcu, mollis in ultricies nec, convallis a risus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Ut pharetra leo quis risus volutpat porta. Praesent bibendum mi nec erat scelerisque vitae pellentesque massa eleifend. Aliquam aliquet venenatis odio id hendrerit. Nulla accumsan tincidunt mauris, nec mollis justo feugiat sit amet. Nullam quis sagittis neque. Integer dui augue, molestie vel semper at, iaculis sed metus. Mauris tempor nibh quis sem pellentesque vulputate. Nullam varius magna rhoncus lectus tempor at viverra tellus pretium.')
	    self.sview.set_insert_spaces_instead_of_tabs(True)
	    self.sview.show()
	    #sbuffer = self.sview.get_source_buffer()
	    #print self.sbuff.get_language().get_name()


if __name__ == "__main__":
	app = SyntaxTest()
	gtk.main()