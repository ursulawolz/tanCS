from gi.repository import Gtk,GObject
from gi.repository import Gdk
from objectcode import *

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

		self.current_page=self.make_login(self.toplevel)

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

###------------------------Make-Functions------------------------###	
		
	def make_homepage(self):
		self.padding=Gtk.Label("\n")
		self.label1=Gtk.Label("<span font_desc='Helvetica 20'>%s</span>" %"<b>Welcome to TanCS</b>")
		self.label2=Gtk.Label("<span font_desc='Helvetica 12'>%s</span>" %"<b>Revision Contol, IDE, Community of Practice and Game all rolled into one</b>")
		self.label1.set_use_markup(True)
		self.label2.set_use_markup(True)
		self.label2.set_line_wrap(True)
		self.return_box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
		self.return_box.pack_start(self.padding,True,True,0)
		self.return_box.pack_start(self.label1,True,True,0)
		self.return_box.pack_start(self.label2,True,True,0)
		return self.return_box

	def make_help(self):
		self.label3=Gtk.Label("This is the Help Page")
		self.return_box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
		self.return_box.pack_start(self.label3,True,True,0)
		return self.return_box

	def make_display_project(self,project):
		self.return_box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=20)
		title=Gtk.Label('<b>'+project.title+'</b>')
		title.set_use_markup(True)
		description_title=Gtk.Label("Description: ")
		
		description=Gtk.Label(project.description)
		description_block=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=20)
		description_block.pack_start(description_title,False,False,0)
		description_block.pack_start(description,False,False,0)
		to_revision_map=Gtk.Button("View Revision Map")
		back_to_group=Gtk.Button("Return to Group Page")
		self.return_box.pack_start(title,False,False,0)
		self.return_box.pack_start(description_block,False,False,0)
		self.return_box.pack_start(to_revision_map,False,False,0)
		self.return_box.pack_start(back_to_group,False,False,0)
		return self.return_box
		
		

###-------------------------Group-Methods--------------------------###

	def make_mygroups(self,account):
		#self.label5=Gtk.Label("This is the MyGroups Page")
		self.return_box=self.make_search_results("groups",self.parent.user)
		#self.return_box.pack_start(self.label5,True,True,0)
		return self.return_box

	def make_display_group(self,group):
		self.return_box2=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=20)

		title=Gtk.Label('<b>'+group.title+'</b>')
		title.set_use_markup(True)
		description_title=Gtk.Label("Description: ")
		admin_title=Gtk.Label("Admin: ")
		account_title=Gtk.Label("Accounts: ")
		project_title=Gtk.Label("Projects: ")

		description=Gtk.Label(group.description)
		admin=Gtk.Label(self.get_results("accounts","FakeID").username)
		temp_group=Group('','','','','','')
		accounts=self.make_search_results("accounts",temp_group)
		projects=self.make_search_results("projects",temp_group)
		new_project_button=Gtk.Button("Create New Project")
		join_group_button=Gtk.Button("Join This Group")

		admin_block=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=20)
		description_block=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=20)
		admin_block.pack_start(admin_title,False,False,0)
		admin_block.pack_start(admin,False,False,0)
		description_block.pack_start(description_title,False,False,0)
		description_block.pack_start(description,False,False,0)

		self.return_box2.pack_start(title,False,False,0)
		self.return_box2.pack_start(description_block,False,False,0)
		self.return_box2.pack_start(admin_block,False,False,0)
		self.return_box2.pack_start(account_title,False,False,0)
		self.return_box2.pack_start(accounts,False,False,0)
		self.return_box2.pack_start(join_group_button,False,False,0)
		self.return_box2.pack_start(project_title,False,False,0)
		self.return_box2.pack_start(projects,False,False,0)
		self.return_box2.pack_start(new_project_button,False,False,0)		
		return self.return_box2

