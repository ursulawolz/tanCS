###------------------------------Inclusions--------------------------------###
from gi.repository import Gtk,GObject
from gi.repository import Gdk
import viewerproto2 as viewer
import editortest as editor
import explorerproto2 as explorer
from objectcode import *
import os
import platform
import subprocess

class tanCS(object):

	def __init__(self):
		win=viewer.TempWindow(self)
		win.connect("delete-event",Gtk.main_quit)
		win.show_all()
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
		f=open("testingtk3.py")
		self.defaultfile=File('projectHASH', 0, 'testingtk3.py', f.read())
		#self.default

		#self.defaultrevision=Revision(0)
		self.defaultproject=Project

		Gtk.main()

###---------------------------MAIN SWITCH----------------------------###
	def on_window_mode_changed(self,new_window_name,parent_window):
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
		parent_window.destroy()

###---------------------------------MAIN-------------------------------###
	
a=tanCS()
