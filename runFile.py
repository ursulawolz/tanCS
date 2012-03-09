from TankWorld import TankWorld
from Tank import *
import string

class PermissionError(Exception):
	'''Not sure how to name this. It it the error that gets raised when a user
	tries to access things they shouldn't
	'''

	def __init__(self, illegalChars, codeLine):
		self.value = illegalChars
		self.line = codeLine

	def __str__(self):
		return "\n" + self.line + "User defined scripts are not allowed to include \"" + self.value + "\""

def getInitialWhitespace(string):
	res = 0
	for letter in string:
		if letter == ' ':
			res += 1
		elif letter == '\t':
			res += 4
		else:
			break
	return ' ' * res


def runFile(filename):
	'''readFile opens and runs a user file, making sure that none of the 
	things in said file are illegal in TankWorld, in illegalStrings


	'''
	illegalStrings = ['__', 'TankWorld', 'tankWorld', 'WorldObject', 'Tank']
	appendToBeginning = '''
tankWorld = TankWorld()
tank = Tank(tankWorld,	 tankWorld.render)

def userFun():
'''
	appendToEnd = '''
x = userFun()
tank.setGenerator(x)
tank.runTasks()'''

	yieldClause = 'yield()\n'
	tabClause = '    '

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
	prevTabs = ''

	for line in lines:
		if line[len(line) - 1] != '\n':
			line += '\n'
		x = line.strip()

		prevTabs = getInitialWhitespace(line)
		
		if x == '' or ':' in line:
			code = code + tabClause + line
		else:
			code = code + tabClause + line + tabClause + prevTabs + yieldClause

		print len(prevTabs)



	f = open('run' + filename, 'w')
	f.close()

	edited = open('run' + filename, 'r+b')
	edited.seek(0)
	edited.write(code)
	edited.close()

	execfile('run' + filename)










