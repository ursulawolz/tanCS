###------------------------------Inclusions--------------------------------###
from gi.repository import GtkClutter
from gi.repository import Gtk,GObject,GtkSource,Clutter
from gi.repository import Gdk
from objectcode import Account,Comment,Borrow
import datetime, sys
import pdb
#from mainproto2 import on_window_mode_changed
###-------------------------------Main Functions---------------------------###

#How the user creates line comments. Should involve clicking on the line or something like that. So this will get called by a button I think.Should add a line comment to the code.
def submit_line_comment(self,account,linenum,text):
	time=datetime.date.today()
	new_comment=Comment(text,time,"Hash","Which_file",self.fake_user,linenum)
	print(account+" says: '"+text+"' on line "+linenum)
	return

def add_mode_menu_actions(action_group,on_window_mode_changed,parent_window):
	action_modemenu=Gtk.Action("ModeMenu","Mode",None,None)
	action_group.add_action(action_modemenu)
	
	action_group.add_radio_actions([
		("Viewer", None, "Viewer", None, None, 1),
		("Explorer", None, "Explorer", None, None, 2),
		("Editor", None, "Editor", None, None, 3)
	], 1, change_window,[on_window_mode_changed,parent_window])

def change_window(widget,new_window_name,parent_window,top_parent):
	top_parent.on_window_mode_changed(new_window_name,parent_window)

###------------------------------Viewer Class------------------------------###
class TempWindow(Gtk.Window):
	def __init__(self,parent):
		Gtk.Window.__init__(self,title="Entry Demo")
		
		#Clutter.init(sys.argv)

		self.fake_user=Account("Random Hash","The instigator","Password","Avatar")
		
		color=Gdk.Color(1000,1000,1000)
		self.set_resizable(False)
		self.x=840
		self.y=280
		self.set_size_request(self.x,self.y)
		self.timeout_id=None

		self.parent=parent
		self.on_window_mode_changed=parent.on_window_mode_changed

		#make toolbar
		self.create_toolbar()

		#self.image=Gtk.Image()
		#self.image=Gtk.set_from_image("side.jpg")
		imagebox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
		self.image2=Gtk.Image.new_from_file("side.jpg")
		self.image=Gtk.Image.new_from_file("sideb.jpg")
		
		#imagebox.pack_start(self.image,False,False,0)
		#imagebox.pack_start(self.image2,False,False,0)

		
		self.embed = GtkClutter.Embed()
		self.embed.grab_focus()
		self.embed.connect("enter-notify-event",self.enter_clutter)
		'''
		clutterscroll=Gtk.ScrolledWindow()
		clutterscroll.add_with_viewport(self.embed)
		clutterscroll.set_size_request(200,800)'''
		#self.embed.connect("button-press-event",self.stageclicked)
		imagebox.pack_start(self.embed,True,True,0)

		self.render_clutter()

		imageframe=Gtk.Frame()
		imageframe.add(imagebox)
		self.embed.set_size_request(200,800)

		self.toplevel=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
		self.toplevel.set_size_request(self.x,self.y)
		self.add(self.toplevel)
		#self.toplevel.pack_start(menubar,False,False,0)
		self.toplevel.pack_start(imageframe,True,True,0)


		vbox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
		#self.add(vbox)

		self.thecode=GtkSource.View()
		self.thecodebuffer = GtkSource.Buffer()
		self.thecode.set_buffer(self.thecodebuffer)
		self.thecodebuffer.set_text(self.parent.defaultfile.content)
		self.thecode.set_show_line_numbers(True)
		self.thecode.set_size_request(self.x-150,560)
		self.thecodeframe=Gtk.Frame()
		self.thecodeframe.add(self.thecode)
		self.thecode.set_editable(False)
		self.thecode.connect("key-press-event",self.on_key_press)
		lang = GtkSource.LanguageManager.get_default().get_language('python')
		self.thecodebuffer.set_language(lang)
		codescroll=Gtk.ScrolledWindow()
		codescroll.add_with_viewport(self.thecodeframe)
		codescroll.set_size_request(self.x-150,390)	
		vbox.pack_start(self.toolbar,False,True,0)
		vbox.pack_start(codescroll,False,False,0)	

		hbox=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
		vbox2=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		self.listbutton=Gtk.ToggleButton("List")
		self.linebutton=Gtk.ToggleButton("Line")
		
		self.listbutton.connect("toggled", self.on_List_toggled,self.listbutton,self.linebutton,vbox2)
		self.linebutton.connect("toggled", self.on_Line_toggled,self.linebutton,self.listbutton,vbox2)
		hbox.pack_end(self.listbutton,False, False,0)
		hbox.pack_end(self.linebutton,False, False,0)

		#vbox.pack_start(hbox, False, False,0)

		commentswindow = Gtk.ScrolledWindow()
		commentswindow.set_size_request(200,95)
		commentswindow.set_hexpand(True)
		commentswindow.set_vexpand(True)
		
		frame=Gtk.Frame()


		self.filecomments=self.get_file_comments("This file")
		index=0
		while index<len(self.filecomments):
			vbox2.pack_start(self.create_comment(self.filecomments[index]),False,False,0)
			index=index+1	
		
		self.padding=Gtk.EventBox()
		self.padding.set_border_width(15)
		self.padding.add(vbox2)
		
		commentswindow.add_with_viewport(self.padding)
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
		commentscroll.set_size_request(self.x-150,60)

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
		#vbox.pack_start(embed,True,True,0)

		self.toplevel.pack_start(vbox,False,False,0)
		#Gtk.UIManager()

