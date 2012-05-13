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
	top_parent.on_window_mode_changed(new_window_name,parent_window,parent_window.activeproject,parent_window.activerev,parent_window.activefile)

###------------------------------Viewer Class------------------------------###
class TempWindow(Gtk.Window):
	def __init__(self,parent,activeproject,activerev,activefile):
		Gtk.Window.__init__(self,title="tanCS IDE - Viewer")
		renderall = not(activerev==None and activefile==None) #enable full functionality
		#pdb.set_trace()
		self.activeproject=activeproject
		self.activerev=activerev
		self.activefile=activefile

		#TODO: remove this, integrate account with explorer
		self.fake_user=Account("Random Hash","The instigator","Password","Avatar")

		color=Gdk.Color(1000,1000,1000)
		#self.set_resizable(False)
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

		#self.embed.connect("button-press-event",self.stageclicked)
		imagebox.pack_start(self.embed,True,True,0)

		self.render_clutter()

		imageframe=Gtk.Frame()
		imageframe.add(imagebox)
		self.embed.set_size_request(200,600)
		#TODO
		self.toplevel=Gtk.HPaned()
		#self.toplevel=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
		self.toplevel.set_size_request(self.x,self.y)
		self.add(self.toplevel)
		#self.toplevel.pack_start(menubar,False,False,0)
		self.toplevel.pack1(imageframe,True,True)


		#vbox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
		#self.add(vbox)
		vbox=Gtk.VPaned()

		self.thecode=GtkSource.View()
		self.thecodebuffer = GtkSource.Buffer()
		self.thecode.set_buffer(self.thecodebuffer)
		if renderall:
			self.thecodebuffer.set_text(self.activeproject.revisions[activerev].files[activefile].content)
		self.thecode.set_show_line_numbers(True)
		#self.thecode.set_size_request(self.x-150,560)
		self.thecodeframe=Gtk.Frame()
		self.thecodeframe.add(self.thecode)
		self.thecode.set_editable(False)
		self.thecode.connect("key-press-event",self.on_key_press)
		lang = GtkSource.LanguageManager.get_default().get_language('python')
		self.thecodebuffer.set_language(lang)
		codescroll=Gtk.ScrolledWindow()
		codescroll.add_with_viewport(self.thecodeframe)
		#codescroll.set_size_request(self.x-150,390)
		codescroll.set_size_request(self.x-150,260)
		vbox4=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
		vbox4.pack_start(self.toolbar,False,False,0)
		vbox4.pack_start(codescroll,True,True,0)
		
		vbox.pack1(vbox4,True,True)

		hbox=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
		self.vbox2=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		self.filebutton=Gtk.ToggleButton("File comments")
		self.linebutton=Gtk.ToggleButton("Line comments")
		
		self.filebuttonhandler=self.filebutton.connect("clicked", self.on_File_toggled)
		self.linebuttonhandler=self.linebutton.connect("clicked", self.on_Line_toggled)
		hbox.pack_end(self.linebutton,False, False,0)
		hbox.pack_end(self.filebutton,False, False,0)

		if renderall:
			self.on_File_toggled(self.filebutton)

		#vbox.pack_start(hbox, False, False,0)

		commentswindow = Gtk.ScrolledWindow()
		#commentswindow.set_size_request(200,95)
		commentswindow.set_hexpand(True)
		commentswindow.set_vexpand(True)
		
		frame=Gtk.Frame()
		
		self.padding=Gtk.EventBox()
		self.padding.set_border_width(15)
		self.padding.add(self.vbox2)
		
		commentswindow.add_with_viewport(self.padding)
		#commentswindow.set_size_request(self.x-150,180)
		commentbox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		commentbox.pack_start(hbox,False,False,0)
		commentbox.pack_start(commentswindow,True,True,0)
		frame.add(commentbox)

		hbox2=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
		entryframe=Gtk.Frame()
		self.entry=Gtk.TextView()
		# Don't change the name of this text view, it is connected to the pop up window for submit line number.
		entryframe.add(self.entry)
		self.comment_buffer=self.entry.get_buffer()
		self.comment_buffer.set_text("Thanks a bunch!")

		commentscroll=Gtk.ScrolledWindow()
		commentscroll.add_with_viewport(entryframe)
		#commentscroll.set_size_request(self.x-150,60)

		self.submitcomment=Gtk.Button("Submit")
		self.submitcomment.connect("clicked", self.toggle_file_comment)

		self.submitlinecomment=Gtk.Button("Submit Line Comment")
		self.submitlinecomment.connect("clicked", self.toggle_line_comment)
		
		vbox3=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		vbox3.pack_start(self.submitlinecomment,True,True,0)
		vbox3.pack_start(self.submitcomment,True,True,0)

		hbox2.pack_start(commentscroll,True,True,0)
		hbox2.pack_start(vbox3,False,False,0)
		vbox5=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
		vbox5.pack_start(frame,True,True,0)
		vbox5.pack_start(hbox2,False,False,0)
		vbox.pack2(vbox5,True,True)
		#vbox.pack_start(embed,True,True,0)

		self.thecode.connect('populate-popup',self.code_clicked)

		if not renderall:
			self.thecodebuffer.set_text('Please select a file to view from one of the revisions on the map at left.')
			self.linebutton.set_sensitive(False)
			self.filebutton.set_sensitive(False)
			self.submitcomment.set_sensitive(False)
			self.submitlinecomment.set_sensitive(False)
			self.toolbar.get_nth_item(2).set_sensitive(False)
			self.toolbar.get_nth_item(4).set_sensitive(False)

		self.toplevel.pack2(vbox,True,True)
		#Gtk.UIManager()

