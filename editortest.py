#!/usr/bin/env python
from gi.repository import Gtk, Gdk, GtkSource


class MyWindow(Gtk.Window):
	def __init__(self):
		'''
		Gtk.Window.__init__(self,title="Editor")

		self.button=Gtk.Button(label="Click Here")
		self.button.connect("clicked",self.on_button_clicked)
		self.add(self.button)
		'''
		#import glade file and initiate window
		self.builder=Gtk.Builder()
		self.builder.add_from_file("gladetest.glade")
		self.builder.connect_signals({ "on_window_destroy" : Gtk.main_quit })
		self.window = self.builder.get_object("window")
		self.window.show()
		self.scroll = self.builder.get_object("scrolledwindow1")
		
		#create gtksourceview objects
		self.sbuff = GtkSource.Buffer()
		self.sview = GtkSource.View()
		self.sview.set_buffer(self.sbuff)

		#set syntax highlighting to python
		self.lang = GtkSource.LanguageManager.get_default().get_language('python')
		self.sbuff.set_language(self.lang)

		#add sourceview to window and initialize properties
		Gtk.ScrolledWindow.add(self.scroll,self.sview)
		self.sbuff.set_text('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed et enim vitae augue dictum vehicula. Duis sit amet velit ipsum. Donec nibh leo, blandit et porttitor quis, aliquet sed est. Nam mollis pellentesque orci id pharetra. Curabitur eros arcu, mollis in ultricies nec, convallis a risus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Ut pharetra leo quis risus volutpat porta. Praesent bibendum mi nec erat scelerisque vitae pellentesque massa eleifend. Aliquam aliquet venenatis odio id hendrerit. Nulla accumsan tincidunt mauris, nec mollis justo feugiat sit amet. Nullam quis sagittis neque. Integer dui augue, molestie vel semper at, iaculis sed metus. Mauris tempor nibh quis sem pellentesque vulputate. Nullam varius magna rhoncus lectus tempor at viverra tellus pretium.')
		self.sview.show()
		self.sview.connect("key-press-event",self.on_key_press)

		#playing around with colors
		'''
		self.sview.modify_base(Gtk.StateType.NORMAL,Gdk.Color(0x00,0x00,0xff))
		
		#make a gdk.color for red
		#self.map1 = gtk.gdk.Colormap(gtk.gdk.visual_get_system(),True)
		self.color=Gdk.Color(9,50,30);
		self.color.red = 0x00C0;
		self.color.green = 0x00DE;
		self.color.blue = 0x00ED;
		#self.color = self.map1.alloc_color("red")

		#copy the current style and replace the background
		self.style = self.sview.get_style().copy()
		self.style.bg[0] = self.color

		#set the button's style to the one you created
		self.sview.set_style(self.style)'''



	def on_key_press(self,widget,data):
		#runs when any key is pressed

		#Space is 32
		#Tab is 65289
		#Backspace is 65288
		#Enter is 65293
		val=data.keyval #get the pressed key
		cursor=self.sbuff.get_iter_at_mark(self.sbuff.get_insert()) #get iter at cursor position
		back=self.sbuff.get_iter_at_offset(cursor.get_offset()-1) #get iter at cursor position-1
		if val==65289: #tab key
			self.sbuff.insert(cursor,'    ') #insert 4 spaces
			return True #repress normal tab key
		elif val==65288: #backspace key
			if self.sbuff.get_selection_bounds()==(): #if no text is selected
				backfour=self.sbuff.get_iter_at_offset(cursor.get_offset()-4) #get iter at cursor position-4
				txt=self.sbuff.get_text(backfour,cursor,True) #get preceding 4 characters
				if txt=='    ': #if preceding text is 4 spaces
					self.sbuff.delete(backfour,cursor) #delete the preceding "tab"
				else:
					self.sbuff.delete(back,cursor) #normal backspace
				return True #repress normal backspace key
			else:
				return False
		elif val==65293: #enter key
			indent=self.check_indent(cursor) #check how far the previous line was indented
			if self.check_colon(cursor): #check if previous line ended in colon
				spaces='    '*(indent+1) #auto-indent block
			else:
				spaces='    '*indent #match indent

			self.sbuff.insert(cursor,'\n'+spaces) #insert appropriate number of "tabs"

			return True #repress normal enter key

	def check_colon(self,cursor):
		#check if previous line ended in a colon
		offset=cursor.get_offset()
		back=self.sbuff.get_iter_at_offset(offset-1)
		if self.sbuff.get_slice(back,cursor,True)==':': #TODO: what if whitespace?
			return True
		else:
			return False

	def check_indent(self,cursor):
		#check how far the previous line was indented
		txt=' '
		i=0
		offset=cursor.get_offset()
		
		#find the start of the line
		while not (txt == ('\n' or '\r') or (offset-i)<1):
			backa=self.sbuff.get_iter_at_offset(offset-i)
			backb=self.sbuff.get_iter_at_offset(offset-i-1)
			txt=self.sbuff.get_slice(backb,backa,True)
			i+=1
		if txt=='\n':
			offset=backa.get_offset()
		else:
			offset=0

		#count number of 4-space strings at start of line
		i=0
		indent=0
		backa=self.sbuff.get_iter_at_offset(offset)
		backb=self.sbuff.get_iter_at_offset(offset+4)
		txt=self.sbuff.get_slice(backa,backb,True)
		while txt == '    ':
			indent+=1
			i+=1
			backa=self.sbuff.get_iter_at_offset(offset+4*i)
			backb=self.sbuff.get_iter_at_offset(offset+4*i+4)
			txt=self.sbuff.get_slice(backa,backb,True)
		return indent

	def on_button_clicked(self,widget):
		print "Hello World" #test func

#initiate window
win = MyWindow()
#win.connect("delete-event",Gtk.main_quit)
win.show_all()
Gtk.main()