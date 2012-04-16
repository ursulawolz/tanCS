###------------------------------Inclusions--------------------------------###
from gi.repository import Gtk,GObject
from gi.repository import Gdk
from objectcode import Account,Comment
import datetime
#from mainproto2 import on_window_mode_changed
###-------------------------------Main Functions---------------------------###

#How the user creates line comments. Should involve clicking on the line or something like that. So this will get called by a button I think.Should add a line comment to the code.
def submit_line_comment(account,linenum,text):
	print(account+" says: '"+text+"' on line "+linenum)
	return

#How the user creates file comments. This involves just typing what the comment is in the gtkentry at the bottom. When they hit submit this function will be called and this will add a file comment to the code.
def submit_file_comment(account,text):
	print(account+" says: '"+text+"' about this file")
	return

def add_mode_menu_actions(action_group,on_window_mode_changed,parent_window):
	action_modemenu=Gtk.Action("ModeMenu","Mode",None,None)
	action_group.add_action(action_modemenu)
	
	action_group.add_radio_actions([
		("Viewer", None, "Viewer", None, None, 1),
		("Explorer", None, "Explorer", None, None, 2),
		("Editor", None, "Editor", None, None, 3)
	], 1, change_window,[on_window_mode_changed,parent_window])

def change_window(widget,new_window_name,parent_window,on_window_mode_changed):
	on_window_mode_changed(new_window_name,parent_window)

###------------------------------Viewer Class------------------------------###
class TempWindow(Gtk.Window):
	def __init__(self,on_window_mode_changed):
		Gtk.Window.__init__(self,title="Entry Demo")
		fake_user=Account("Random Hash","The instigator","Password","Avatar")
		color=Gdk.Color(1000,1000,1000)
		self.x=840
		self.y=280
		self.set_size_request(self.x,self.y)
		self.timeout_id=None

		self.on_window_mode_changed=on_window_mode_changed

		#make toolbar
		self.create_toolbar()

		#self.image=Gtk.Image()
		#self.image=Gtk.set_from_image("side.jpg")
		imagebox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=50)
		self.image2=Gtk.Image.new_from_file("side.jpg")
		self.image=Gtk.Image.new_from_file("sideb.jpg")
		
		imagebox.pack_start(self.image,False,False,0)
		imagebox.pack_start(self.image2,False,False,0)

		imageframe=Gtk.Frame()
		imageframe.add(imagebox)

		toplevel=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
		toplevel.set_size_request(self.x,self.y)
		self.add(toplevel)
		#toplevel.pack_start(menubar,False,False,0)
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
		self.thecode.set_editable(False)
		self.thecode.connect("key-press-event",self.on_key_press)
		codescroll=Gtk.ScrolledWindow()
		codescroll.add_with_viewport(self.thecodeframe)
		codescroll.set_size_request(self.x-150,400)	
		vbox.pack_start(self.toolbar,False,True,0)
		vbox.pack_start(codescroll,False,False,0)	

		hbox=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
		
		self.listbutton=Gtk.ToggleButton("List")
		self.linebutton=Gtk.ToggleButton("Line")
		
		self.listbutton.connect("toggled", change_window, "Editor", [on_window_mode_changed,self])
		self.linebutton.connect("toggled", change_window, "Explorer", [on_window_mode_changed,self])
		hbox.pack_end(self.listbutton,False, False,0)
		hbox.pack_end(self.linebutton,False, False,0)

		#vbox.pack_start(hbox, False, False,0)

		commentswindow = Gtk.ScrolledWindow()
		commentswindow.set_size_request(200,100)
		commentswindow.set_hexpand(True)
		commentswindow.set_vexpand(True)
		
		frame=Gtk.Frame()
		vbox2=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

		self.filecomments=self.get_file_comments("This file")
		index=0
		while index<len(self.filecomments):
			vbox2.pack_start(self.create_comment(self.filecomments[index]),False,False,0)
			index=index+1	
		

		
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
		#Gtk.UIManager()

###---------------------------------METHODS--------------------------------###

# Just to make it clear for later, there is a label, which is the text of the comment. It is placed within an event box for border reasons. 
# Then frames are created. The event boxes are added to the frames. The account name associated with the comment is then made as a label for bold reasons. 
# Markup allows gtk to read the bold tags. Then those account names are added as labels (little things at the top of frames in this case) to the frames. 
# The frames are then added to a vertical box

	def create_comment(self,comment):
		temp_label=Gtk.Label(comment.text,halign=Gtk.Align.START)
		temp_frame=Gtk.Frame()
		temp_event=Gtk.EventBox()
		temp_event.set_border_width(6)
		temp_event.add(temp_label)
		temp_frame.add(temp_event)
		temp_title=Gtk.Label("<b>"+"Account Name Goes Here"+"</b>")
		temp_title.set_use_markup(True)
		temp_frame.set_label_widget(temp_title)
		return temp_frame

