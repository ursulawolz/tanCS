###------------------------------Inclusions--------------------------------###

from gi.repository import Gtk,GObject
from gi.repository import Gdk
class TempWindow(Gtk.Window):

###------------------------------Construction------------------------------###

	def __init__(self):
		Gtk.Window.__init__(self,title="Entry Demo")

		color=Gdk.Color(1000,1000,1000)
		self.x=840
		self.y=280
		self.set_size_request(self.x,self.y)
		self.timeout_id=None

		#self.image=Gtk.Image()
		#self.image=Gtk.set_from_image("side.jpg")
		imagebox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=50)
		self.image2=Gtk.Image.new_from_file("/home/brendan/Desktop/softdev/side.jpg")
		self.image=Gtk.Image.new_from_file("/home/brendan/Desktop/softdev/sideb.jpg")
		
		imagebox.pack_start(self.image,False,False,0)
		imagebox.pack_start(self.image2,False,False,0)

		imageframe=Gtk.Frame()
		imageframe.add(imagebox)

		toplevel=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
		toplevel.set_size_request(self.x,self.y)
		self.add(toplevel)
		toplevel.pack_start(imageframe,True,True,0)
		
		vbox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
		#self.add(vbox)
	
		f=open("testingtk3.py")
		

		self.thecode=Gtk.TextView()
		self.thecodebuffer=self.thecode.get_buffer()
		self.thecodebuffer.set_text(f.read())
		self.thecode.set_size_request(self.x-150,560)
		codescroll=Gtk.ScrolledWindow()
		codescroll.add_with_viewport(self.thecode)
		codescroll.set_size_request(self.x-150,400)	
		vbox.pack_start(codescroll,False,False,0)	

		hbox=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
		
		self.listbutton=Gtk.ToggleButton("List")
		self.linebutton=Gtk.ToggleButton("Line")
		
		self.listbutton.connect("toggled", self.on_List_toggled, "List")
		self.linebutton.connect("toggled", self.on_Line_toggled, "Line")
		hbox.pack_end(self.listbutton,False, False,0)
		hbox.pack_end(self.linebutton,False, False,0)

		#vbox.pack_start(hbox, False, False,0)

		commentswindow = Gtk.ScrolledWindow()
		commentswindow.set_size_request(200,100)
		commentswindow.set_hexpand(True)
		commentswindow.set_vexpand(True)
		
		self.label2=Gtk.Label("I see how you have added many buttons. Is there anyway to dynamically create widgets?",halign=Gtk.Align.START)
		self.label2.set_justify(Gtk.Justification.RIGHT)
		self.label3=Gtk.Label("Well, yes and no. Its a little hard but you can definitely do it.",halign=Gtk.Align.START)
		self.label4=Gtk.Label("Thank you for the help. Also I saw that there are some variables that just seem to come out of nowhere, \n like 'clicked' and 'label'. Where do these come from?",halign=Gtk.Align.START)
		self.label5=Gtk.Label("They are variables that Gtk has included in it. When you import they get recognized.",halign=Gtk.Align.START)

		frame=Gtk.Frame()
		frame2=Gtk.Frame()
		frame3=Gtk.Frame()
		frame4=Gtk.Frame()
		frame5=Gtk.Frame()

		frame2.add(self.label2)
		frame3.add(self.label3)
		frame4.add(self.label4)
		frame5.add(self.label5)

		title2=Gtk.Label("<b>Code-11</b>")
		title3=Gtk.Label("<b>The Instigat0r</b>")
		title4=Gtk.Label("<b>Code-11</b>")
		title5=Gtk.Label("<b>The Instigat0r</b>")

		title2.set_use_markup(True)
		title3.set_use_markup(True)
		title4.set_use_markup(True)
		title5.set_use_markup(True)

		frame2.set_label_widget(title2)
		frame3.set_label_widget(title3)
		frame4.set_label_widget(title4)
		frame5.set_label_widget(title5)

		vbox2=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		vbox2.pack_start(frame2,False,False,0)
		vbox2.pack_start(frame3,False,False,0)
		vbox2.pack_start(frame4,False,False,0)
		vbox2.pack_start(frame5,False,False,0)

		#vbox2.pack_start(hbox,False,False,0)
		
		commentswindow.add_with_viewport(vbox2)
		commentswindow.set_size_request(self.x-150,240)
		commentbox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		commentbox.pack_start(hbox,False,False,0)
		commentbox.pack_start(commentswindow,False,False,0)
		frame.add(commentbox)

		hbox2=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
		self.entry=Gtk.Entry()
		self.entry.set_text("Thanks a bunch!")
		self.entry.set_size_request(self.x-150,100)
		self.submitcomment=Gtk.Button("Submit")
		hbox2.pack_start(self.entry,True,True,0)
		hbox2.pack_start(self.submitcomment,False,False,0)
		
		vbox.pack_start(frame,False,False,0)
		vbox.pack_start(hbox2,False,False,0)

		toplevel.pack_start(vbox,False,False,0)

###---------------------------------METHODS--------------------------------###

#Should unpackage the code from how ever it is stored in the revision and make a text buffer out of it so that it can be displayed later in a text view.  	
	def get_code(revision):
		return textbuffer

#should unpack the comments from where they are in revision and make a list of all the file comments so that they can be displayed.
	def get_file_comments(revision):
		return filecommentlist

#should unpack the line comments from where they are in revision and make a list of all of them so that they can be displayed.
	def get_line_comments(revision):
		return linecommentlist

# Not quite sure how to do this one. It needs to dynamically create a revision map for the whole project and allow you to move from one revision to another as well as load those revision. 
	def create_revision_map():
		return notsure	
#What happens when you click on the list comments only button
	def on_List_toggled(self,button,which):
		print(which)

#What happens when you click on the file comments only button
	def on_Line_toggled(self,button,which):
		print(which)

#How the user creates line comments. Should involve clicking on the line or something like that. So this will get called by a button I think.Should add a line comment to the code.
	def submit_line_comment():
		return

#How the user creates file comments. This involves just typing what the comment is in the gtkentry at the bottom. When they hit submit this function will be called and this will add a file comment to the code.
	def submit_file_comment():
		return

###------------------------------MAIN------------------------------###

win=TempWindow()
win.connect("delete-event",Gtk.main_quit)
win.show_all()
Gtk.main()		