###---------------------------------METHODS--------------------------------###

	def render_clutter(self):
		self.stage = self.embed.get_stage()	# Get the Stage
		self.stage.set_no_clear_hint(False)
		self.stage.ensure_redraw()
		self.stage.set_title("tanCS IDE - Viewer")		# Stage's title
		self.stage.connect("motion-event",self.mouse_moved)
		self.stage.connect("leave-event",self.leave_clutter)
		white=Clutter.Color.new(255,255,255,255)
		black=Clutter.Color.new(0,0,0,255)
		blue = Clutter.Color.new(0,0,255,255) # red,green,blue,alpha
		self.stage.set_color(white)
		self.stage.set_reactive(True)

		self.scroll=0
		
		self.toptext = Clutter.Text.new_full("Sans 20", "Revision Map", blue)
		self.toptext.set_reactive(True)
		Clutter.Container.add_actor(self.stage, self.toptext)
		self.toptext.set_position(15,5)

		num_revs=len(self.activeproject.revisions)

		#pdb.set_trace()

		#nested lists containing the various clutter objects within a revision circle
		#[circle,label,files,isopen,ishead]
		self.circles=[] 

		headcircle=Clutter.Texture.new_from_file("headcircle.png");
		Clutter.Container.add_actor(self.stage, headcircle)
		headcircle.set_position(50,50)
		headcircle.set_size(100,100)
		headcircle.set_reactive(True)
		headcircle.connect('button-press-event',self.revclick,0)
		headcircle.connect('enter-event',self.revhover,0)
		headcircle.connect('leave-event',self.revleave,0)

		headlabel=Clutter.Text.new_full("Serif 20","Head",black)
		Clutter.Container.add_actor(self.stage,headlabel)
		headlabel.set_anchor_point(headlabel.get_size()[0]/2.0,headlabel.get_size()[1]/2.0)
		headlabel.set_position(100,100)

		self.circles.append([headcircle,headlabel,[],False,True])

		for i in range(num_revs-1):
			rev=num_revs-i-1
			newcircle=Clutter.Texture.new_from_file("circle.png");
			Clutter.Container.add_actor(self.stage, newcircle)
			newcircle.set_position(50,125*(i+1)+50)
			newcircle.set_size(100,100)
			newcircle.set_reactive(True)
			newcircle.connect('button-press-event',self.revclick,i+1)
			newcircle.connect('enter-event',self.revhover,i+1)
			newcircle.connect('leave-event',self.revleave,i+1)

			newlabel=Clutter.Text.new_full("Serif 20","Rev "+str(rev),black)
			Clutter.Container.add_actor(self.stage,newlabel)
			newlabel.set_anchor_point(newlabel.get_size()[0]/2.0,newlabel.get_size()[1]/2.0)
			newlabel.set_position(100,125*(i+1)+100)

			self.circles.append([newcircle,newlabel,[],False,False])

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
		flag=(not self.circles[revnum][3])
		self.reset_clutter()
		num_revs=len(self.activeproject.revisions)
		if flag:
			filelabels=[]
			starty=self.circles[revnum][0].get_position()[1]+100
			numfiles=0
			#if self.circles[revnum][4]:
				#files=self.activeproject.head.files
			#else:
			files=self.activeproject.revisions[len(self.activeproject.revisions)-revnum-1].files
			print files
			#pdb.set_trace()
			for f in files:
				numfiles+=1
				#pdb.set_trace()
				newlabel=Clutter.Text.new_full("Serif 12",files[f].file_name,black)
				Clutter.Container.add_actor(self.stage,newlabel)
				newlabel.set_anchor_point(newlabel.get_size()[0]/2.0,newlabel.get_size()[1]/2.0)
				newlabel.set_position(100,starty+25*numfiles)
				newlabel.set_reactive(True)
				newlabel.connect('button-press-event',self.openfile,files[f])
				newlabel.connect('enter-event',self.filehover,revnum,numfiles-1)
				newlabel.connect('leave-event',self.fileleave,revnum,numfiles-1)
				filelabels.append(newlabel)
			self.circles[revnum][2]=filelabels
			for i in range(len(self.circles)-(revnum+1)):
				i+=revnum+1
				self.circles[i][0].move_by(0,25+25*numfiles)
				self.circles[i][1].move_by(0,25+25*numfiles)
			self.circles[revnum][3]=True

	def revhover(self,widget,data,revnum):
		red=Clutter.Color.new(255,0,0,255)
		self.circles[revnum][1].set_color(red)

	def revleave(self,widget,data,revnum):
		black=Clutter.Color.new(0,0,0,255)
		self.circles[revnum][1].set_color(black)

	def filehover(self,widget,data,revnum,filenum):
		blue=Clutter.Color.new(0,10,255,255)
		self.circles[revnum][2][filenum].set_color(blue)

	def fileleave(self,widget,data,revnum,filenum):
		black=Clutter.Color.new(0,0,0,255)
		self.circles[revnum][2][filenum].set_color(black)

	def enter_clutter(self,widget,data=-1):
		self.embed.grab_focus()

	def mouse_moved(self,widget,event):
		miny=200
		maxy=self.embed.get_allocation().height-200
		self.curr_y=event.get_coords()[1]
		if self.curr_y<miny:
			GObject.timeout_add(50,self.scrollup)
			self.scrollOn=True
		if self.curr_y>maxy:
			GObject.timeout_add(50,self.scrolldown)
			self.scrollOn=True

	def scrollup(self,data=None):
		if self.scroll<0:
			self.scroll+=.5
			self.reset_clutter()
			miny=150
			maxy=self.embed.get_allocation().height-200
			if self.curr_y<miny:
				return self.scrollOn
			else:
				return False
		else:
			return False

	def scrolldown(self,data=None):
		self.scroll-=.5
		self.reset_clutter()
		miny=100
		maxy=self.embed.get_allocation().height-200
		if self.curr_y>maxy:
			return self.scrollOn
		else:
			return False


	def leave_clutter(self,widget,data):
		self.scrollOn=False

	def openfile(self,widget=None,data=None,f=None):
		print 'Opening '+f.file_name
		self.thecodebuffer.set_text(f.content)
		self.activerev=f.rev_number
		self.activefile=f.file_name

		print self.activerev

		if self.filebutton.get_active()==True:
			self.on_File_toggled(self.filebutton)
		else:
			self.on_Line_toggled(self.linebutton)

		if self.filebutton.get_sensitive()==False:
			self.linebutton.set_sensitive(True)
			self.filebutton.set_sensitive(True)
			self.submitcomment.set_sensitive(True)
			self.submitlinecomment.set_sensitive(True)
			self.toolbar.get_nth_item(2).set_sensitive(True)
			self.toolbar.get_nth_item(4).set_sensitive(True)
			self.on_File_toggled(self.filebutton)

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
		linenum=comment.linenum
		if linenum==-1:
			temp_title=Gtk.Label("<b>"+comment.account.username+"</b>")
		else:
			temp_title=Gtk.Label("<b>"+comment.account.username+" (in reference to line "+str(linenum)+")"+"</b>")
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
		fake1=Comment(text1,"10:20","Random Hash",1,"This file",self.fake_user,-1)
		fake2=Comment(text2,"10:35","Random Hash",1,"This file",self.fake_user,-1)
		fake3=Comment(text3,"10:47","Random Hash",1,"This file",self.fake_user,-1)
		fake4=Comment(text4,"11:00","Random Hash",1,"This file",self.fake_user,-1)
		filecommentlist=[]
		#pdb.set_trace()
		for comment in self.activeproject.revisions[self.activerev].files[self.activefile].comments:
			if comment.linenum==-1:
				filecommentlist.append(comment)
		#filecommentlist=[fake1,fake2,fake3,fake4]
		return filecommentlist