###---------------------------Account-Functions---------------------###
	def make_account(self,account):
		self.return_box2=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
		info_block=Gtk.Table(4,4,True)

		user_title=Gtk.Label("Username: ")
		pass_title=Gtk.Label("Password: ")
		avatar_title=Gtk.Label("Avatar: ")
		self.username_label=Gtk.Entry()
		self.username_label.set_text(account.username)
		self.password_label=Gtk.Entry()
		self.password_label.set_text(account.password)
		self.avatar_label=Gtk.Image()
		self.avatar_label.set_from_file(account.avatar)
		if account==self.parent.user:
			user_button=Gtk.Button("Change")
			pass_button=Gtk.Button("Change")
			avatar_button=Gtk.Button("Change")

		user_button.connect("clicked",self.on_change_pressed,"usr")
		pass_button.connect("clicked",self.on_change_pressed,"pass")
		avatar_button.connect("clicked",self.on_change_pressed,"avatar",self.avatar_label)

		info_block.attach(user_title,0,1,0,1)
		info_block.attach(pass_title,0,1,1,2)
		info_block.attach(avatar_title,0,1,2,3)
		info_block.attach(self.username_label,1,3,0,1)
		info_block.attach(self.password_label,1,3,1,2)
		info_block.attach(self.avatar_label,1,3,2,4)
		info_block.attach(user_button,3,4,0,1)
		info_block.attach(pass_button,3,4,1,2)
		info_block.attach(avatar_button,3,4,2,3)
		
		group_title=Gtk.Label("Groups: ")
		temp=self.make_search_results("groups",self.parent.user)
		project_title=Gtk.Label("Projects: ")
		#temp2=self.make_search_results("demo",'')
		temp2=self.make_search_results("projects",self.parent.user)
		
		self.return_box2.pack_start(info_block,False,False,0)
		self.return_box2.pack_start(group_title,True,True,0)
		self.return_box2.pack_start(temp,True,True,0)
		self.return_box2.pack_start(project_title,True,True,0)
		self.return_box2.pack_start(temp2,True,True,0)
		return self.return_box2

	def on_change_pressed(self,widget,which,realwidget=None):
		if which=="usr":
			#change_username(self.parent.user.userID,new_username)
			print "username changed from '"+self.parent.user.username+"' to '"+self.username_label.get_text()+"'" 
		elif which=="pass":
			#change_password(self.parent.user.userID,new_password)
			print "password changed from '"+self.parent.user.password+"' to '"+self.password_label.get_text()+"'"
		elif which=="avatar":
			dialog=Gtk.FileChooserDialog('Choose a file',self,Gtk.FileChooserAction.OPEN,(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,Gtk.STOCK_OK,Gtk.ResponseType.ACCEPT))
			filter_img = Gtk.FileFilter()
			filter_img.set_name("Image files")
			filter_img.add_mime_type("image/jpeg")
			filter_img.add_mime_type("image/bmp")
			filter_img.add_mime_type("image/png")
			filter_img.add_mime_type("image/gif")
			dialog.add_filter(filter_img)
			response=dialog.run()
			if response==Gtk.ResponseType.ACCEPT:
				filename=dialog.get_filename()
				f=open(filename)
				#change_avatar(self.parent.user.userID,new_avatar)
				print "avatar changed from '"+self.parent.user.avatar+"' to "+f.name+"'" 
				self.parent.user.avatar=f.name
				realwidget.set_from_file(self.parent.user.avatar)
			dialog.destroy()

###----------------------------Login-Functions----------------------###
	def make_login(self,toplevel):
		self.username_entry=Gtk.Entry()
		self.password_entry=Gtk.Entry()
		self.password_entry.set_visibility(False)
		self.username_note=Gtk.Label("Username: ")
		self.password_note=Gtk.Label("Password: ")
		self.register=Gtk.Button("Register")
		self.login=Gtk.Button("Login")

		self.login.connect("clicked",self.submit_login,self.username_entry,self.password_entry,toplevel)

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

	def submit_login(self,widget,username,password,toplevel):
		#check to see if the account is valid
		#Account=get_account(username.get_text(),password.get_text())
		account=Account("account ID","Fake Account","1234","fork-icon.png")
		if not account==None:
			self.parent.user=account
			self.alert.set_text("You have logged in!")

			nav_options=[self.tohome,self.tomyaccount,self.tomygroups,self.tosearch,self.tohelp]
			index=0
			while index<len(nav_options):
				nav_options[index].handler_block_by_func(self.on_nologin_clicked)
				index=index+1

			self.tohome.connect("button_press_event",self.on_home_clicked,self.toplevel)
			self.tomyaccount.connect("button_press_event",self.on_account_clicked,self.toplevel)
			self.tomygroups.connect("button_press_event",self.on_mygroups_clicked,self.toplevel)
			self.tosearch.connect("button_press_event",self.on_search_clicked,self.toplevel)
			self.tohelp.connect("button_press_event",self.on_help_clicked,self.toplevel)
			#print self.parent.user
			self.on_home_clicked("widget","something",toplevel)
		else:
			self.alert.set_text("Your login information is invalid")


