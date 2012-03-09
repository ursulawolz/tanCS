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
	appendToBeginning = '''
tankWorld = TankWorld()
tank = Tank(tankWorld, tankWorld.render)

def userFun():
    '''
    

	yieldClause = '    yield()\n    '
	newLineClause = '    '

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
		if line[len(line) - 1] != '\n':
			line += '\n'
		x = line.strip()
		if x == '':
			code = code + line + newLineClause
		else:
			code = code + line + yieldClause


	f = open('run' + filename, 'w')
	f.close()

	edited = open('run' + filename, 'r+b')
	edited.seek(0)
	edited.write(code)
	edited.close()

	execfile('run' + filename)