#should unpack the line comments from where they are in revision and make a list of all of them so that they can be displayed.
	def get_line_comments(self,revision):
		text1="I see how you have added many oranges. Is there any way to dynamically create widgets?"
		text2="Well, yes and no. It's a little hard, but you can definitely do it. Papayas?"
		text3="Thanks for the help. Also, I saw that there are some variables that just seem to come out of nowhere like 'clicked' and 'label'. Where do these come from?"
		text4="They are variables that Gtk has included in it. When you import they get recognized. \n\nHowever, it is important to recognize that the c++ library for Gtk+ and the python bindings for gtk are slightly different.\n\n For instance, most of the final variables associated with the style attributes of buttons (ex. Gtk.SHADOW_OUT) are different in the python version.\n\n This can lead to much frustruation, especially because documentation is sometimes inconsistant or out of date"
		fake1=Comment(text1,"10:20","Random Hash",1,"This file",self.fake_user,6)
		fake2=Comment(text2,"10:35","Random Hash",1,"This file",self.fake_user,4)
		fake3=Comment(text3,"10:47","Random Hash",1,"This file",self.fake_user,32)
		fake4=Comment(text4,"11:00","Random Hash",1,"This file",self.fake_user,12)
		linecommentlist=[fake4,fake3,fake2,fake1]
		return linecommentlist

