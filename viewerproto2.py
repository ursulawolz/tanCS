###------------------------------Inclusions--------------------------------###
from gi.repository import Gtk,GObject
from gi.repository import Gdk
#from mainproto2 import on_menu_mode_changed
###-------------------------------Main Functions---------------------------###

#How the user creates line comments. Should involve clicking on the line or something like that. So this will get called by a button I think.Should add a line comment to the code.
def submit_line_comment(account,linenum,text):
	print(account+" says: '"+text+"' on line "+linenum)
	return

#How the user creates file comments. This involves just typing what the comment is in the gtkentry at the bottom. When they hit submit this function will be called and this will add a file comment to the code.
def submit_file_comment(account,text):
	print(account+" says: '"+text+"' about this file")
	return

def add_mode_menu_actions(action_group,on_menu_mode_changed,parent_window):
	action_modemenu=Gtk.Action("ModeMenu","Mode",None,None)
	action_group.add_action(action_modemenu)
	
	action_group.add_radio_actions([
		("Viewer", None, "Viewer", None, None, 1),
		("Explorer", None, "Explorer", None, None, 2),
		("Editor", None, "Editor", None, None, 3)
	], 1, on_menu_mode_changed,parent_window)

def create_ui_manager(UI_INFO):
	uimanager = Gtk.UIManager()

	# Throws exception if something went wrong
	uimanager.add_ui_from_string(UI_INFO)
	return uimanager

#def on_menu_mode_changed(widget, current):
	#print current.get_name() + " was selected."

###------------------------------Viewer Class------------------------------###
class TempWindow(Gtk.Window):
	def __init__(self,UI_INFO,on_menu_mode_changed):
		Gtk.Window.__init__(self,title="Entry Demo")

		action_group = Gtk.ActionGroup("my_actions")
		add_mode_menu_actions(action_group,on_menu_mode_changed,self)
		uimanager = create_ui_manager(UI_INFO)
		uimanager.insert_action_group(action_group)
		menubar = uimanager.get_widget("/MenuBar")

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
		toplevel.pack_start(menubar,False,False,0)
		toplevel.pack_start(imageframe,True,True,0)
		
		vbox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
		#self.add(vbox)
	
		f=open("testingtk3.py")
		

		self.thecode=Gtk.TextView()
		self.thecodebuffer=self.thecode.get_buffer()
		self.thecodebuffer.set_text(f.read())
		self.thecode.set_size_request(self.x-150,560)
		self.thecodeframe=Gtk.Frame()
		self.thecodeframe.add(self.thecode)
		codescroll=Gtk.ScrolledWindow()
		codescroll.add_with_viewport(self.thecodeframe)
		codescroll.set_size_request(self.x-150,400)	
		vbox.pack_start(codescroll,False,False,0)	

		hbox=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
		
		self.listbutton=Gtk.ToggleButton("List")
		self.linebutton=Gtk.ToggleButton("Line")
		
		self.listbutton.connect("toggled", self.on_List_toggled, "List", self.linebutton)
		self.linebutton.connect("toggled", self.on_Line_toggled, "Line", self.listbutton)
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
		self.label4=Gtk.Label("Thank you for the help. Also I saw that there are some variables that just seem to come out of nowhere like 'clicked' and 'label'. Where do these come from?",halign=Gtk.Align.START)
		self.label5=Gtk.Label("They are variables that Gtk has included in it. When you import they get recognized. \n\nHowever it is important to recognize that the c++ library for Gtk+ and the python bindings for gtk are slightly different.\n\n For instance, most of the final variables associated with the style attributes of buttons (ex. Gtk.SHADOW_OUT) are different in the python version.\n\n This can lead to much frustruation, especially because documentation is sometimes inconsistant or out of date",halign=Gtk.Align.START)

# I am so very sorry for doing this. The comments need to be made dynamically according to this way of making comments.
		frame=Gtk.Frame()
		frame2=Gtk.Frame()
		frame3=Gtk.Frame()
		frame4=Gtk.Frame()
		frame5=Gtk.Frame()

# This is a cheat so I can have padding around the comment text within the frame so it looks nice. 
# Since label is not a container I can't just add border to it so I have to put it in an event box first

		cheat2=Gtk.EventBox()
		cheat3=Gtk.EventBox()
		cheat4=Gtk.EventBox()
		cheat5=Gtk.EventBox()

		cheat2.set_border_width(6)
		cheat3.set_border_width(6)
		cheat4.set_border_width(6)
		cheat5.set_border_width(6)

		cheat2.add(self.label2)
		cheat3.add(self.label3)
		cheat4.add(self.label4)
		cheat5.add(self.label5)

		frame2.add(cheat2)
		frame3.add(cheat3)
		frame4.add(cheat4)
		frame5.add(cheat5)

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

