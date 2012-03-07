from TankWorld import TankWorld
from Tank import *
import pickle

class PermissionError(Exception):
	'''Not sure how to name this. It it the error that gets raised when a user
	tries to access things they shouldn't
	'''

	def __init__(self, illegalChars, codeLine):
		self.value = illegalChars
		self.line = codeLine

	def __str__(self):
		return "\n" + self.line + "User defined scripts are not allowed to include \"" + self.value + "\""


def runFile(filename):
	'''readFile opens and runs a user file, making sure that none of the 
	things in said file are illegal in TankWorld, in illegalStrings


	'''
	illegalStrings = ['__', 'TankWorld', 'tankWorld', 'WorldObject', 'Tank']
	appendToBeginning = '''tankWorld = TankWorld()\n
tank = Tank(tankWorld.getPhysics(), tankWorld.render)\n
tank.setTankWorld(tankWorld)\n'''


	script = open(filename, 'rb')
	lines = script.readlines()
	#Check for illegal strings in file
	for line in lines:
		for illegal in illegalStrings:
			if illegal in line:
				print line
				raise PermissionError(illegal, line)

	#If no errors:
	code = appendToBeginning
	for line in lines:
		code = code + line

	f = open('run' + filename, 'w')
	f.close()

	edited = open('run' + filename, 'r+b')
	edited.seek(0)
	edited.write(code)
	edited.close()

	execfile('run' + filename)










