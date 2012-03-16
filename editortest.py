#!/usr/bin/env python
from gi.repository import Gtk
#import gtksourceview2
from gi.repository import GtkSource


class MyWindow(Gtk.Window):
	def __init__(self):
		'''
		Gtk.Window.__init__(self,title="Editor")

		self.button=Gtk.Button(label="Click Here")
		self.button.connect("clicked",self.on_button_clicked)
		self.add(self.button)
		'''
		self.builder=Gtk.Builder()
		self.builder.add_from_file("../gladetest.glade")
		self.builder.connect_signals({ "on_window_destroy" : Gtk.main_quit })
		self.window = self.builder.get_object("window")
		self.window.show()
		self.scroll = self.builder.get_object("scrolledwindow1")
	    
		#self.box = builder.get_object("vbox2")

		#self.sview = builder.get_object("sview")
		#self.sbuff = builder.get_object("textbuffer1")

		self.sbuff = GtkSource.Buffer()
		self.sview = GtkSource.View()
		self.sview.set_buffer(self.sbuff)
		self.sview.set_auto_indent(True)
		####self.sbuff = self.sview.get_buffer() ###
		#self.sbuff.set_highlight(True)
		self.lang = GtkSource.LanguageManager.get_default().get_language('python')
		self.sbuff.set_language(self.lang)
		Gtk.ScrolledWindow.add(self.scroll,self.sview)
		#self.box.pack_start(self.sview,True,True,0)
		self.sbuff.set_text('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed et enim vitae augue dictum vehicula. Duis sit amet velit ipsum. Donec nibh leo, blandit et porttitor quis, aliquet sed est. Nam mollis pellentesque orci id pharetra. Curabitur eros arcu, mollis in ultricies nec, convallis a risus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Ut pharetra leo quis risus volutpat porta. Praesent bibendum mi nec erat scelerisque vitae pellentesque massa eleifend. Aliquam aliquet venenatis odio id hendrerit. Nulla accumsan tincidunt mauris, nec mollis justo feugiat sit amet. Nullam quis sagittis neque. Integer dui augue, molestie vel semper at, iaculis sed metus. Mauris tempor nibh quis sem pellentesque vulputate. Nullam varius magna rhoncus lectus tempor at viverra tellus pretium.')
		#self.sview.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
		###self.sview.set_insert_spaces_instead_of_tabs(True)
		self.sview.show()
		#sbuffer = self.sview.get_source_buffer()
		#print self.sbuff.get_language().get_name()
		#self.window.set_events(Gtk.key_press_mask)
		self.sview.connect("key-press-event",self.on_key_press)

	def on_key_press(self,widget,data):
		#Space is 32
		#Tab is 65289
		#Backspace is 65288
		#Enter is 65293
		val=data.keyval
		cursor=self.sbuff.get_iter_at_mark(self.sbuff.get_insert())
		back=self.sbuff.get_iter_at_offset(cursor.get_offset()-1)
		if val==65289: #tab key
			self.sbuff.insert(cursor,'    ') #insert 4 spaces
			return True
		elif val==65288: #backspace key
			if self.sbuff.get_selection_bounds()==(): #if no text is selected
				backfour=self.sbuff.get_iter_at_offset(cursor.get_offset()-4)
				txt=self.sbuff.get_text(backfour,cursor,True)
				if txt=='    ':
					self.sbuff.delete(backfour,cursor) #delete the preceding tab
				else:
					self.sbuff.delete(back,cursor) #normal backspace
				print txt
				return True
			else:
				return False
		elif val==65293: #enter key
			indent=self.check_indent(cursor)
			if self.check_colon(cursor):
				spaces='    '*(indent+1)
			else:
				spaces='    '*indent

			self.sbuff.insert(cursor,'\n'+spaces)

			return True
		#print cursor.get_offset()
		#print back.get_offset()
		print data.keyval

	def check_colon(self,cursor):
		offset=cursor.get_offset()
		back=self.sbuff.get_iter_at_offset(offset-1)
		if self.sbuff.get_slice(back,cursor,True)==':': #what if whitespace?
			return True
		else:
			return False

	def check_indent(self,cursor):
		txt=' '
		i=0
		offset=cursor.get_offset()
		#print 'started'
		while not (txt == ('\n' or '\r') or (offset-i)<1):
			backa=self.sbuff.get_iter_at_offset(offset-i)
			backb=self.sbuff.get_iter_at_offset(offset-i-1)
			txt=self.sbuff.get_slice(backb,backa,True)
			i+=1
		if txt=='\n':
			offset=backa.get_offset()
		else:
			offset=0
		i=0
		indent=0
		backa=self.sbuff.get_iter_at_offset(offset)
		backb=self.sbuff.get_iter_at_offset(offset+4)
		txt=self.sbuff.get_slice(backa,backb,True)
		#print txt
		while txt == '    ':
			indent+=1
			i+=1
			backa=self.sbuff.get_iter_at_offset(offset+4*i)
			backb=self.sbuff.get_iter_at_offset(offset+4*i+4)
			txt=self.sbuff.get_slice(backa,backb,True)
		return indent

	def on_button_clicked(self,widget):
		print "Hello World"

win = MyWindow()
#win.connect("delete-event",Gtk.main_quit)
win.show_all()
Gtk.main()