# Just to make it clear for later, there is a label, which is the text of the comment. It is placed within an event box for border reasons. 
# Then frames are created. The event boxes are added to the frames. The account name associated with the comment is then made as a label for bold reasons. 
# Markup allows gtk to read the bold tags. Then those account names are added as labels (little things at the top of frames in this case) to the frames. 
# The frames are then added to a vertical box

		#vbox2.pack_start(hbox,False,False,0)
		
		commentswindow.add_with_viewport(vbox2)
		commentswindow.set_size_request(self.x-150,240)
		commentbox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		commentbox.pack_start(hbox,False,False,0)
		commentbox.pack_start(commentswindow,False,False,0)
		frame.add(commentbox)

		hbox2=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
		entryframe=Gtk.Frame()
		self.entry=Gtk.TextView()
		# Don't change the name of this text view, it is connected to the pop up window for sumbit line number.
		entryframe.add(self.entry)
		self.comment_buffer=self.entry.get_buffer()
		self.comment_buffer.set_text("Thanks a bunch!")

		commentscroll=Gtk.ScrolledWindow()
		commentscroll.add_with_viewport(entryframe)
		commentscroll.set_size_request(self.x-150,100)

		self.submitcomment=Gtk.Button("Submit")
		self.submitcomment.connect("clicked", self.toggle_file_comment,self.entry)

		self.submitlinecomment=Gtk.Button("Submit Line Comment")
		self.submitlinecomment.connect("clicked", self.toggle_line_comment)
		
		vbox3=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		vbox3.pack_start(self.submitlinecomment,True,True,0)
		vbox3.pack_start(self.submitcomment,True,True,0)

		hbox2.pack_start(commentscroll,True,True,0)
		hbox2.pack_start(vbox3,False,False,0)
		
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
	def on_List_toggled(self,button,which,other):
		if button.get_active()==True:
			other.set_active(False)
			print(which)

#What happens when you click on the file comments only button
	def on_Line_toggled(self,button,which,other):
		if button.get_active()==True:
			other.set_active(False)
			print(which)

#What happens when you hit the submit line comment button
	def toggle_line_comment(self,widget):
		dialog=LineCommentDialog(self)
		endresult=dialog.run()

#What happens when you hit the submit file comment button.
	def toggle_file_comment(self,widget,entry):
		#account=get_account()
		account="The Instigater"
		tempbuffer=entry.get_buffer()
		startiter = tempbuffer.get_start_iter()
		enditer = tempbuffer.get_end_iter()
		thetext=tempbuffer.get_text(startiter,enditer,False)
		submit_file_comment(account,thetext)
		return
###-----------------------------ADDITIONAL WINDOWS-------------------------###
class LineCommentDialog(Gtk.Dialog):
	def __init__(self, parent):
		Gtk.Dialog.__init__(self,"Submit Line Comment",parent,0)
		label=Gtk.Label("Testing")
		adjustment = Gtk.Adjustment(0, 0, 100, 1, 10, 0)
		#Note that the limits on the spinner can change, don't exceed line numbs
		self.spinbutton = Gtk.SpinButton()
		self.spinbutton.set_adjustment(adjustment)
		self.spinsubmit=Gtk.Button("Submit")
		"""dframe=Gtk.Frame()
		dframe.set_size_request(100,50)
		self.dentry=Gtk.TextView()
		dframe.add(self.dentry)
		self.dtext_buffer=self.dentry.get_buffer()"""
		self.dlabel=Gtk.Label("Line Number")
		self.spinsubmit.connect("clicked", self.dialog_toggle_line_comment,self.spinbutton,parent.entry)
		#Note that this uses parent!!!!!!!!!! do not change the name of entry!

		dvbox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		#this does nothing, remove later?
		dhbox=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
		dhbox.pack_start(self.dlabel,False,False,0)
		dhbox.pack_start(self.spinbutton,False,False,0)
		dhbox.pack_end(self.spinsubmit,False,False,0)
		
		dvbox.pack_start(dhbox,False,False,0)
		# same as above
		box=self.get_content_area()
		box.add(dvbox)
		self.show_all()

	def dialog_toggle_line_comment(self,button,spinner,entry):
		#account=get_account()
		account="The Instigater"
		tempbuffer=entry.get_buffer()
		startiter = tempbuffer.get_start_iter()
		enditer = tempbuffer.get_end_iter()
		thetext=tempbuffer.get_text(startiter,enditer,False)
		submit_line_comment(account,str(spinner.get_value()),thetext)
		self.destroy()