#Should unpackage the code from how ever it is stored in the revision and make a text buffer out of it so that it can be displayed later in a text view.  	
	def get_code(self,revision):
		return textbuffer

#should unpack the comments from where they are in revision and make a list of all the file comments so that they can be displayed.
	def get_file_comments(self,revision):
		text1="I see how you have added many oranges. Is there any way to dynamically create widgets?"
		text2="Well, yes and no. It's a little hard, but you can definitely do it. Papayas?"
		text3="Thanks for the help. Also, I saw that there are some variables that just seem to come out of nowhere like 'clicked' and 'label'. Where do these come from?"
		text4="They are variables that Gtk has included in it. When you import they get recognized. \n\nHowever, it is important to recognize that the c++ library for Gtk+ and the python bindings for gtk are slightly different.\n\n For instance, most of the final variables associated with the style attributes of buttons (ex. Gtk.SHADOW_OUT) are different in the python version.\n\n This can lead to much frustruation, especially because documentation is sometimes inconsistant or out of date"
		fake1=Comment(text1,"10:20","Random Hash","This file")
		fake2=Comment(text2,"10:35","Random Hash","This file")
		fake3=Comment(text3,"10:47","Random Hash","This file")
		fake4=Comment(text4,"11:00","Random Hash","This file")
		filecommentlist=[fake1,fake2,fake3,fake4]
		return filecommentlist

#should unpack the line comments from where they are in revision and make a list of all of them so that they can be displayed.
	def get_line_comments(self,revision):
		return linecommentlist

# Not quite sure how to do this one. It needs to dynamically create a revision map for the whole project and allow you to move from one revision to another as well as load those revision. 
	def create_revision_map(self):
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

#Creates the top toolbar for the window.
	def create_toolbar(self):
		
		self.toolbar=Gtk.Toolbar()
		button_new=Gtk.ToolButton.new_from_stock(Gtk.STOCK_NEW)
		self.toolbar.insert(button_new, 0)
		#button_new.connect("clicked", self.create_new)

		button_copy=Gtk.ToolButton.new_from_stock(Gtk.STOCK_COPY)
		self.toolbar.insert(button_copy, 1)
		button_copy.connect("clicked", self.copy_text)

		editor_icon=Gtk.Image.new_from_file('editor-icon.png')
		button_editor=Gtk.ToolButton()
		button_editor.set_icon_widget(editor_icon)
		self.toolbar.insert(button_editor, 2)
		button_editor.connect("clicked",change_window,"Editor",self,self.on_window_mode_changed)

		explorer_icon=Gtk.Image.new_from_file('explorer-icon.png')
		button_explorer=Gtk.ToolButton()
		button_explorer.set_icon_widget(explorer_icon)
		self.toolbar.insert(button_explorer, 3)
		button_explorer.connect("clicked",change_window,"Explorer",self,self.on_window_mode_changed)

		self.toolbar.show_all()

	def on_key_press(self,widget,data):
		#runs when any key is pressed

		#c is 99

		val=data.keyval #get the pressed key
		if val==99:
			if Gdk.ModifierType.CONTROL_MASK&data.state==Gdk.ModifierType.CONTROL_MASK:
				self.copy_text()

	def copy_text(self):
		date=datetime.date.today()
		select=self.thecodebuffer.get_selection_bounds()
		if select==():
			select=self.sbuff.get_iter_at_mark(self.sbuff.get_insert())

		a=self.thecodebuffer.get_end_iter()
		#copy=Borrow(date,self.projID,self.projrev,self.filename)

	def get_lines_from_block(self,select):
		#takes in a tuple with the selection bounds
		#outputs a list containing the offset for the start of each line
		#if select is empty, returns a list containing -1
		if not select==():
			frontoffset=self.get_line_start(select[0])
			backoffset=self.get_line_start(select[1])
			front=self.sbuff.get_iter_at_offset(frontoffset)
			back=self.sbuff.get_iter_at_offset(backoffset)
			tempoffset=backoffset-1
			lines=[backoffset]
			while tempoffset>frontoffset:
				backa=self.sbuff.get_iter_at_offset(tempoffset-1)
				backb=self.sbuff.get_iter_at_offset(tempoffset)
				txt=self.sbuff.get_slice(backa,backb,True)
				if txt=='\n':
					lines.append(tempoffset)
				tempoffset-=1
			lines.append(frontoffset)
			lines.reverse()
			return lines
		else:
			return [-1]

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