###-------------------------Search-Functions-----------------------###
		
	# look for all results of type 'type_results' using 'identifier'
	# for instance, look for all results of type group using identifier account. This would display all of account's groups
	def make_search_results(self,type_results,identifier):
		#ask for results from network
		resultslist=self.get_results(type_results,identifier)
		#print "working in make results"
		self.return_box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
		#self.label4=Gtk.Label("This is the Search Result page")
		#self.return_box.pack_start(self.label4,True,True,0)
		search_grid=Gtk.Grid()
		total=len(resultslist)
		number=1
		ypos=1
		while ypos<5 and number<=total:
			xpos=1
			while xpos<9 and number<=total:
				display_list=self.what_display(resultslist[number-1])
				search_box=self.make_search_box(number,display_list[0],display_list[1],display_list[2],resultslist[number-1])
				search_grid.attach(search_box,xpos,ypos,1,1)
				xpos=xpos+1
				number=number+1
				#print "number: "+str(number)
				#print "xpos: "+str(xpos)
				#print "ypos: "+str(ypos)
			ypos=ypos+1
		self.return_box.pack_start(search_grid,True,True,0)
		return self.return_box

	def make_search_box(self,number,title,comment,other_info,result):
		#Get rid of this stuff later
		#title="Title goes here"
		#comment="Comment goes here. This should be very long and take up ALL of the space"
		#other_info="Other info goes here"
		temp_group=Group('','','','')
		temp_project=Project('','','','',4,'')
		temp_account=Account('','','','')

		outer_padding=Gtk.EventBox()
		outer_frame=Gtk.Frame()
		outer_vbox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
		heading=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
		number=Gtk.Label(number)
		title=Gtk.Label(title)
		#comment_padding=Gtk.EventBox()
		#comment_frame=Gtk.Frame()
		comment=Gtk.Label(comment)
		comment.set_line_wrap(True)
		other_info=Gtk.Label(other_info)

		if type(result)==type(temp_group):
			outer_padding.connect("button_press_event",self.on_group_display_clicked,self.toplevel,result)

		if type(result)==type(temp_project):
			outer_padding.connect("button_press_event",self.on_project_display_clicked,self.toplevel,result)
		
		if type(result)==type(temp_account):
			outer_padding.connect("button_press_event",self.on_account_clicked,self.toplevel,result)		

		outer_padding.add(outer_frame)
		outer_frame.add(outer_vbox)
		outer_vbox.pack_start(heading,True,True,0)
		outer_vbox.pack_start(comment,True,True,0)
		#outer_vbox.pack_start(comment_padding,True,True,0)
		outer_vbox.pack_start(other_info,True,True,0)
		heading.pack_start(number,False,False,0)
		heading.pack_start(title,False,False,0)
		#comment_padding.add(comment_frame)
		#comment_frame.add(comment)	

		outer_padding.set_border_width(6)
		#comment_padding.set_border_width(3)
		return outer_padding

	def search_input(self,toplevel):
		search_for=Gtk.Entry()
		search_using=Gtk.Entry()
		for_note=Gtk.Label("Search For:    ")
		using_note=Gtk.Label("Search Using: ")
		search_submit=Gtk.Button("Submit")

		search_submit.connect("clicked",self.submit_search,search_for,search_using,toplevel)

		for_block=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=40)
		using_block=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=40)
		
		for_block.pack_start(for_note,True,True,0)
		for_block.pack_start(search_for,True,True,0)
		using_block.pack_start(using_note,True,True,0)
		using_block.pack_start(search_using,True,True,0)
		formattingbox=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=0)

		formattingbox.pack_end(search_submit,False,False,0)
		
		total_block=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=10)
		total_block.pack_start(for_block,True,True,0)
		total_block.pack_start(using_block,False,False,0)
		total_block.pack_start(formattingbox,False,False,0)
		self.return_box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=10)
		self.return_box.pack_start(total_block,False,False,0)
		return self.return_box

	def submit_search(self,widget,search_for,search_using,toplevel):
		search_for=search_for.get_text()
		search_using=search_using.get_text()
		print "search for is: ",search_for," search using is: ",search_using 
		self.the_new_page=self.make_search_results(search_for,search_using)
		self.create_new_page(toplevel,self.the_new_page)

	def what_display(self,result):
		temp_group=Group('','','','')
		temp_project=Project('','','','',4,'')
		temp_account=Account('','','','')
		#print result
		if type(result)==type(temp_account):
			title=result.username
			comment=result.avatar
			other_info="Nothing"
			return [title,comment,other_info]
		elif type(result)==type(temp_group):
			title=result.title
			comment=result.description
			#other_info="Accounts are"+result.get_accounts()
			dictionary=result.accountIDs
			thelist=[]
			for key in dictionary:
				thelist.append(dictionary[key]) 
			other_info="Accounts are: "+str(thelist)
			return [title,comment,other_info]
		elif type(result)==type(temp_project):
			print "project"	
			title=result.title
			comment=result.description
			other_info="Current Revision is: ",str(result.revisions[0])
			return [title,comment,other_info]
		elif type(result)==type(('','')):
			#print "result is: ",result
			title=result[0]
			comment=result[1]
			other_info=result[2]
			return [title,comment,other_info]
		else:
			print "Error in identifying types in display"	

