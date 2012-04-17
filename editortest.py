from gi.repository import Gtk, Gdk, GtkSource, GObject

class Editor(Gtk.Window):

	def __init__(self,parent,project,revision,file):
		Gtk.Window.__init__(self,title='tanCS Editor')
		
		self.parent=parent
		self.on_window_mode_changed=parent.on_window_mode_changed

		#structure rewrite
		self.set_default_size(800,500)
		self.vbox_top = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
		self.vbox_top.set_homogeneous(False)
		self.add(self.vbox_top)
		self.scrolledwindow = Gtk.ScrolledWindow()
		self.scrolledwindow.set_hexpand(True)
		self.scrolledwindow.set_vexpand(True)
		self.statusbar=Gtk.Statusbar()

		#toolbar
		self.create_toolbar()

		self.borrows=()

		self.vbox_top.pack_start(self.toolbar,False,True,0)
		self.vbox_top.pack_start(self.scrolledwindow,True,True,0)
		self.vbox_top.pack_start(self.statusbar,False,True,0)
		
		#create gtksourceview objects
		self.sbuff = GtkSource.Buffer()
		self.sview = GtkSource.View()
		self.sview.set_buffer(self.sbuff)

		#set syntax highlighting to python
		self.lang = GtkSource.LanguageManager.get_default().get_language('python')
		self.sbuff.set_language(self.lang)

		#add sourceview to window and initialize properties
		Gtk.ScrolledWindow.add(self.scrolledwindow,self.sview)
		self.sbuff.set_text('Lorem ipsum dolor sit amet, \nconsectetur adipiscing elit. Sed et \nenim vitae augue dictum vehicula. Duis \nsit amet velit ipsum. Donec n\nibh leo, blandit et porttitor quis, aliquet sed est. Nam mollis pellentesque orci id pharetra. Curabitur eros arcu, mollis in ultricies nec, convallis a risus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Ut pharetra leo quis risus volutpat porta. Praesent bibendum mi nec erat scelerisque vitae pellentesque massa eleifend. Aliquam aliquet venenatis odio id hendrerit. Nulla accumsan tincidunt mauris, nec mollis justo feugiat sit amet. Nullam quis sagittis neque. Integer dui augue, molestie vel semper at, iaculis sed metus. Mauris tempor nibh quis sem pellentesque vulputate. Nullam varius magna rhoncus lectus tempor at viverra tellus pretium.')
		self.sview.show()
		self.sview.connect("key-press-event",self.on_key_press)


	def on_key_press(self,widget,data):
		#runs when any key is pressed

		#Space is 32
		#Tab is 65289
		#Backspace is 65288
		#Enter is 65293
		#c is 99
		#v is 118
		#x is 120
		#Ctrl is 65507
		val=data.keyval #get the pressed key
		cursor=self.sbuff.get_iter_at_mark(self.sbuff.get_insert()) #get iter at cursor position
		back=self.sbuff.get_iter_at_offset(cursor.get_offset()-1) #get iter at cursor position-1
		if val==65289: #tab key ####TODO: what if user selects text
			self.sbuff.insert(cursor,'    ') #insert 4 spaces
			return True #repress normal tab key
		elif val==65288: #backspace key
			if self.sbuff.get_selection_bounds()==(): #if no text is selected
				backfour=self.sbuff.get_iter_at_offset(cursor.get_offset()-4) #get iter at cursor position-4
				txt=self.sbuff.get_text(backfour,cursor,True) #get preceding 4 characters
				if txt=='    ': #if preceding text is 4 spaces
					self.sbuff.delete(backfour,cursor) #delete the preceding "tab"
				else:
					self.sbuff.delete(back,cursor) #normal backspace
				return True #repress normal backspace key
			else:
				return False
		elif val==65293: #enter key
			indent=self.check_indent(cursor) #check how far the previous line was indented
			if self.check_colon(cursor): #check if previous line ended in colon
				spaces='    '*(indent+1) #auto-indent block
			else:
				spaces='    '*indent #match indent
			self.sbuff.insert(cursor,'\n'+spaces) #insert appropriate number of "tabs"
			return True #repress normal enter key
		elif val==99:
			if Gdk.ModifierType.CONTROL_MASK&data.state==Gdk.ModifierType.CONTROL_MASK:
				self.copy_text()
		elif val==120:
			if Gdk.ModifierType.CONTROL_MASK&data.state==Gdk.ModifierType.CONTROL_MASK:
				self.cut_text()
		elif val==118:
			if Gdk.ModifierType.CONTROL_MASK&data.state==Gdk.ModifierType.CONTROL_MASK:
				self.paste_text()
				return True

	def check_colon(self,cursor):
		#check if previous line ended in a colon
		offset=cursor.get_offset()
		back=self.sbuff.get_iter_at_offset(offset-1)
		if self.sbuff.get_slice(back,cursor,True)==':': #TODO: what if whitespace? or comment?
			return True
		else:
			return False

	def get_line_start(self,cursor):
		#find the start of the line
		offset=cursor.get_offset()
		txt=' '
		i=0
		while not (txt == ('\n' or '\r') or (offset-i)<1):
			backa=self.sbuff.get_iter_at_offset(offset-i)
			backb=self.sbuff.get_iter_at_offset(offset-i-1)
			txt=self.sbuff.get_slice(backb,backa,True)
			i+=1
		if txt==('\n' or '\r'):
			offset=backa.get_offset()
		else:
			offset=0
		return offset

	def check_indent(self,cursor):
		#check how far the previous line was indented
		txt=' '
		i=0
		offset=self.get_line_start(cursor)

		#count number of 4-space strings at start of line
		i=0
		indent=0
		backa=self.sbuff.get_iter_at_offset(offset)
		backb=self.sbuff.get_iter_at_offset(offset+4)
		txt=self.sbuff.get_slice(backa,backb,True)
		while txt == '    ':
			indent+=1
			i+=1
			backa=self.sbuff.get_iter_at_offset(offset+4*i)
			backb=self.sbuff.get_iter_at_offset(offset+4*i+4)
			txt=self.sbuff.get_slice(backa,backb,True)
		return indent

	def on_button_clicked(self,widget):
		print "Hello World" #test func

	def copy_text(self,widget=None):
		#TODO: get URL of source? offer to add source to user?
		print 'copying'

	def cut_text(self,widget=None):
		print 'cutting'

	def paste_text(self,widget=None):
		pasted = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD).wait_for_text()
		if self.isBorrow(pasted):
			print self.parent.borrows[0].line_range
		else:
			dialog = ReferenceDialog(self,pasted)
			response = dialog.run()
			if response==Gtk.ResponseType.OK:
				text=dialog.reference.get_text()
				if not text.strip()==None:
					print 'Source cited:'+text
					#TODO: create a new Borrow object
			dialog.destroy()

	def isBorrow(self,text):
		if not self.borrows==():
			return False
		else:
			pass
		return True

	def indent_block(self,widget):
		print 'indenting block'
		select=self.sbuff.get_selection_bounds()
		if not select==():
			lines=self.get_lines_from_block(select)
		else:
			lines=[self.get_line_start(self.sbuff.get_iter_at_mark(self.sbuff.get_insert()))]
		count=0
		for line in lines:
			line+=count
			self.sbuff.insert(self.sbuff.get_iter_at_offset(line),'    ')
			count+=4

	def unindent_block(self,widget):
		print 'unindenting block'
		select=self.sbuff.get_selection_bounds()
		if not select==():
			lines=self.get_lines_from_block(select)
		else:
			lines=[self.get_line_start(self.sbuff.get_iter_at_mark(self.sbuff.get_insert()))]
		count=0
		for line in lines:
			line+=count
			itera=self.sbuff.get_iter_at_offset(line)
			iterb=self.sbuff.get_iter_at_offset(line+4)
			txt=self.sbuff.get_slice(itera,iterb,True)
			if txt=='    ':
				self.sbuff.delete(itera,iterb)
				count-=4

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

	def comment_block(self,widget):
		select=self.sbuff.get_selection_bounds()
		if not select==():
			lines=self.get_lines_from_block(select)
			count=0
			print lines
			uncomment=True
			#PRE: lines must be ordered lowest to highest
			for line in lines:
				line+=count
				offset=line
				txt=' '
				while txt==' ':
					itera=self.sbuff.get_iter_at_offset(offset)
					iterb=self.sbuff.get_iter_at_offset(offset+1)
					txt=self.sbuff.get_slice(itera,iterb,True)
					offset+=1
				if uncomment:
					uncomment = (txt=='#')
				print uncomment

			for line in lines:
				line+=count
				txt=' '
				offset=line
				while txt==' ':
					itera=self.sbuff.get_iter_at_offset(offset)
					iterb=self.sbuff.get_iter_at_offset(offset+1)
					txt=self.sbuff.get_slice(itera,iterb,True)
					offset+=1
				if uncomment:
					print 'delete'
					self.sbuff.delete(itera,iterb)
					count-=1
				else:
					print 'comment'
					self.sbuff.insert(itera,'#')
					count+=1
		else:
			cursor=self.sbuff.get_iter_at_mark(self.sbuff.get_insert()) #get iter at cursor position
			offset=self.get_line_start(cursor)
			txt=' '
			while txt==' ':
				itera=self.sbuff.get_iter_at_offset(offset)
				iterb=self.sbuff.get_iter_at_offset(offset+1)
				txt=self.sbuff.get_slice(itera,iterb,True)
				offset+=1
			if txt=='#':
				print 'delete'
				self.sbuff.delete(itera,iterb)
			else:
				print 'comment'
				self.sbuff.insert(itera,'#')



	def create_toolbar(self):
		self.toolbar=Gtk.Toolbar()
		button_new=Gtk.ToolButton.new_from_stock(Gtk.STOCK_NEW)
		self.toolbar.insert(button_new, 0)
		button_new.set_tooltip_text('New File')
		#button_new.connect("clicked", self.create_new)

		button_savepoint=Gtk.ToolButton.new_from_stock(Gtk.STOCK_SAVE)
		self.toolbar.insert(button_savepoint, 1)
		button_savepoint.set_tooltip_text('Save to New Revision')
		#button_savepoint.connect("clicked", self.create_save_point)

		button_copy=Gtk.ToolButton.new_from_stock(Gtk.STOCK_COPY)
		self.toolbar.insert(button_copy, 2)
		button_copy.set_tooltip_text('Copy')
		button_copy.connect("clicked", self.copy_text)

		button_cut=Gtk.ToolButton.new_from_stock(Gtk.STOCK_CUT)
		self.toolbar.insert(button_cut, 3)
		button_cut.set_tooltip_text('Cut')
		button_cut.connect("clicked", self.cut_text)

		button_paste=Gtk.ToolButton.new_from_stock(Gtk.STOCK_PASTE)
		self.toolbar.insert(button_paste, 4)
		button_paste.set_tooltip_text('Paste')
		button_paste.connect("clicked", self.paste_text)

		comment_icon=Gtk.Image.new_from_file('comment-icon.png')
		button_comment=Gtk.ToolButton()
		button_comment.set_icon_widget(comment_icon)
		button_comment.set_tooltip_text('Toggle comment on code block')
		self.toolbar.insert(button_comment, 5)
		button_comment.connect("clicked", self.comment_block)

		button_indent=Gtk.ToolButton.new_from_stock(Gtk.STOCK_INDENT)
		self.toolbar.insert(button_indent, 6)
		button_indent.set_tooltip_text('Indent code block')
		button_indent.connect("clicked", self.indent_block)

		button_unindent=Gtk.ToolButton.new_from_stock(Gtk.STOCK_UNINDENT)
		self.toolbar.insert(button_unindent, 7)
		button_unindent.set_tooltip_text('Unindent code block')
		button_unindent.connect("clicked", self.unindent_block)
		button_unindent.set_label('hello')

		sep=Gtk.SeparatorToolItem()
		self.toolbar.insert(sep,8)
		
		viewer_icon=Gtk.Image.new_from_file('viewer-icon.png')
		button_viewer=Gtk.ToolButton()
		button_viewer.set_icon_widget(viewer_icon)
		button_viewer.set_tooltip_text('Switch to Viewer')
		self.toolbar.insert(button_viewer, 9)
		button_viewer.connect("clicked", change_window,"Viewer",self,self.parent)

		explorer_icon=Gtk.Image.new_from_file('explorer-icon.png')
		button_explorer=Gtk.ToolButton()
		button_explorer.set_icon_widget(explorer_icon)
		button_explorer.set_tooltip_text('Switch to Explorer')
		self.toolbar.insert(button_explorer, 10)
		button_explorer.connect("clicked",change_window,"Explorer",self,self.parent)

		sep2=Gtk.SeparatorToolItem()
		self.toolbar.insert(sep2,11)

		run_icon=Gtk.Image.new_from_file('run-icon.png')
		button_run=Gtk.ToolButton()
		button_run.set_icon_widget(run_icon)
		button_run.set_tooltip_text('Run Program')
		self.toolbar.insert(button_run, 12)
		button_run.connect("clicked",self.run_file)

		level_icon=Gtk.Image.new_from_file('level-icon.png')
		button_level=Gtk.ToolButton()
		button_level.set_icon_widget(level_icon)
		button_level.set_tooltip_text('Level Select')
		self.toolbar.insert(button_level, 13)
		button_level.connect("clicked",self.level_select)

		self.toolbar.show_all()

	def level_select(self, widget):
		pass

	def run_file(self,widget):
		pass

def change_window(widget,new_window_name,parent_window,top_parent):
	top_parent.on_window_mode_changed(new_window_name,parent_window)


class ReferenceDialog(Gtk.Dialog):
	def __init__(self,parent,text):
		#Gtk.Dialog.__init__(self, "Search", parent,Gtk.DialogFlags.MODAL, buttons=(Gtk.STOCK_FIND, Gtk.ResponseType.OK,Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

		Gtk.Dialog.__init__(self, flags=Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT, title="My Dialog", parent=parent, buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
		
		self.text=text
		length=len(self.text)
		if length>80:
			self.text=self.text[:40]+'......'+self.text[length-40:]
		self.label1=Gtk.Label('You\'re copying the following into your project:\n')
		self.label2=Gtk.Label('"'+self.text+'"')
		self.label3=Gtk.Label('\nPlease cite your source by entering it in the box below.\n\n')
		self.reference=Gtk.Entry()
		box=self.get_content_area()
		box.add(self.label1)
		box.add(self.label2)
		box.add(self.label3)
		box.add(self.reference)

		self.show_all()

'''
#initiate window
win = Editor(-1)
win.connect("delete-event",Gtk.main_quit)
win.show_all()
Gtk.main()'''