###---------------------------------METHODS--------------------------------###

	#How the user creates file comments. This involves just typing what the comment is in the gtkentry at the bottom. When they hit submit this function will be called and this will add a file comment to the code.
	def submit_file_comment(self,account,text):
		time=datetime.date.today()
		new_comment=Comment(text,time,"Hash","Which_file",self.fake_user)
		print(account+" says: '"+text+"' about this file")
		return

	def render_clutter(self):
		self.stage = self.embed.get_stage()	# Get the Stage
		self.stage.set_no_clear_hint(False)
		self.stage.ensure_redraw()
		self.stage.set_title("The application title")		# Stage's title
		self.stage.connect("motion-event",self.mouse_moved)
		white = Clutter.Color.new(255,255,255,255)
		black=Clutter.Color.new(0,0,0,255)
		blue = Clutter.Color.new(0,0,255,255) # red,green,blue,alpha
		self.stage.set_color(white)
		self.stage.set_reactive(True)

		self.scroll=0

		'''
		intext = Clutter.Text.new_full("Sans 20", "Hello! This\nis where the\ndynamic\nrevision map\nwill go.\nPlease do\nnot panic\nwhile we\nrenovate.", blue)
		intext.set_reactive(True)
		Clutter.Container.add_actor(self.stage, intext)
		intext.set_position(5,5)

		self.rect=Clutter.Rectangle()
		self.rect.set_color(blue)
		self.rect.set_reactive(True)
		Clutter.Container.add_actor(self.stage, self.rect)
		self.rect.set_position(40,1200)
		self.rect.set_size(50,50)'''
		
		self.toptext = Clutter.Text.new_full("Sans 20", "Revision Map", blue)
		self.toptext.set_reactive(True)
		Clutter.Container.add_actor(self.stage, self.toptext)
		self.toptext.set_position(15,5)

		num_revs=len(self.parent.defaultproject.revisions)

		#nested lists containing the various clutter objects within a revision circle
		#[circle,label,files,isopen,ishead]
		self.circles=[] 

		for i in range(num_revs):
			newcircle=Clutter.Texture.new_from_file("circle.png");
			Clutter.Container.add_actor(self.stage, newcircle)
			newcircle.set_position(50,125*i+50)
			newcircle.set_size(100,100)
			newcircle.set_reactive(True)
			newcircle.connect('button-press-event',self.revclick,i)

			newlabel=Clutter.Text.new_full("Serif 20","Rev "+str(i+1),black)
			Clutter.Container.add_actor(self.stage,newlabel)
			newlabel.set_anchor_point(newlabel.get_size()[0]/2.0,newlabel.get_size()[1]/2.0)
			newlabel.set_position(100,125*i+100)

			self.circles.append([newcircle,newlabel,[],False,False])

		headcircle=Clutter.Texture.new_from_file("headcircle.png");
		Clutter.Container.add_actor(self.stage, headcircle)
		headcircle.set_position(50,125*num_revs+50)
		headcircle.set_size(100,100)
		headcircle.set_reactive(True)
		headcircle.connect('button-press-event',self.revclick,num_revs)

		headlabel=Clutter.Text.new_full("Serif 20","Head",black)
		Clutter.Container.add_actor(self.stage,headlabel)
		headlabel.set_anchor_point(headlabel.get_size()[0]/2.0,headlabel.get_size()[1]/2.0)
		headlabel.set_position(100,125*num_revs+100)

		self.circles.append([headcircle,headlabel,[],False,True])

		'''
		circle=Clutter.Texture.new_from_file("circle.png");
		Clutter.Container.add_actor(self.stage, circle)
		circle.set_position(50,450)
		circle.set_size(100,100)
		circle.set_reactive(True)
		#circle.connect('button-press-event',lambda x,y:self.success())

		label1=Clutter.Text.new_full("Serif 20","Rev 1",black)
		Clutter.Container.add_actor(self.stage,label1)
		label1.set_anchor_point(label1.get_size()[0]/2.0,label1.get_size()[1]/2.0)
		label1.set_position(100,500)

		circle2=Clutter.Texture.new_from_file("circle.png");
		Clutter.Container.add_actor(self.stage, circle2)
		circle2.set_position(50,570)
		circle2.set_size(100,100)
		circle2.set_reactive(True)

		label2=Clutter.Text.new_full("Serif 20","Rev 2",black)
		Clutter.Container.add_actor(self.stage,label2)
		label2.set_anchor_point(label2.get_size()[0]/2.0,label2.get_size()[1]/2.0)
		label2.set_position(100,620)'''

		'''
		#self.stage.connect('button-press-event',self.stageclicked)
		self.rectrot=0
		GObject.timeout_add(10,self.clutterupdate)'''

		self.stage.show_all()	# We show everything

	def reset_clutter(self):
		for i in range(len(self.circles)):
			self.circles[i]
			self.circles[i][0].set_position(50,125*i+50+self.scroll)
			self.circles[i][1].set_position(100,125*i+100+self.scroll)
			self.circles[i][3] = False
			for j in range(len(self.circles[i][2])):
				self.circles[i][2][j].hide_all()
				Clutter.Container.remove_actor(self.stage, self.circles[i][2][j])
			self.circles[i][2] = []
		self.toptext.set_position(15,5+self.scroll)

	def revclick(self,widget,data,revnum):
		black=Clutter.Color.new(0,0,0,255)
		#self.stage.hide_all()
		#self.circles[1][0].hide()
		flag=(not self.circles[revnum][3])
		self.reset_clutter()
		if flag:
			filelabels=[]
			starty=self.circles[revnum][0].get_position()[1]+100
			numfiles=0
			if self.circles[revnum][4]:
				files=self.parent.defaultproject.head.files
			else:
				files=self.parent.defaultproject.revisions[revnum].files
			for f in files:
				numfiles+=1
				newlabel=Clutter.Text.new_full("Serif 12",f.file_name,black)
				Clutter.Container.add_actor(self.stage,newlabel)
				newlabel.set_anchor_point(newlabel.get_size()[0]/2.0,newlabel.get_size()[1]/2.0)
				newlabel.set_position(100,starty+25*numfiles)
				newlabel.connect('button-press-event',self.openfile,f)
				filelabels.append(newlabel)
			self.circles[revnum][2]=filelabels
			for i in range(len(self.circles)-(revnum+1)):
				i+=revnum+1
				self.circles[i][0].move_by(0,25+25*numfiles)
				self.circles[i][1].move_by(0,25+25*numfiles)
			self.circles[revnum][3]=True

	def enter_clutter(self,widget,data=-1):
		self.embed.grab_focus()

	def mouse_moved(self,widget,event):
		miny=100
		maxy=self.embed.get_allocation().height-100
		self.curr_y=event.get_coords()[1]
		#print maxy
		if self.curr_y<miny:
			GObject.timeout_add(200,self.scrollup)
		if self.curr_y>maxy:
			GObject.timeout_add(200,self.scrolldown)

	def scrollup(self,data=None):
		if self.scroll<0:
			self.scroll+=2
			self.reset_clutter()
			miny=150
			maxy=self.embed.get_allocation().height-150
			if self.curr_y<miny:
				return True
			else:
				return False
		else:
			return False

	def scrolldown(self,data=None):
		self.scroll-=2
		self.reset_clutter()
		miny=100
		maxy=self.embed.get_allocation().height-100
		if self.curr_y>maxy:
			return True
		else:
			return False

	def openfile(self,widget=None,data=None,f=None):
		print 'Opening '+f.file_name


	def stageclicked(self,widget,event=-1,data=-1):
		#print "Stage clicked at (%f, %f)" % (event.get_coords()[0],event.get_coords()[1])
		'''
		circle=Clutter.Texture.new_from_file("explorer-icon.png");
		Clutter.Container.add_actor(self.stage, circle)
		circle.set_position(event.get_coords()[0],event.get_coords()[1])'''
		return True # Stop further handling of this event

	def clutterupdate(self,data=-1):
		self.rect.set_rotation(Clutter.RotateAxis.X_AXIS, self.rectrot, 0, 25, 0)
		self.rectrot+=5 
		return True

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
		fake1=Comment(text1,"10:20","Random Hash","This file","Some account")
		fake2=Comment(text2,"10:35","Random Hash","This file","Some account")
		fake3=Comment(text3,"10:47","Random Hash","This file","Some account")
		fake4=Comment(text4,"11:00","Random Hash","This file","Some account")
		filecommentlist=[fake1,fake2,fake3,fake4]
		return filecommentlist

