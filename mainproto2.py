###------------------------------Inclusions--------------------------------###
from gi.repository import Gtk,GObject
from gi.repository import Gdk
import viewerproto2 as viewer
import editortest as editor
import explorerproto2 as explorer
import editornew as enew
###-------------------------------Menu UI----------------------------------###
UI_INFO="""
<ui>
	<menubar name='MenuBar'>
		<menu action='ModeMenu'>
			<menuitem action='Editor'/>
			<separator />
			<menuitem action='Viewer'/>
			<separator />
			<menuitem action='Explorer'/>
		</menu>
	</menubar>
</ui>

"""
###-------------------------------MAIN SWITCH------------------------------###
def on_window_mode_changed(new_window_name,parent_window):
	if new_window_name==("Viewer"):
		window=viewer.TempWindow(UI_INFO,on_window_mode_changed)
		window.connect("delete-event",Gtk.main_quit)
		window.show_all()
	if new_window_name==("Explorer"):
		window=explorer.explorer_window(UI_INFO,on_window_mode_changed)
		window.connect("delete-event",Gtk.main_quit)
		window.show_all()
	if new_window_name==("Editor"):
		window2=editor.Editor(UI_INFO,on_window_mode_changed)
		window2.connect("delete-event",Gtk.main_quit)
		window2.show_all()
	parent_window.destroy()

###-----------------------------------MAIN---------------------------------###

win=viewer.TempWindow(UI_INFO,on_window_mode_changed)
#win=editor.Editor(UI_INFO,on_window_mode_changed)
win.connect("delete-event",Gtk.main_quit)
win.show_all()
Gtk.main()
