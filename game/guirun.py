
import sys
sys.path.append("../game")
sys.path.append("..")
sys.path.append("game")
from TankWorld import TankWorld
from runFile import runFile
import sys
#import xmlParse
import levels.MakeLevel


import sys
sys.path.append("../game")
sys.path.append("..")
sys.path.append("game")
from TankWorld import TankWorld
from runFile import runFile
import sys
#import xmlParse
import levels.MakeLevel

import os
os.chdir("../game")


def runGame(userfile):

	import os
	os.system('python forkrun.py '+userfile)

	
