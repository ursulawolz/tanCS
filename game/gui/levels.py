from gi.repository import Gtk, Gdk
import pdb
class LevelWindow(Gtk.Window): 
	def parseLevels(self):
		'''
		Parse the level file and return a reasonable thing.
		'''
		self.appendpath = '../game/gui/'
		f = open('../game/gui/levels.txt')

		levels = [] 
		onWorld = -1
		for i in f:
			st = i.strip().split('@')
			if len(st) > 2: #random number for the lols
				levels[onWorld]['levelInfo'].append([st[0], st[1],st[2]])
			elif len(st) == 1:
				onWorld+=1
				levels.append({'name':st[0],'levelInfo':[]})

		return levels

	def __init__(self):
		Gtk.Window.__init__(self, title="Select a Level")
		grid=Gtk.Grid()
		self.add(grid)
		labels = []
		info = []
		#vScrollbar = Gtk.VScrollbar()
		#grid.attach(vScrollbar, 1, 2, 0, 1, gtk.FILL|gtk.SHRINK,
		#	gtk.FILL|gtk.SHRINK, 0, 0)
		levels = self.parseLevels()

		#Grab the current level that you are on
		
		try:
			f = open('saved.data')
			self.worldNum = int(f.readline().strip().split('orld')[1])

			self.levelNum = int(f.readline().strip().split('evel')[1])
		except:
			print "Could not read"
			self.worldNum = 1
			self.levelNum = 1


		#pdb.set_trace()
		x = 0
		y = 0

		told = None
		for w in levels:
			l = Gtk.Label(w)
			size = (2,2)
			table = Gtk.Table(size[0],size[1], True)
			worldLabel = Gtk.Label(w['name'])
			table.attach(worldLabel, 0, size[0]+1, 0, 1)
			#table.set_row_spacing(0,20)
			#worldLabel.set_border_width(15)
			if told == None:
				grid.add(table)
				told = table
				hasAdded = True
			else:

				grid.attach_next_to(table, told,Gtk.PositionType.BOTTOM,1,1)
				told = table
			x = 0
			y = 0
			count = 0
			for k in w['levelInfo']:
				count +=1
				button = Gtk.Button(k[0]+":" +k[1])
				table.attach(button, x, x+1, y+1, y+2)				
				#print levels[w][k][0]+":" +levels[w][k][1]
				
				#table.(button)
				button.connect('clicked',self.selectLevel,k, int(w['name'].split('orld')[1]), count)
				x += 1
				if x > size[0]:
					x =0
					y += 1
		
		self.levelGrid = Gtk.Table(1,9)
		#self.levelGrid.set_col_spacing(1,100)

		grid.attach(self.levelGrid,1,0,1,2)
		#self.boxSeperator.add(self.levelGrid)
		self.levelGrid.set_border_width(15)
		#self.worldNameLabel=
		self.levelNameLabel=Gtk.Label("No level Selected")
		self.levelNameLabel.set_alignment(0,1)
		self.levelGrid.attach(self.levelNameLabel, 0, 1, 0, 1)
		
		self.levelImage = Gtk.Image()
		
		self.levelImage.set_alignment(0,1)
		#self.levelGrid.attach_next_to( self.levelImage,self.levelNameLabel,Gtk.PositionType.BOTTOM,2,2)
		self.levelGrid.attach( self.levelImage, 0, 1, 1, 2)
		
		self.levelDescription=Gtk.Label("No level Descriptions lololol")
		#self.levelGrid.attach_next_to( self.levelDescription, self.levelImage,Gtk.PositionType.BOTTOM,2,2)
		self.levelGrid.attach( self.levelDescription, 0, 1, 2, 3)
		print self.levelNum
		self.selectLevel(None, levels[self.worldNum-1]['levelInfo'][self.levelNum-1], self.worldNum, self.levelNum)

	def close(self, unused1, unused2):
		f = open('../game/gui/saved.data', 'w')
		f.write('World'+str(self.worldNum)+'\n'+'Level'+str(self.levelNum)+'\n')
		f.close()
		print "Closed Gui"
	def selectLevel(self, button, level,worldnum,levelnum):
		self.levelNameLabel.set_text(level[0] + ": "+ level[1])
		self.levelDescription.set_text(level[2])
		self.levelImage.set_from_file(self.appendpath +level[0]+'.png')
		
		#pixbuf = self.levelImage.get_pixbuf()

		#scaled_buf = pixbuf.scale_simple(.5,.5,2)

		#self.levelImage.set_from_pixbuf(pixbuf)
		#im.show()
		
		#self.levelImage.set_pixel_size(.1);
		#self.levelImage.set_size_request(10,10)
		self.levelNum = levelnum
		self.worldNum = worldnum


#win=GridWindow()
#win.connect("delete-event", Gtk.main_quit)
#win.connect("delete-event", win.close)
#win.show_all()
#Gtk.main()

