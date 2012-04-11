from gi.repository import Gtk,GObject
from gi.repository import Gdk

###------------------------Explorer Class--------------------------###
class explorer_window(Gtk.Window):
	def __init__(self, UI_INFO,on_window_mode_changed):
		Gtk.Window.__init__(self,title="Entry Demo")
		#action_group = Gtk.ActionGroup("my_actions")
		#add_mode_menu_actions(action_group,on_window_mode_changed,self)
		#uimanager = create_ui_manager(UI_INFO)
		#uimanager.insert_action_group(action_group)
		#menubar = uimanager.get_widget("/MenuBar")

		self.x=640
		self.y=280
		self.set_size_request(self.x,self.y)

		self.toplevel=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)

		self.quicknav=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

		self.tohome=Gtk.Label("Home")
		self.tomyaccount=Gtk.Label("My Account")
		self.tomygroups=Gtk.Label("My Groups")
		self.tosearch=Gtk.Label("Search")
		self.tohelp=Gtk.Label("Help")
		self.toggle=Gtk.Button("TOGGLE")

		self.quicknav.pack_start(self.tohome,True,True,0)
		self.quicknav.pack_start(self.tomyaccount,True,True,0)
		self.quicknav.pack_start(self.tomygroups,True,True,0)
		self.quicknav.pack_start(self.tosearch,True,True,0)
		self.quicknav.pack_start(self.tohelp,True,True,0)
		self.quicknav.pack_start(self.toggle,False,False,0)
		
		self.toplevel.pack_start(self.quicknav,False,False,0)
		self.current_page=self.make_search_results("type_results","identifier")

		#self.toggle.connect("clicked",self.new_page,self.current_page,self.toplevel)
		self.toggle.connect("clicked",self.change,on_window_mode_changed,'Editor')

		self.toplevel.pack_start(self.current_page,False,False,0)
		self.add(self.toplevel)

	def change(self,widget,on_window_mode_changed,winname):
		on_window_mode_changed(winname,self)


###-------------------------------METHODS------------------------------###
	def new_page(self, widget,old_page,toplevel):
		children=old_page.get_children()
		index=0
		while index<len(children):
			children[index].destroy()
			index=index+1	
		self.new_page=self.make_homepage()
		toplevel.pack_start(self.new_page,False,False,0)
		toplevel.show_all()
			
	def make_homepage(self):
		self.label1=Gtk.Label("This is one project")
		self.label2=Gtk.Label("This is another")
		self.label3=Gtk.Label("This is the last one")
		self.return_box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
		self.return_box.pack_start(self.label1,True,True,0)
		self.return_box.pack_start(self.label2,True,True,0)
		self.return_box.pack_start(self.label3,True,True,0)
		return self.return_box

	# look for all results of type 'type_results' using 'identifier'
	# for instance, look for all results of type group using identifier account. This would display all of account's groups
	def make_search_results(self,type_results,identifier):
		self.return_box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
		self.label4=Gtk.Label("This is the Search Result page")
		self.return_box.pack_start(self.label4,True,True,0)
		return self.return_box
		

'''
UI_INFO="blah"
on_window_mode_changed="moar blah"
win=explorer_window(UI_INFO,on_window_mode_changed)
win.connect("delete-event",Gtk.main_quit)
win.show_all()
Gtk.main()	
'''

