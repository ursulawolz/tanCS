from gi.repository import Gtk,GObject
from gi.repository import Gdk
class TempWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self,title="Entry Demo")

		color=Gdk.Color(1000,1000,1000)
		self.x=640
		self.y=280
		self.set_size_request(self.x,self.y)
		self.timeout_id=None

		#self.image=Gtk.Image()
		#self.image=Gtk.set_from_image("side.jpg")
		imagebox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=50)
		self.image2=Gtk.Image.new_from_file("/home/brendan/Desktop/softdev/side.jpg")
		self.image=Gtk.Image.new_from_file("/home/brendan/Desktop/softdev/side.jpg")
		
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
	
		self.thecode=Gtk.TextView()
		self.thecodebuffer=self.thecode.get_buffer()
		self.thecodebuffer.set_text("code code code code code code code \n code code code code code code code \n code code code code code code code \n code code code code code code code \n code code code code code code code \n code code code code code code code \n code code code code code code code \n code code code code code code code \n code code code code code code code \n code code code code code code code \n code code code code code code code \n code code code code code code code \n code code code code code code code \n code code code code code code code \n code code code code code code code \n code code code code code code code \n code code code code code code code \n code code code code code code code \n code code code code code code code \n code code code code code code code \n code code code code code code code \n code code code code code code code \n code code code code code code code \n code code code code code code code \n code code code code code code code \n code code code code code code code \n code code code code code code code \n code code code code code code code \n code code code code code code code \n code code code code code code code \n code code code code code code code \n code code code code code code code \n code code code code code code code \n code code code code code code code \n code code code code code code code \n")
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

		self.label2=Gtk.Label("Blah")
		self.label3=Gtk.Label("THINGS")
		self.label4=Gtk.Label("This is a very long and annoying line of code. It will obviously not fit nicely on one line of code. Thus your program will break and you will cry. Longer and longer it goes.  Stretching out the widow and making your day change from a pleasant  ride in the country to a hellish nightmare filled with your darkest fears.")
		self.label5=Gtk.Label("This is another longish line of code to see things.")

		frame=Gtk.Frame()
		frame2=Gtk.Frame()
		frame3=Gtk.Frame()
		frame4=Gtk.Frame()
		frame5=Gtk.Frame()

		frame2.add(self.label2)
		frame3.add(self.label3)
		frame4.add(self.label4)
		frame5.add(self.label5)

		vbox2=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		vbox2.pack_start(frame2,True,True,0)
		vbox2.pack_start(frame3,True,True,0)
		vbox2.pack_start(frame4,True,True,0)
		vbox2.pack_start(frame5,True,True,0)

		#vbox2.pack_start(hbox,False,False,0)
		
		commentswindow.add_with_viewport(vbox2)
		commentswindow.set_size_request(self.x-150,240)
		commentbox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		commentbox.pack_start(hbox,False,False,0)
		commentbox.pack_start(commentswindow,False,False,0)
		frame.add(commentbox)

		hbox2=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
		self.entry=Gtk.Entry()
		self.entry.set_text("Add a comment")
		self.entry.set_size_request(self.x-150,100)
		self.submitcomment=Gtk.Button("Submit")
		hbox2.pack_start(self.entry,True,True,0)
		hbox2.pack_start(self.submitcomment,False,False,0)



		#self.e=Gtk.Entry()
		#self.e.foreground=Gtk.gdk.color_parse("#0000FF")
		#style=self.e.get_style().copy()
		#style.bg[Gtk.STATE_NORMAL]=self.e.get_colormap().alloc_color("#FF9999")
		#self.e.set_style(style)

		#vbox2.packstart(self.e,True,True,0)
		
		vbox.pack_start(frame,False,False,0)
		vbox.pack_start(hbox2,False,False,0)

		toplevel.pack_start(vbox,False,False,0)

	def on_List_toggled(self,button,which):
		print(which)

	def on_Line_toggled(self,button,which):
		print(which)

win=TempWindow()
win.connect("delete-event",Gtk.main_quit)
win.show_all()
Gtk.main()		
