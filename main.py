###------------------------------Inclusions--------------------------------###
from gi.repository import GtkClutter
GtkClutter.init([])
from gi.repository import Gtk,GObject
from gi.repository import Gdk
import Viewer as viewer
import Editor as editor
import Explorer as explorer
from objectcode import *
import os
import platform
import subprocess
import pdb

#------TODOS------
# Implement forking projects
# Do error testing
# Long-term: Create massive Clutter borrow map


#-------DONE-------
# Implemented make revision and cut in Editor
# Implemented deepcopy stuff so that objects are actually copied over, esp File
# Fixed Borrow linking
# Add borrow "to" attributes (done, I think)
# Add click-drag-resize ability to Viewer (hooray, Brendan!)
# Add copy/paste override to context menu
# Add line comment to context menu
# Viewer popup menu is fixed, for certain definitions of fixed.
# Implemented new file button in Viewer and Editor

class tanCS(object):

	def __init__(self):
		self.user=None
		self.borrows=[]
		
		#The following code creates a tanCS preferences directory.
		#I don't remember why I wrote it, so it's commented for now.
		'''
		#Checks whether user preference files already exist; if not, creates them.
		self.USERPATH=os.path.expanduser('~')
		osname=platform.system()
		if osname=='Linux':
			self.USERPATH+='/.tanCS'
			print self.USERPATH
			if not os.path.exists(self.USERPATH):
				print 'Creating new pref file'
				subprocess.call('mkdir '+self.USERPATH,shell=True)
		elif osname=='Windows':
			self.USERPATH+='\\.tanCS'
			if not os.path.exists(self.USERPATH):
				subprocess.call('mkdir '+self.USERPATH,shell=True)
				subprocess.call('attrib +h '+self.USERPATH,shell=True)
		else:
			print 'ERROR: You appear to be using an unsupported OS.'
		'''
		
		#in the process of creating default objects
		self.defaultgroup=Group('groupHASH',set('userHASH'),'godHASH',"default group")
		self.defaultaccount=Account('userHASH', 'oranges', 'kiwi', 'explorer-icon.png')
		self.defaultproject=Project('The default!','A dummy project.', 'proj01',None, 8, 'groupHASH')
		#THESE SHOULDS BE OF A FUNCTION
		f=open("testingtk3.py")
		file1=File(self.defaultproject, 0, 'testingtk3.py0', f.read())
		f.close()
		self.defaultfile=file1
		f=open("testingtk3.py")
		file2=File(self.defaultproject, 1, 'testingtk3.py1', f.read())
		f.close()
		f=open("cluttertest3.py")
		file3=File(self.defaultproject, 1, 'cluttertest3.py1', f.read())
		f.close()

		f=open("testingtk3.py")
		file1=File(self.defaultproject, 2, 'testingtk3.py2', f.read())
		f.close()
		f=open("testingtk3.py")
		file2=File(self.defaultproject, 3, 'testingtk3.py3', f.read())
		f.close()
		f=open("cluttertest3.py")
		file3=File(self.defaultproject, 4, 'cluttertest3.py4', f.read())
		f.close()

		f=open("testingtk3.py")
		file1=File(self.defaultproject, 5, 'testingtk3.py5', f.read())
		f.close()
		f=open("testingtk3.py")
		file2=File(self.defaultproject, 6, 'testingtk3.py6', f.read())
		f.close()
		f=open("cluttertest3.py")
		file3=File(self.defaultproject, 7, 'cluttertest3.py7', f.read())
		f.close()

		f.close()
		self.defaultproject.create_revision() #make a new head

		self.defaultrevision=7
		self.defaultfile='cluttertest3.py'

		#win=viewer.TempWindow(self,self.defaultproject,self.defaultrevision,self.defaultfile)
		win=viewer.TempWindow(self,self.defaultproject,None,None)
		win.connect("delete-event",Gtk.main_quit)
		win.show_all()

		#GObject.MainLoop().run()
		Gtk.main()

###---------------------------MAIN SWITCH----------------------------###
	def on_window_mode_changed(self,new_window_name,parent_window,activeproject,activerev,activefile):
		parent_window.destroy()
		if new_window_name==("Viewer"):
			#window=viewer.TempWindow(self,self.defaultproject,self.defaultrevision,self.defaultfile) #DEMO CODE
			window=viewer.TempWindow(self,activeproject,activerev,activefile) #REAL CODE
			window.connect("delete-event",Gtk.main_quit)
			window.show_all()
		if new_window_name==("Explorer"):
			window=explorer.explorer_window(self,)
			window.connect("delete-event",Gtk.main_quit)
			window.show_all()
		if new_window_name==("Editor"):
			window=editor.Editor(self,activeproject,activerev,activefile)
			window.connect("delete-event",Gtk.main_quit)
			window.show_all()

###---------------------------------MAIN-------------------------------###

a=tanCS()
