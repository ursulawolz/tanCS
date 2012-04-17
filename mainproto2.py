###------------------------------Inclusions--------------------------------###
from gi.repository import Gtk,GObject
from gi.repository import Gdk
import viewerproto2 as viewer
import editortest as editor
import explorerproto2 as explorer

class tanCS(object):

	def __init__(self):
		win=viewer.TempWindow(self)
		win.connect("delete-event",Gtk.main_quit)
		win.show_all()

		self.borrows=[]

		Gtk.main()

	###-------------------------------MAIN SWITCH------------------------------###
	def on_window_mode_changed(self,new_window_name,parent_window):
		if new_window_name==("Viewer"):
			window=viewer.TempWindow(self)
			window.connect("delete-event",Gtk.main_quit)
			window.show_all()
		if new_window_name==("Explorer"):
			window=explorer.explorer_window(self)
			window.connect("delete-event",Gtk.main_quit)
			window.show_all()
		if new_window_name==("Editor"):
			window=editor.Editor(self)
			window.connect("delete-event",Gtk.main_quit)
			window.show_all()
		parent_window.destroy()

	###-----------------------------------MAIN---------------------------------###
	
a=tanCS()