###--------------------------Quicknav-Functions----------------------###
	
	def on_home_clicked(self,widget,something,toplevel):
		print("Home clicked")
		self.the_new_page=self.make_homepage()
		self.create_new_page(toplevel,self.the_new_page)
		self.alert.set_text("Homepage")

	def on_account_clicked(self,widget,something,toplevel):
		print("Account clicked")
		self.the_new_page=self.make_account(self.parent.user)
		self.create_new_page(toplevel,self.the_new_page)
		self.alert.set_text("Account Page")

	def on_mygroups_clicked(self,widget,something,toplevel):
		self.the_new_page=self.make_mygroups("account")
		self.create_new_page(toplevel,self.the_new_page)
		self.alert.set_text("My Groups")

	def on_search_clicked(self,widget,something,toplevel):
		print("Search clicked")
		#self.the_new_page=self.make_search_results("type_results","Identifier")
		self.the_new_page=self.search_input(toplevel)
		self.create_new_page(toplevel,self.the_new_page)
		self.alert.set_text("Search Parameters")

	def on_help_clicked(self,widget,something,toplevel):
		print("Help clicked")
		#self.the_new_page=self.make_help()
		temp=Group("GroupID","GodID","This is the title","This is the description",'a','a')
		self.the_new_page=self.make_display_group(temp)
		self.create_new_page(toplevel,self.the_new_page)
		self.alert.set_text("Help Page")

	def on_nologin_clicked(self,widget,something,toplevel):
		#print not(self.parent.user==None)
		self.alert.set_text("You have not logged in yet!") 

	def on_group_display_clicked(self,widget,something,toplevel,group):
		self.the_new_page=self.make_display_group(group)
		self.create_new_page(toplevel,self.the_new_page)
		self.alert.set_text("Group Display Page")
	def on_project_display_clicked(self,widget,something,toplevel,project):
		self.the_new_page=self.make_display_project(project)
		self.create_new_page(toplevel,self.the_new_page)
		self.alert.set_text("Project Display Page")

	###-------------------------Other-Functions-----------------------###
	def get_results(self,type_results,identifier):
		temp_account=Account("Fake ID","Fake Username",'','')
		temp_group=Group('','','','','')
		if type_results=="groups" and type(identifier)==type(temp_account):			
			result1=Group("gId",["aID","aID2"],"godId","Title1")
			result1.description="This is a Description"
			result2=Group("gId","aID","godId","Title2")
			result2.description="This is a Description"
			result3=Group("gId","aID","godId","Title3")
			result3.description="This is a Description"
			results=[result1,result2,result3]
			print "working in get results"
			return results
		elif type_results=="projects" and type(identifier)==type(temp_account):
			result1=Project("This is a title","This is a description",'','',4,'')
			result2=Project("This is a title","This is a description",'','',4,'')
			result3=Project("This is a title","This is a description",'','',4,'')
			result4=Project("This is a title","This is a description",'','',4,'')
			results=[result1,result2,result3,result4]
			return results
			
		elif type_results=="projects" and type(identifier)==type(temp_group):
			result1=Project("This is a title","This is a description",'','',4,'')
			result2=Project("This is a title","This is a description",'','',4,'')
			result3=Project("This is a title","This is a description",'','',4,'')
			results=[result1,result2,result3]
			return results
		elif type_results=="accounts" and type(identifier)==type(temp_group):
			return [temp_account,temp_account,temp_account]
		elif type_results=="accounts" and type(identifier)==type(""):
			result=temp_account
			return result
		elif type_results=="demo" and type(identifier)==type("string"):
			result1=("Title1","This is where description information will go","This is other information")
			result2=("Title2","This is where description information will go","This is other information")
			results=[result1,result2]
			return results
		else:
			print "Error in identifying types",type(identifier),"with",type(''),"in get results"
			print "type_results is: ",type_results		



