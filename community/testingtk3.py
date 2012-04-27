from gi.repository import Gtk
class GridWindow(Gtk.Window): 
	def callback(self, widget, data):
		print "Hello again - %s was pressed" % data
	def __init__(self):
		Gtk.Window.__init__(self, title="Grid Example")
		grid=Gtk.Grid()
		self.add(grid)
		
		button1=Gtk.Button(label="Button 1")
		button2=Gtk.Button(label="Button 2")
		button3=Gtk.Button(label="Button 3")
		button4=Gtk.Button(label="Button 4")
		button5=Gtk.Button(label="Button 5")
		button6=Gtk.Button(label="Button 6")
		
		label=Gtk.Label("This is a normal label")
		label.set_markup("Go to <a href=\"http://calvin.olin.edu\" title=\"Our website\">Tancs website</a>")

		

		button1.connect("clicked", self.callback, "button 1")
		button2.connect("clicked", self.callback, "button 2")
		button3.connect("clicked", self.callback, "button 3")
		button4.connect("clicked", self.callback, "button 4")
		button5.connect("clicked", self.callback, "button 5")
		button6.connect("clicked", self.callback, "button 6")

		grid.add(button1)
		grid.attach(button2,1,0,2,1)
		grid.attach_next_to(button3,button1,Gtk.PositionType.BOTTOM,1,2)
		grid.attach_next_to(button4,button3,Gtk.PositionType.RIGHT,1,2)
		grid.attach_next_to(button5,button4,Gtk.PositionType.RIGHT,1,1)
		grid.attach_next_to(button6,button5,Gtk.PositionType.BOTTOM,1,1)
		grid.attach_next_to(label,button2,Gtk.PositionType.RIGHT,1,1)
		
win=GridWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()

