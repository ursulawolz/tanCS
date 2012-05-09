###------------------------------Inclusions--------------------------------###
from gi.repository import GtkClutter
GtkClutter.init([])
from gi.repository import Gtk,GObject
from gi.repository import Gdk
import viewerproto2 as viewer
import editortest as editor
import explorerproto2 as explorer
from objectcode import *
import os
import platform
import subprocess
import pdb

class tanCS(object):

	def __init__(self):
		self.user=None
		self.borrows=[]
		
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
		
		#in the process of creating default objects
		self.defaultgroup=Group('groupHASH',set('userHASH'),'godHASH',"default group")
		self.defaultaccount=Account('userHASH', 'oranges', 'kiwi', 'explorer-icon.png')
		self.defaultproject=Project('The default!','A dummy project.', 'proj01',None, 8, 'groupHASH')
		f=open("testingtk3.py")
		file1=File(self.defaultproject, 0, 'testingtk3.py', f.read())
		f.close()
		self.defaultfile=file1
		f=open("testingtk3.py")
		file2=File(self.defaultproject, 1, 'testingtk3.py', f.read())
		f.close()
		f=open("cluttertest3.py")
		file3=File(self.defaultproject, 1, 'cluttertest3.py', f.read())

		f=open("testingtk3.py")
		file1=File(self.defaultproject, 2, 'testingtk3.py', f.read())
		self.defaultfile=file1
		f.close()
		f=open("testingtk3.py")
		file2=File(self.defaultproject, 3, 'testingtk3.py', f.read())
		f.close()
		f=open("cluttertest3.py")
		file3=File(self.defaultproject, 4, 'cluttertest3.py', f.read())
		f.close()

		f=open("testingtk3.py")
		file1=File(self.defaultproject, 5, 'testingtk3.py', f.read())
		self.defaultfile=file1
		f.close()
		f=open("testingtk3.py")
		file2=File(self.defaultproject, 6, 'testingtk3.py', f.read())
		f.close()
		f=open("cluttertest3.py")
		file3=File(self.defaultproject, 7, 'cluttertest3.py', f.read())
		f.close()

		f.close()
		self.defaultproject.head=Head(prevrev=self.defaultproject.revisions[-1])
		#self.defaultproject.revisions=[defaultrevision]
		#self.defaultproject.head=defaulthead

		win=viewer.TempWindow(self)
		win.connect("delete-event",Gtk.main_quit)
		win.show_all()

		#GObject.MainLoop().run()
		Gtk.main()

###---------------------------MAIN SWITCH----------------------------###
	def on_window_mode_changed(self,new_window_name,parent_window):
		parent_window.destroy()
		if new_window_name==("Viewer"):
			window=viewer.TempWindow(self)
			window.connect("delete-event",Gtk.main_quit)
			window.show_all()
		if new_window_name==("Explorer"):
			window=explorer.explorer_window(self)
			window.connect("delete-event",Gtk.main_quit)
			window.show_all()
		if new_window_name==("Editor"):
			window=editor.Editor(self)
			window.connect("delete-event",Gtk.main_quit)
			window.show_all()

###---------------------------------MAIN-------------------------------###
	
a=tanCS()
