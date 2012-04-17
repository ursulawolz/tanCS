from gi.repository import Gtk,GObject
from gi.repository import Gdk

###------------------------Explorer Class--------------------------###
class explorer_window(Gtk.Window):
	def __init__(self,parent):
		Gtk.Window.__init__(self,title="Entry Demo")

		self.x=640
		self.y=280
		self.set_size_request(self.x,self.y)
		
		self.parent=parent

		#because of the way things are destroyed spacing on the next line needs to be 0
		self.toplevel=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

		self.quicknav=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

		self.home=Gtk.Label("Home")
		self.myaccount=Gtk.Label("My Account")
		self.mygroups=Gtk.Label("My Groups")
		self.search=Gtk.Label("Search")
		self.help=Gtk.Label("Help")

		self.tohome=Gtk.EventBox()
		self.tohome.add(self.home)

		self.tomyaccount=Gtk.EventBox()
		self.tomyaccount.add(self.myaccount)

		self.tomygroups=Gtk.EventBox()
		self.tomygroups.add(self.mygroups)

		self.tosearch=Gtk.EventBox()
		self.tosearch.add(self.search)

		self.tohelp=Gtk.EventBox()
		self.tohelp.add(self.help)

		if not(self.parent.user)==None:
			self.tohome.connect("button_press_event",self.on_home_clicked,self.toplevel)
			self.tomyaccount.connect("button_press_event",self.on_account_clicked,self.toplevel)
			self.tomygroups.connect("button_press_event",self.on_mygroups_clicked,self.toplevel)
			self.tosearch.connect("button_press_event",self.on_search_clicked,self.toplevel)
			self.tohelp.connect("button_press_event",self.on_help_clicked,self.toplevel)
		else:
			nav_options=[self.tohome,self.tomyaccount,self.tomygroups,self.tosearch,self.tohelp]
			index=0
			while index<len(nav_options):
				nav_options[index].connect("button_press_event",self.on_nologin_clicked,self.toplevel)
				index=index+1

		self.quicknav.pack_start(self.tohome,True,True,0)
		self.quicknav.pack_start(self.tomyaccount,True,True,0)
		self.quicknav.pack_start(self.tomygroups,True,True,0)
		self.quicknav.pack_start(self.tosearch,True,True,0)
		self.quicknav.pack_start(self.tohelp,True,True,0)
		self.quicknavframe=Gtk.Frame()
		self.quicknavframe.add(self.quicknav)
		self.toplevel.pack_start(self.quicknavframe,False,False,0)

		self.alert=Gtk.Label("This is a Helpful Message!")
		self.toplevel.pack_start(self.alert,False,False,0)

		self.current_page=self.make_login()

		#self.toggle.connect("clicked",self.new_page,self.current_page,self.toplevel)
		#self.toggle.connect("clicked",self.change,on_window_mode_changed,'Editor')

		self.toplevel.pack_start(self.current_page,False,False,0)
		self.add(self.toplevel)

	def change(self,widget,on_window_mode_changed,winname):
		on_window_mode_changed(winname,self)


###-------------------------------METHODS------------------------------###

# Ok so how do you make a new page appear? So this is how it works:
# First: You click on a button that redirects you to
# Second: A function of form 'on_blah_clicked' which calls
# Third: A function of from 'make_blah' which actually has the information and forms it into a Gtk.Box which then
# Fourth: Calls new_page which replaces the top level box with the box made by 'make_blah' 
# Brendan you say, this sounds moronic! Why use three functions instead of one? 
# Its because I wanted to be able to have a generic new page function which just cleared the current page. 
# Then, I realized that unless I had two functions, one for the specific buttons and the other for the general function itself, we would have the problem that we had with the change function, where we wanted a general fucntion so it could be called by something other than that button if we wnated it to. 

	def create_new_page(self,toplevel,the_new_page):
		children=self.current_page.get_children()
		index=0
		while index<len(children):
			children[index].destroy()
			index=index+1	
		self.current_page=the_new_page
		toplevel.pack_start(self.current_page,False,False,0)
		toplevel.show_all()
			
	def make_homepage(self):
		self.label1=Gtk.Label("This is the Homepage")
		self.return_box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
		self.return_box.pack_start(self.label1,True,True,0)
		return self.return_box

	def make_account(self,account):
		self.label2=Gtk.Label("This is the Account Page")
		self.return_box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
		self.return_box.pack_start(self.label2,True,True,0)
		return self.return_box

	def make_help(self):
		self.label3=Gtk.Label("This is the Help Page")
		self.return_box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
		self.return_box.pack_start(self.label3,True,True,0)
		return self.return_box

	def make_mygroups(self,account):
		self.label5=Gtk.Label("This is the MyGroups Page")
		self.return_box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
		self.return_box.pack_start(self.label5,True,True,0)
		return self.return_box

	def make_login(self):
		self.username_entry=Gtk.Entry()
		self.password_entry=Gtk.Entry()
		self.password_entry.set_visibility(False)
		self.username_note=Gtk.Label("Username: ")
		self.password_note=Gtk.Label("Password: ")
		self.register=Gtk.Button("Register")
		self.login=Gtk.Button("Login")

		self.username_block=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=40)
		self.password_block=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=40)
		self.button_block=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=40)
		
		self.username_block.pack_start(self.username_note,True,True,0)
		self.username_block.pack_start(self.username_entry,True,True,0)
		self.password_block.pack_start(self.password_note,True,True,0)
		self.password_block.pack_start(self.password_entry,True,True,0)
		self.button_block.pack_end(self.login,False,False,0)
		self.button_block.pack_end(self.register,False,False,0)
		
		self.total_block=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=10)
		self.total_block.pack_start(self.username_block,True,True,0)
		self.total_block.pack_start(self.password_block,True,True,0)
		self.total_block.pack_start(self.button_block,True,True,0)
		self.return_box=Gtk.Frame()
		self.return_box.add(self.total_block)
		return self.return_box

	# look for all results of type 'type_results' using 'identifier'
	# for instance, look for all results of type group using identifier account. This would display all of account's groups
	def make_search_results(self,type_results,identifier):
		self.return_box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
		self.label4=Gtk.Label("This is the Search Result page")
		self.return_box.pack_start(self.label4,True,True,0)
		return self.return_box
	
	def on_home_clicked(self,widget,something,toplevel):
		print("Home clicked")
		self.the_new_page=self.make_homepage()
		self.create_new_page(toplevel,self.the_new_page)
	def on_account_clicked(self,widget,something,toplevel):
		print("Account clicked")
		self.the_new_page=self.make_account("account")
		self.create_new_page(toplevel,self.the_new_page)
	def on_mygroups_clicked(self,widget,something,toplevel):
		print("My groups clicked")
		self.the_new_page=self.make_mygroups("account")
		self.create_new_page(toplevel,self.the_new_page)
	def on_search_clicked(self,widget,something,toplevel):
		print("Search clicked")
		self.the_new_page=self.make_search_results("type_results","Identifier")
		self.create_new_page(toplevel,self.the_new_page)
	def on_help_clicked(self,widget,something,toplevel):
		print("Help clicked")
		self.the_new_page=self.make_help()
		self.create_new_page(toplevel,self.the_new_page)
	def on_nologin_clicked(self,widget,something,toplevel):
		self.alert.set_text("You have not logged in yet!") 

