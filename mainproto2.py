###------------------------------Inclusions--------------------------------###
from gi.repository import Gtk,GObject
from gi.repository import Gdk
import viewerproto2 as viewer
import editortest as editor
import explorerproto2 as explorer
###-------------------------------MAIN SWITCH------------------------------###
def on_window_mode_changed(new_window_name,parent_window):
	if new_window_name==("Viewer"):
		window=viewer.TempWindow(on_window_mode_changed)
		window.connect("delete-event",Gtk.main_quit)
		window.show_all()
	if new_window_name==("Explorer"):
		window=explorer.explorer_window(on_window_mode_changed)
		window.connect("delete-event",Gtk.main_quit)
		window.show_all()
	if new_window_name==("Editor"):
		window=editor.Editor(on_window_mode_changed)
		window.connect("delete-event",Gtk.main_quit)
		window.show_all()
	parent_window.destroy()

###-----------------------------------MAIN---------------------------------###
win=viewer.TempWindow(on_window_mode_changed)
win.connect("delete-event",Gtk.main_quit)
win.show_all()
Gtk.main()