#should unpack the line comments from where they are in revision and make a list of all of them so that they can be displayed.
	def get_line_comments(self,revision):
		text1="I see how you have added many oranges. Is there any way to dynamically create widgets?"
		text2="Well, yes and no. It's a little hard, but you can definitely do it. Papayas?"
		text3="Thanks for the help. Also, I saw that there are some variables that just seem to come out of nowhere like 'clicked' and 'label'. Where do these come from?"
		text4="They are variables that Gtk has included in it. When you import they get recognized. \n\nHowever, it is important to recognize that the c++ library for Gtk+ and the python bindings for gtk are slightly different.\n\n For instance, most of the final variables associated with the style attributes of buttons (ex. Gtk.SHADOW_OUT) are different in the python version.\n\n This can lead to much frustruation, especially because documentation is sometimes inconsistant or out of date"
		fake1=Comment(text1,"10:20","Random Hash","This file","Some account")
		fake2=Comment(text2,"10:35","Random Hash","This file","Some account")
		fake3=Comment(text3,"10:47","Random Hash","This file","Some account")
		fake4=Comment(text4,"11:00","Random Hash","This file","Some account")
		linecommentlist=[fake4,fake3,fake2,fake1]
		return linecommentlist

# Not quite sure how to do this one. It needs to dynamically create a revision map for the whole project and allow you to move from one revision to another as well as load those revision. 
	def create_revision_map(self):
		return notsure	

