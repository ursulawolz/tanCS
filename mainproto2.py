###------------------------------Inclusions--------------------------------###
from gi.repository import Gtk,GObject
from gi.repository import Gdk
import viewerproto2 as viewer
import editortest as editor
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
def on_menu_mode_changed(widget,current,parent_window):
	print widget
	print current
	print parent_window
	new_window_name=current.get_name()
	if new_window_name==("Viewer"):
		window=viewer.TempWindow(UI_INFO,on_menu_mode_changed)
		window.connect("delete-event",Gtk.main_quit)
		window.show_all()
	if new_window_name==("Explorer"):
		window=viewer.TempWindow(UI_INFO,on_menu_mode_changed)
		window.connect("delete-event",Gtk.main_quit)
		window.show_all()
	if new_window_name==("Editor"):
		window2=editor.Editor(UI_INFO,on_menu_mode_changed)
		window2.connect("delete-event",Gtk.main_quit)
		window2.show_all()

	parent_window.destroy()	
	
	#print current.get_name() + " was selected."
###-----------------------------------MAIN---------------------------------###

#Could instantiating here be the problem?
win=viewer.TempWindow(UI_INFO,on_menu_mode_changed)
win.connect("delete-event",Gtk.main_quit)
win.show_all()
Gtk.main()	