# Not quite sure how to do this one. It needs to dynamically create a revision map for the whole project and allow you to move from one revision to another as well as load those revision. 
	def create_revision_map(self):
		return notsure	

#What happens when you click on the line comments only button
	def on_Line_toggled(self,button):
		if button.get_active()==False:
			button.handler_block(self.linebuttonhandler)
			button.set_active(True)
			button.handler_unblock(self.linebuttonhandler)
		children=self.vbox2.get_children()
		index=0
		while index<len(children):
			children[index].destroy()
			index=index+1	
		linecomments=self.get_line_comments("This File")
		index=0
		while index<len(linecomments):
			self.vbox2.pack_start(self.create_comment(linecomments[index]),False,False,0)
			index=index+1
		self.filebutton.handler_block(self.filebuttonhandler)
		self.filebutton.set_active(False)
		self.filebutton.handler_unblock(self.filebuttonhandler)
		self.vbox2.show_all()

#What happens when you click on the file comments only button
	def on_File_toggled(self,button):
		if button.get_active()==False:
			button.handler_block(self.filebuttonhandler)
			button.set_active(True)
			button.handler_unblock(self.filebuttonhandler)
		children=self.vbox2.get_children()
		index=0
		while index<len(children):
			children[index].destroy()
			index=index+1
		filecomments=self.get_file_comments("This File")
		index=0
		while index<len(filecomments):
			self.vbox2.pack_start(self.create_comment(filecomments[index]),False,False,0)
			index=index+1	
		self.linebutton.handler_block(self.linebuttonhandler)
		self.linebutton.set_active(False)
		self.linebutton.handler_unblock(self.linebuttonhandler)
		self.vbox2.show_all()