#What happens when you click on the list comments only button
	def on_List_toggled(self,button,which,other,vbox):
		if button.get_active()==True:
			children=vbox.get_children()
			index=0
			while index<len(children):
				children[index].destroy()
				index=index+1	
			linecomments=self.get_line_comments("This File")
			index=0
			while index<len(linecomments):
				vbox.pack_start(self.create_comment(linecomments[index]),False,False,0)
				index=index+1	
			other.set_active(False)
			vbox.show_all()

#What happens when you click on the file comments only button
	def on_Line_toggled(self,button,which,other,vbox):	
		if button.get_active()==True:
			children=vbox.get_children()
			index=0
			while index<len(children):
				children[index].destroy()
				index=index+1
			filecomments=self.get_file_comments("This File")
			index=0
			while index<len(filecomments):
				vbox.pack_start(self.create_comment(filecomments[index]),False,False,0)
				index=index+1	
			other.set_active(False)
			vbox.show_all()

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
		self.submit_file_comment(account,thetext)
		return

#Creates the top toolbar for the window.
	def create_toolbar(self):
		
		self.toolbar=Gtk.Toolbar()
		self.toolbar.set_size_request(self.x-150,10)
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
		button_editor.connect("clicked",change_window,"Editor",self,self.parent)

		explorer_icon=Gtk.Image.new_from_file('explorer-icon.png')
		button_explorer=Gtk.ToolButton()
		button_explorer.set_icon_widget(explorer_icon)
		self.toolbar.insert(button_explorer, 3)
		button_explorer.connect("clicked",change_window,"Explorer",self,self.parent)

		sep=Gtk.SeparatorToolItem()
		self.toolbar.insert(sep,4)

		fork_icon=Gtk.Image.new_from_file('fork-icon.png')
		button_fork=Gtk.ToolButton()
		button_fork.set_icon_widget(fork_icon)
		self.toolbar.insert(button_fork, 5)
		button_explorer.connect("clicked",self.fork_file)

		self.toolbar.show_all()

	def on_key_press(self,widget,data):
		#runs when any key is pressed
		#c is 99

		val=data.keyval #get the pressed key
		if val==99:
			if Gdk.ModifierType.CONTROL_MASK&data.state==Gdk.ModifierType.CONTROL_MASK:
				self.copy_text()

	def copy_text(self,widget=None):
		date=datetime.date.today()
		select=self.thecodebuffer.get_selection_bounds()
		if select==():
			self.parent.borrows[0].get_text()
			print 'There\'s nothing selected, you kiwi.'
		else:
			line1=select[0].get_line()
			line2=select[1].get_line()
			lineoffset1=select[0].get_line_offset()
			lineoffset2=select[1].get_line_offset()
			offset1=select[0].get_offset()
			offset2=select[1].get_offset()
			if line1==line2:
				self.copy=Borrow(date,'self.project.projID','self.revision','self.file.file_name',(line1,line1),(lineoffset1,lineoffset2))
			else:
				self.copy=Borrow(date,'self.project.projID','self.revision','self.file.file_name',(line1,line2),(lineoffset1,lineoffset2))
			self.parent.borrows.append(self.copy)
			Gtk.Clipboard.set_text(Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD),self.thecodebuffer.get_text(select[0],select[1],True),-1)

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

	def fork_file(self,widget):
		print 'Would you like a spoon instead?'
		pass

###-------------------------ADDITIONAL WINDOWS-----------------------###
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
		self.spinsubmit.connect("clicked", self.dialog_toggle_line_comment,self.spinbutton,parent)
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

	def dialog_toggle_line_comment(self,button,spinner,parent):
		#account=get_account()
		entry=parent.entry
		account="The Instigater"
		tempbuffer=entry.get_buffer()
		startiter = tempbuffer.get_start_iter()
		enditer = tempbuffer.get_end_iter()
		thetext=tempbuffer.get_text(startiter,enditer,False)
		submit_line_comment(parent,account,str(spinner.get_value()),thetext)
		self.destroy()