#What happens when you hit the submit line comment button
	def toggle_line_comment(self,widget):
		tempbuffer=self.entry.get_buffer()
		startiter = tempbuffer.get_start_iter()
		enditer = tempbuffer.get_end_iter()
		thetext=tempbuffer.get_text(startiter,enditer,False)
		if len(thetext)>0:
			dialog=LineCommentDialog(self)
			endresult=dialog.run()
			tempbuffer.set_text('')

#What happens when you hit the submit file comment button.
	def toggle_file_comment(self,widget):
		#account=get_account()
		account="The Instigater"
		tempbuffer=self.entry.get_buffer()
		startiter = tempbuffer.get_start_iter()
		enditer = tempbuffer.get_end_iter()
		thetext=tempbuffer.get_text(startiter,enditer,False)
		if len(thetext)>0:
			self.submit_file_comment(account,thetext)
			tempbuffer.set_text('')
		return

	#How the user creates file comments. This involves just typing what the comment is in the gtkentry at the bottom. When they hit submit this function will be called and this will add a file comment to the code.
	def submit_file_comment(self,account,text):
		time=datetime.date.today()
		new_comment=Comment(text,time,"Hash",self.activerev,self.activefile,self.fake_user,-1)
		self.activeproject.revisions[self.activerev].files[self.activefile].comments.append(new_comment)
		if self.filebutton.get_active():
			self.vbox2.pack_start(self.create_comment(new_comment),False,False,0)
			self.vbox2.show_all()
		print(account+" says: '"+text+"' about this file")
		return

	def submit_line_comment(self,account,text,linenum):
		time=datetime.date.today()
		new_comment=Comment(text,time,"Hash",self.activerev,self.activefile,self.fake_user,linenum)
		self.activeproject.revisions[self.activerev].files[self.activefile].comments.append(new_comment)
		if self.linebutton.get_active():
			self.vbox2.pack_start(self.create_comment(new_comment),False,False,0)
			self.vbox2.show_all()
		print(account+" says: '"+text+"' about this file")
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

	def code_clicked(self,widget,menu,event=None):
		#print event.button
		menu.append(Gtk.MenuItem('hello'))
		print 'clicked'
		return menu
		#Gtk.Menu.popup(Gtk.Menu(),None,None,None,None,event.button,event.time)

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
				self.copy=Borrow(date,self.activeproject,self.activerev,self.activefile,(line1,line1),(lineoffset1,lineoffset2))
			else:
				self.copy=Borrow(date,self.activeproject,self.activerev,self.activefile,(line1,line2),(lineoffset1,lineoffset2))
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
		adjustment = Gtk.Adjustment(1, 1, parent.thecode.get_buffer().get_line_count(), 1, 10, 0)
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
		parent.submit_line_comment(account,thetext,str(spinner.get_value()))
		self.destroy()
